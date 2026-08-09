import base64
import gc
import math
import os
import re
import secrets
import statistics
import time
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path

import pandas as pd
from cryptography.hazmat.primitives.asymmetric import rsa


# Project folders
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
SOURCE_DIR = PROJECT_ROOT / "2_sample_data" / "source_original"
OUTPUT_DIR = PROJECT_ROOT / "2_sample_data" / "rsa_she"
METRICS_DIR = PROJECT_ROOT / "3_output_data" / "run_metrics"
VALIDATION_DIR = PROJECT_ROOT / "3_output_data" / "validation_reports"

# Study settings
ENVIRONMENT_START = 26
ENVIRONMENT_END = 40
TIMED_RUNS = 5
RSA_KEY_SIZE = 2048
RSA_PUBLIC_EXPONENT = 65537
MAP_SBP_COLUMN = "bp_systolic"
MAP_DBP_COLUMN = "bp_diastolic"
ROUNDTRIP_SAMPLE_ROWS = 12
GENERAL_ENCODING_SENTINEL = b"\x01"

PROTECTED_COLUMNS = [
    "org_id",
    "device_id",
    "timestamp",
    "heart_rate",
    "bp_systolic",
    "bp_diastolic",
    "spo2",
    "temperature",
    "battery_level",
]

MAP_COLUMNS = {MAP_SBP_COLUMN, MAP_DBP_COLUMN}


@dataclass
class RSAContext:
    n: int
    e: int
    d: int
    p: int
    q: int
    dmp1: int
    dmq1: int
    iqmp: int
    ciphertext_bytes: int


@dataclass
class CryptoWorkflowResult:
    encrypted_dataframe: pd.DataFrame
    hybrid_ciphertexts: list
    masks: list
    evaluation_ciphertexts: list
    evaluation_masks: list
    rsa_context: RSAContext
    homomorphic_base: int
    max_map_numerator: int
    elapsed_time_sec: float
    rsa_keygen_time_sec: float
    homomorphic_setup_time_sec: float
    rsa_stage_time_sec: float
    homomorphic_layer_time_sec: float
    evaluation_time_sec: float
    structure_time_sec: float


# Read the environment number from a filename
def get_environment_number(filename):
    match = re.search(r"ENV-(\d+)", filename, re.IGNORECASE)
    return int(match.group(1)) if match else None


# Find one source file for each RSA-SHE environment
def find_source_files():
    if not SOURCE_DIR.is_dir():
        raise FileNotFoundError(f"Source folder not found: {SOURCE_DIR}")

    source_files = {}
    for file_path in SOURCE_DIR.glob("*.csv"):
        environment_number = get_environment_number(file_path.name)
        if environment_number is None:
            continue
        if not ENVIRONMENT_START <= environment_number <= ENVIRONMENT_END:
            continue
        if environment_number in source_files:
            raise ValueError(f"Duplicate source file for ENV-{environment_number}")
        source_files[environment_number] = file_path

    missing = [
        number
        for number in range(ENVIRONMENT_START, ENVIRONMENT_END + 1)
        if number not in source_files
    ]
    if missing:
        names = ", ".join(f"ENV-{number}" for number in missing)
        raise FileNotFoundError(f"Missing source files: {names}")

    return source_files


# Load and structurally validate one source file before timing begins
def load_source_file(file_path):
    dataframe = pd.read_csv(file_path, dtype=str, keep_default_na=False)

    if list(dataframe.columns) != PROTECTED_COLUMNS:
        raise ValueError(
            f"{file_path.name} must contain the nine protected columns in order"
        )
    if dataframe.empty:
        raise ValueError(f"{file_path.name} does not contain data rows")
    if dataframe.isna().any().any():
        raise ValueError(f"{file_path.name} contains missing values")

    validate_source_values(dataframe)
    return dataframe


# Parse an integer-valued blood-pressure field without using float arithmetic
def parse_bp_integer(value, column_name):
    text = str(value).strip()
    try:
        number = Decimal(text)
    except InvalidOperation as error:
        raise ValueError(f"{column_name} contains a nonnumeric value: {value}") from error

    if number != number.to_integral_value():
        raise ValueError(f"{column_name} must contain integer values for MAP evaluation")

    integer_value = int(number)
    if integer_value < 0:
        raise ValueError(f"{column_name} contains a negative value")
    return integer_value


