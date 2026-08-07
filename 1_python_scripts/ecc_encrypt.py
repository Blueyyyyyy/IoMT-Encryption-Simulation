import base64
import os
import re
import statistics
import time
from pathlib import Path

import pandas as pd
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


# Project folders
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
SOURCE_DIR = PROJECT_ROOT / "2_sample_data" / "source_original"
OUTPUT_DIR = PROJECT_ROOT / "2_sample_data" / "ecc"
METRICS_DIR = PROJECT_ROOT / "3_output_data" / "run_metrics"
VALIDATION_DIR = PROJECT_ROOT / "3_output_data" / "validation_reports"

# Study settings
ENVIRONMENT_START = 11
ENVIRONMENT_END = 25
TIMED_RUNS = 5
NONCE_SIZE = 12

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


# Read the environment number from a filename
def get_environment_number(filename):
    match = re.search(r"ENV-(\d+)", filename, re.IGNORECASE)
    return int(match.group(1)) if match else None


# Find one source file for each ECC environment
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


# Load and check one source file
def load_source_file(file_path):
    dataframe = pd.read_csv(file_path, dtype=str, keep_default_na=False)

    if list(dataframe.columns) != PROTECTED_COLUMNS:
        raise ValueError(
            f"{file_path.name} must contain the nine protected columns in order"
        )
    if dataframe.empty:
        raise ValueError(f"{file_path.name} does not contain data rows")

    return dataframe


# Create the shared AES key
def create_aes_key():
    sender_private_key = ec.generate_private_key(ec.SECP384R1())
    receiver_private_key = ec.generate_private_key(ec.SECP384R1())

    sender_secret = sender_private_key.exchange(
        ec.ECDH(),
        receiver_private_key.public_key(),
    )
    receiver_secret = receiver_private_key.exchange(
        ec.ECDH(),
        sender_private_key.public_key(),
    )

    if sender_secret != receiver_secret:
        raise ValueError("ECDH shared secrets did not match")

    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"iomt-ecc-simulation",
    ).derive(sender_secret)


# Encrypt one protected value
def encrypt_value(aesgcm, value):
    nonce = os.urandom(NONCE_SIZE)
    ciphertext = aesgcm.encrypt(nonce, str(value).encode("utf-8"), None)
    return base64.b64encode(nonce + ciphertext).decode("ascii")


# Generate new keys and encrypt all nine columns
def encrypt_dataframe(dataframe):
    aes_key = create_aes_key()
    aesgcm = AESGCM(aes_key)

    encrypted_rows = []
    for row in dataframe.itertuples(index=False, name=None):
        encrypted_rows.append(
            {
                column: encrypt_value(aesgcm, value)
                for column, value in zip(PROTECTED_COLUMNS, row)
            }
        )

    encrypted_dataframe = pd.DataFrame(
        encrypted_rows,
        columns=PROTECTED_COLUMNS,
    )
    return encrypted_dataframe, aes_key


# Warm up once and time five runs
def run_timed_encryption(dataframe):
    encrypt_dataframe(dataframe)

    timed_results = []
    for run_number in range(1, TIMED_RUNS + 1):
        start_time = time.perf_counter()
        encrypted_dataframe, aes_key = encrypt_dataframe(dataframe)
        elapsed_time = time.perf_counter() - start_time
        timed_results.append(
            (run_number, elapsed_time, encrypted_dataframe, aes_key)
        )

    median_time = statistics.median(result[1] for result in timed_results)
    median_result = min(
        timed_results,
        key=lambda result: abs(result[1] - median_time),
    )
    return timed_results, median_result[2], median_result[3], median_time


# Check structure, decryption, and clear-text exposure
def validate_output(source_dataframe, encrypted_dataframe, aes_key):
    if list(encrypted_dataframe.columns) != PROTECTED_COLUMNS:
        raise ValueError("Encrypted columns do not match the source columns")
    if len(encrypted_dataframe) != len(source_dataframe):
        raise ValueError("Encrypted row count does not match the source row count")
    if encrypted_dataframe.isna().any().any():
        raise ValueError("Encrypted output contains missing values")

    source_values = source_dataframe.to_numpy(dtype=str)
    encrypted_values = encrypted_dataframe.to_numpy(dtype=str)
    unchanged_values = int((source_values == encrypted_values).sum())
    aesgcm = AESGCM(aes_key)

    for source_value, encrypted_value in zip(
        source_values.ravel(),
        encrypted_values.ravel(),
    ):
        payload = base64.b64decode(encrypted_value, validate=True)
        if len(payload) <= NONCE_SIZE:
            raise ValueError("Encrypted output contains an invalid AES-GCM payload")
        nonce = payload[:NONCE_SIZE]
        ciphertext = payload[NONCE_SIZE:]
        plaintext = aesgcm.decrypt(nonce, ciphertext, None).decode("utf-8")
        if plaintext != source_value:
            raise ValueError("Decrypted value does not match the source value")

    total_values = int(source_values.size)
    exposure = (unchanged_values / total_values) * 100

    if exposure != 0:
        raise ValueError("Clear-text exposure was not zero")

    return {
        "row_count_valid": True,
        "column_order_valid": True,
        "missing_values": 0,
        "protected_values": total_values,
        "unchanged_values": unchanged_values,
        "clear_text_exposure_percent": exposure,
        "ciphertext_valid": True,
        "decryption_check_valid": True,
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
    timed_results, encrypted_dataframe, aes_key, median_time = run_timed_encryption(
        source_dataframe
    )
    validation = validate_output(
        source_dataframe,
        encrypted_dataframe,
        aes_key,
    )

    environment_id = f"ENV-{environment_number:02d}"
    output_filename = f"ecc_encrypted_{environment_id}.csv"
    write_csv(encrypted_dataframe, OUTPUT_DIR / output_filename)

    metrics = {
        "environment_id": environment_id,
        "encryption_code": 2,
        "encryption_type": "ECC",
        "source_file": source_path.name,
        "output_file": output_filename,
        "row_count": len(source_dataframe),
        "column_count": len(source_dataframe.columns),
    }
    for run_number, elapsed_time, _, _ in timed_results:
        metrics[f"run_{run_number}_sec"] = round(elapsed_time, 9)
    metrics["simulated_encryption_time_sec"] = round(median_time, 9)

    validation_record = {
        "environment_id": environment_id,
        "source_file": source_path.name,
        "output_file": output_filename,
        **validation,
        "status": "PASS",
    }

    print(f"{environment_id}: {median_time:.6f} seconds")
    return metrics, validation_record


# Run all ECC environments
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
            METRICS_DIR / "ecc_timing_results.csv",
        )
        write_csv(
            pd.DataFrame(validation_records),
            VALIDATION_DIR / "ecc_validation_report.csv",
        )

        print(f"Completed {len(metrics_records)} environments")
        return 0
    except Exception as error:
        print(f"ECC encryption stopped: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