# Validate source-value suitability before cryptographic timing begins
def validate_source_values(dataframe):
    max_map_numerator = 0

    for row in dataframe.itertuples(index=False, name=None):
        row_map = dict(zip(PROTECTED_COLUMNS, row))
        sbp = parse_bp_integer(row_map[MAP_SBP_COLUMN], MAP_SBP_COLUMN)
        dbp = parse_bp_integer(row_map[MAP_DBP_COLUMN], MAP_DBP_COLUMN)
        numerator = sbp + (2 * dbp)
        max_map_numerator = max(max_map_numerator, numerator)

        for column, value in row_map.items():
            if column in MAP_COLUMNS:
                continue
            raw = str(value).encode("utf-8")
            if len(raw) > 240:
                raise ValueError(
                    f"{column} contains a value too long for the 2048-bit study encoding"
                )

    if max_map_numerator <= 0:
        raise ValueError("MAP numerator range is invalid")

    return max_map_numerator


# Generate one run-specific RSA key pair
def generate_rsa_context():
    private_key = rsa.generate_private_key(
        public_exponent=RSA_PUBLIC_EXPONENT,
        key_size=RSA_KEY_SIZE,
    )
    numbers = private_key.private_numbers()
    public_numbers = numbers.public_numbers

    return RSAContext(
        n=public_numbers.n,
        e=public_numbers.e,
        d=numbers.d,
        p=numbers.p,
        q=numbers.q,
        dmp1=numbers.dmp1,
        dmq1=numbers.dmq1,
        iqmp=numbers.iqmp,
        ciphertext_bytes=RSA_KEY_SIZE // 8,
    )


# CRT-accelerated textbook RSA private operation used only after timing for validation
def rsa_private_operation_crt(ciphertext, context):
    m1 = pow(ciphertext, context.dmp1, context.p)
    m2 = pow(ciphertext, context.dmq1, context.q)
    h = (context.iqmp * (m1 - m2)) % context.p
    return m2 + (h * context.q)


# Draw a fresh random invertible value modulo n
def random_unit(n):
    while True:
        candidate = secrets.randbelow(n - 3) + 2
        if math.gcd(candidate, n) == 1:
            return candidate


# Choose a run-specific exponent-encoding base and prove uniqueness over the required range
def choose_homomorphic_base(n, max_exponent):
    for _ in range(128):
        base = random_unit(n)
        if base == 1:
            continue

        seen = set()
        value = 1
        valid = True
        for _exponent in range(max_exponent + 1):
            if value in seen:
                valid = False
                break
            seen.add(value)
            value = (value * base) % n

        if valid:
            return base

    raise ValueError("Could not generate a unique homomorphic exponent base")


# Reversible integer encoding for protected values not used in the MAP computation
def encode_general_value(value, modulus):
    raw = str(value).encode("utf-8")
    if len(raw) > 65535:
        raise ValueError("Protected value is too long for the general encoding")

    payload = GENERAL_ENCODING_SENTINEL + len(raw).to_bytes(2, "big") + raw
    encoded = int.from_bytes(payload, "big")

    if not 0 < encoded < modulus:
        raise ValueError("Encoded protected value does not fit inside the RSA modulus")
    if math.gcd(encoded, modulus) != 1:
        raise ValueError("Encoded protected value is not invertible modulo the RSA modulus")

    return encoded


# Decode a general protected value after validation decryption/unmasking
def decode_general_value(encoded):
    length = max(1, (encoded.bit_length() + 7) // 8)
    payload = encoded.to_bytes(length, "big")

    if len(payload) < 3 or payload[:1] != GENERAL_ENCODING_SENTINEL:
        raise ValueError("Decoded general value has an invalid sentinel")

    expected_length = int.from_bytes(payload[1:3], "big")
    raw = payload[3:]
    if len(raw) != expected_length:
        raise ValueError("Decoded general value has an invalid length")

    return raw.decode("utf-8")


# Fixed-width Base64 representation of one RSA-sized ciphertext
def ciphertext_to_base64(ciphertext, context):
    raw = ciphertext.to_bytes(context.ciphertext_bytes, "big")
    return base64.b64encode(raw).decode("ascii")


# Decode and validate one fixed-width Base64 ciphertext
def base64_to_ciphertext(value, context):
    try:
        raw = base64.b64decode(str(value), validate=True)
    except Exception as error:
        raise ValueError("Encrypted output contains invalid Base64") from error

    if len(raw) != context.ciphertext_bytes:
        raise ValueError("Encrypted output contains an invalid RSA ciphertext length")

    ciphertext = int.from_bytes(raw, "big")
    if not 0 <= ciphertext < context.n:
        raise ValueError("Encrypted output contains a ciphertext outside the RSA modulus")
    return ciphertext


# Encode the source value for the RSA stage
def encode_for_rsa(column, value, context, homomorphic_base):
    if column in MAP_COLUMNS:
        exponent = parse_bp_integer(value, column)
        encoded = pow(homomorphic_base, exponent, context.n)
        if math.gcd(encoded, context.n) != 1:
            raise ValueError(f"{column} exponent encoding is not invertible")
        return encoded

    return encode_general_value(value, context.n)


# Complete one cryptographic workflow. The total timer covers exactly Decision 3.
def run_crypto_workflow(dataframe, max_map_numerator):
    total_start = time.perf_counter()

    keygen_start = time.perf_counter()
    context = generate_rsa_context()
    rsa_keygen_time = time.perf_counter() - keygen_start

    setup_start = time.perf_counter()
    homomorphic_base = choose_homomorphic_base(context.n, max_map_numerator)
    homomorphic_setup_time = time.perf_counter() - setup_start

    # Stage 1: deterministic source encoding followed by textbook RSA modular encryption.
    rsa_stage_start = time.perf_counter()
    rsa_cipher_rows = []
    for row in dataframe.itertuples(index=False, name=None):
        rsa_row = []
        for column, value in zip(PROTECTED_COLUMNS, row):
            encoded = encode_for_rsa(column, value, context, homomorphic_base)
            rsa_row.append(pow(encoded, context.e, context.n))
        rsa_cipher_rows.append(rsa_row)
    rsa_stage_time = time.perf_counter() - rsa_stage_start

    # Stage 2: MEHE-inspired controlled randomizing layer applied after RSA.
    # H = RSA(encoded) * RSA(r) mod n = RSA(encoded * r mod n).
    homomorphic_layer_start = time.perf_counter()
    hybrid_rows = []
    mask_rows = []
    encoded_output_rows = []

    for rsa_row in rsa_cipher_rows:
        hybrid_row = []
        mask_row = []
        encoded_row = []

        for rsa_ciphertext in rsa_row:
            mask = random_unit(context.n)
            encrypted_mask = pow(mask, context.e, context.n)
            hybrid_ciphertext = (rsa_ciphertext * encrypted_mask) % context.n

            hybrid_row.append(hybrid_ciphertext)
            mask_row.append(mask)
            encoded_row.append(ciphertext_to_base64(hybrid_ciphertext, context))

        hybrid_rows.append(hybrid_row)
        mask_rows.append(mask_row)
        encoded_output_rows.append(encoded_row)

    homomorphic_layer_time = time.perf_counter() - homomorphic_layer_start
    del rsa_cipher_rows

    # Stage 3: encrypted MAP-numerator evaluation: SBP + 2(DBP).
    evaluation_start = time.perf_counter()
    sbp_index = PROTECTED_COLUMNS.index(MAP_SBP_COLUMN)
    dbp_index = PROTECTED_COLUMNS.index(MAP_DBP_COLUMN)
    evaluation_ciphertexts = []
    evaluation_masks = []

    for hybrid_row, mask_row in zip(hybrid_rows, mask_rows):
        sbp_ciphertext = hybrid_row[sbp_index]
        dbp_ciphertext = hybrid_row[dbp_index]

        evaluated_ciphertext = (
            sbp_ciphertext * pow(dbp_ciphertext, 2, context.n)
        ) % context.n
        combined_mask = (
            mask_row[sbp_index] * pow(mask_row[dbp_index], 2, context.n)
        ) % context.n

        evaluation_ciphertexts.append(evaluated_ciphertext)
        evaluation_masks.append(combined_mask)

    evaluation_time = time.perf_counter() - evaluation_start

    structure_start = time.perf_counter()
    encrypted_dataframe = pd.DataFrame(encoded_output_rows, columns=PROTECTED_COLUMNS)
    structure_time = time.perf_counter() - structure_start

    elapsed_time = time.perf_counter() - total_start

    return CryptoWorkflowResult(
        encrypted_dataframe=encrypted_dataframe,
        hybrid_ciphertexts=hybrid_rows,
        masks=mask_rows,
        evaluation_ciphertexts=evaluation_ciphertexts,
        evaluation_masks=evaluation_masks,
        rsa_context=context,
        homomorphic_base=homomorphic_base,
        max_map_numerator=max_map_numerator,
        elapsed_time_sec=elapsed_time,
        rsa_keygen_time_sec=rsa_keygen_time,
        homomorphic_setup_time_sec=homomorphic_setup_time,
        rsa_stage_time_sec=rsa_stage_time,
        homomorphic_layer_time_sec=homomorphic_layer_time,
        evaluation_time_sec=evaluation_time,
        structure_time_sec=structure_time,
    )


# One untimed warm-up followed by five timed runs; retain the median run.
def run_timed_encryption(dataframe):
    max_map_numerator = validate_source_values(dataframe)

    warmup_result = run_crypto_workflow(dataframe, max_map_numerator)
    del warmup_result
    gc.collect()

    timed_results = []
    for run_number in range(1, TIMED_RUNS + 1):
        gc.collect()
        result = run_crypto_workflow(dataframe, max_map_numerator)
        timed_results.append((run_number, result))

    median_time = statistics.median(
        result.elapsed_time_sec for _, result in timed_results
    )
    median_run_number, median_result = min(
        timed_results,
        key=lambda item: abs(item[1].elapsed_time_sec - median_time),
    )

    return timed_results, median_run_number, median_result, median_time


# Build a bounded discrete-log lookup for the validated MAP-numerator range.
def build_exponent_lookup(base, modulus, max_exponent):
    lookup = {}
    value = 1

    for exponent in range(max_exponent + 1):
        if value in lookup:
            raise ValueError("Homomorphic base is not unique over the MAP range")
        lookup[value] = exponent
        value = (value * base) % modulus

    return lookup


# Deterministic set of rows for direct decrypt/unmask round-trip spot checks.
def validation_sample_indexes(row_count):
    if row_count <= ROUNDTRIP_SAMPLE_ROWS:
        return list(range(row_count))

    indexes = {
        round(position * (row_count - 1) / (ROUNDTRIP_SAMPLE_ROWS - 1))
        for position in range(ROUNDTRIP_SAMPLE_ROWS)
    }
    return sorted(indexes)


# Validate structure, every ciphertext relation, MAP evaluation, decryption, and exposure.
def validate_output(source_dataframe, result):
    encrypted_dataframe = result.encrypted_dataframe
    context = result.rsa_context
    base = result.homomorphic_base

    if list(encrypted_dataframe.columns) != PROTECTED_COLUMNS:
        raise ValueError("Encrypted columns do not match the source columns")
    if len(encrypted_dataframe) != len(source_dataframe):
        raise ValueError("Encrypted row count does not match the source row count")
    if encrypted_dataframe.isna().any().any():
        raise ValueError("Encrypted output contains missing values")

    source_values = source_dataframe.to_numpy(dtype=str)
    encrypted_values = encrypted_dataframe.to_numpy(dtype=str)
    unchanged_values = int((source_values == encrypted_values).sum())
    total_values = int(source_values.size)
    exposure = (unchanged_values / total_values) * 100

    if exposure != 0:
        raise ValueError("Clear-text exposure was not zero")

    # Validate every output ciphertext and its exact public-key construction.
    construction_checks = 0
    for row_index, source_row in enumerate(
        source_dataframe.itertuples(index=False, name=None)
    ):
        for column_index, (column, source_value) in enumerate(
            zip(PROTECTED_COLUMNS, source_row)
        ):
            ciphertext = base64_to_ciphertext(
                encrypted_dataframe.iat[row_index, column_index], context
            )
            if ciphertext != result.hybrid_ciphertexts[row_index][column_index]:
                raise ValueError("Serialized ciphertext does not match in-memory ciphertext")

            encoded = encode_for_rsa(column, source_value, context, base)
            rsa_ciphertext = pow(encoded, context.e, context.n)
            mask = result.masks[row_index][column_index]
            expected_ciphertext = (
                rsa_ciphertext * pow(mask, context.e, context.n)
            ) % context.n

            if ciphertext != expected_ciphertext:
                raise ValueError("Hybrid ciphertext construction validation failed")
            construction_checks += 1

    # Directly decrypt/unmask a deterministic sample across all nine columns.
    sample_indexes = validation_sample_indexes(len(source_dataframe))
    roundtrip_checks = 0
    for row_index in sample_indexes:
        source_row = source_dataframe.iloc[row_index]

        for column_index, column in enumerate(PROTECTED_COLUMNS):
            ciphertext = result.hybrid_ciphertexts[row_index][column_index]
            mask = result.masks[row_index][column_index]
            decrypted_masked = rsa_private_operation_crt(ciphertext, context)
            recovered_encoded = (
                decrypted_masked * pow(mask, -1, context.n)
            ) % context.n

            if column in MAP_COLUMNS:
                expected_integer = parse_bp_integer(source_row[column], column)
                expected_encoded = pow(base, expected_integer, context.n)
                if recovered_encoded != expected_encoded:
                    raise ValueError(f"{column} round-trip validation failed")
            else:
                recovered_value = decode_general_value(recovered_encoded)
                if recovered_value != str(source_row[column]):
                    raise ValueError(f"{column} round-trip validation failed")

            roundtrip_checks += 1

    # Decrypt and verify every encrypted MAP-numerator evaluation result.
    exponent_lookup = build_exponent_lookup(
        base, context.n, result.max_map_numerator
    )
    map_evaluations_checked = 0

    for row_index, source_row in source_dataframe.iterrows():
        evaluated_ciphertext = result.evaluation_ciphertexts[row_index]
        combined_mask = result.evaluation_masks[row_index]

        sbp = parse_bp_integer(source_row[MAP_SBP_COLUMN], MAP_SBP_COLUMN)
        dbp = parse_bp_integer(source_row[MAP_DBP_COLUMN], MAP_DBP_COLUMN)
        expected_numerator = sbp + (2 * dbp)

        # Confirm the ciphertext-domain operation itself matches the published frozen rule.
        sbp_index = PROTECTED_COLUMNS.index(MAP_SBP_COLUMN)
        dbp_index = PROTECTED_COLUMNS.index(MAP_DBP_COLUMN)
        expected_evaluation_ciphertext = (
            result.hybrid_ciphertexts[row_index][sbp_index]
            * pow(result.hybrid_ciphertexts[row_index][dbp_index], 2, context.n)
        ) % context.n
        if evaluated_ciphertext != expected_evaluation_ciphertext:
            raise ValueError("Encrypted MAP evaluation construction failed")

        decrypted_masked = rsa_private_operation_crt(evaluated_ciphertext, context)
        recovered_encoded = (
            decrypted_masked * pow(combined_mask, -1, context.n)
        ) % context.n
        recovered_numerator = exponent_lookup.get(recovered_encoded)

        if recovered_numerator is None:
            raise ValueError("Encrypted MAP result was outside the validated exponent range")
        if recovered_numerator != expected_numerator:
            raise ValueError("Homomorphic MAP-numerator evaluation validation failed")

        # MAP division is intentionally performed only after validation decryption.
        recovered_map = Decimal(recovered_numerator) / Decimal(3)
        expected_map = Decimal(expected_numerator) / Decimal(3)
        if recovered_map != expected_map:
            raise ValueError("Post-decryption MAP validation failed")

        map_evaluations_checked += 1

    return {
        "row_count_valid": True,
        "column_order_valid": True,
        "missing_values": 0,
        "protected_values": total_values,
        "unchanged_values": unchanged_values,
        "clear_text_exposure_percent": exposure,
        "ciphertext_valid": True,
        "hybrid_construction_checks": construction_checks,
        "roundtrip_decrypt_checks": roundtrip_checks,
        "map_evaluations_checked": map_evaluations_checked,
        "map_evaluations_valid": map_evaluations_checked,
        "map_evaluation_operation": "SBP + 2(DBP)",
        "map_division_stage": "post_validation_decryption",
        "homomorphic_base_range_valid": True,
        "arithmetic_bounds_valid": True,
        "rsa_key_size_bits": RSA_KEY_SIZE,
        "rsa_public_exponent": RSA_PUBLIC_EXPONENT,
    }


# Write a CSV without leaving a partial output file
def write_csv(dataframe, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = output_path.with_suffix(".tmp")
    dataframe.to_csv(temporary_path, index=False)
    os.replace(temporary_path, output_path)


# Process one environment
def process_environment(environment_number, source_path):
    source_dataframe = load_source_file(source_path)
    timed_results, median_run_number, median_result, median_time = run_timed_encryption(
        source_dataframe
    )

    # All correctness/decryption/exposure validation occurs after the timer stopped.
    validation = validate_output(source_dataframe, median_result)

    environment_id = f"ENV-{environment_number:02d}"
    output_filename = f"rsa_she_encrypted_{environment_id}.csv"
    write_csv(median_result.encrypted_dataframe, OUTPUT_DIR / output_filename)

    metrics = {
        "environment_id": environment_id,
        "encryption_code": 3,
        "encryption_type": "RSA-SHE",
        "source_file": source_path.name,
        "output_file": output_filename,
        "row_count": len(source_dataframe),
        "column_count": len(source_dataframe.columns),
    }

    for run_number, result in timed_results:
        metrics[f"run_{run_number}_sec"] = round(result.elapsed_time_sec, 9)

    metrics["simulated_encryption_time_sec"] = round(median_time, 9)
    metrics["median_run_number"] = median_run_number
    metrics["median_rsa_keygen_time_sec"] = round(
        median_result.rsa_keygen_time_sec, 9
    )
    metrics["median_homomorphic_setup_time_sec"] = round(
        median_result.homomorphic_setup_time_sec, 9
    )
    metrics["median_rsa_stage_time_sec"] = round(
        median_result.rsa_stage_time_sec, 9
    )
    metrics["median_homomorphic_layer_time_sec"] = round(
        median_result.homomorphic_layer_time_sec, 9
    )
    metrics["median_evaluation_time_sec"] = round(
        median_result.evaluation_time_sec, 9
    )
    metrics["median_structure_time_sec"] = round(
        median_result.structure_time_sec, 9
    )

    validation_record = {
        "environment_id": environment_id,
        "source_file": source_path.name,
        "output_file": output_filename,
        **validation,
        "status": "PASS",
    }

    print(
        f"{environment_id}: {median_time:.6f} seconds "
        f"(median run {median_run_number}; "
        f"{validation['map_evaluations_checked']} MAP evaluations validated)"
    )
    return metrics, validation_record


# Run all RSA-SHE environments
def main():
    try:
        source_files = find_source_files()
        metrics_records = []
        validation_records = []

        for environment_number in range(
            ENVIRONMENT_START,
            ENVIRONMENT_END + 1,
        ):
            metrics, validation = process_environment(
                environment_number,
                source_files[environment_number],
            )
            metrics_records.append(metrics)
            validation_records.append(validation)

        write_csv(
            pd.DataFrame(metrics_records),
            METRICS_DIR / "rsa_she_timing_results.csv",
        )
        write_csv(
            pd.DataFrame(validation_records),
            VALIDATION_DIR / "rsa_she_validation_report.csv",
        )

        print(f"Completed {len(metrics_records)} environments")
        return 0
    except (FileNotFoundError, ValueError, OSError) as error:
        print(f"RSA-SHE encryption stopped: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
