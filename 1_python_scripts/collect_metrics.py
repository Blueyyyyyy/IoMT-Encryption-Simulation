import csv
import os
import re
import statistics
from pathlib import Path

import pandas as pd


# Project folders
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
SOURCE_DIR = PROJECT_ROOT / "2_sample_data" / "source_original"
SAMPLE_DIR = PROJECT_ROOT / "2_sample_data"
METRICS_DIR = PROJECT_ROOT / "3_output_data" / "run_metrics"
VALIDATION_DIR = PROJECT_ROOT / "3_output_data" / "validation_reports"
ANALYSIS_DIR = PROJECT_ROOT / "3_output_data" / "analysis_ready"

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

CONDITIONS = [
    {
        "code": 1,
        "name": "Unencrypted",
        "folder": "unencrypted",
        "start": 1,
        "end": 10,
        "timing_file": "unencrypted_timing_results.csv",
        "validation_file": "unencrypted_validation_report.csv",
        "expected_exposure": 100.0,
    },
    {
        "code": 2,
        "name": "ECC",
        "folder": "ecc",
        "start": 11,
        "end": 25,
        "timing_file": "ecc_timing_results.csv",
        "validation_file": "ecc_validation_report.csv",
        "expected_exposure": 0.0,
    },
    {
        "code": 3,
        "name": "RSA-SHE",
        "folder": "rsa_she",
        "start": 26,
        "end": 40,
        "timing_file": "rsa_she_timing_results.csv",
        "validation_file": "rsa_she_validation_report.csv",
        "expected_exposure": 0.0,
    },
]

TIMING_COLUMNS = {
    "environment_id",
    "encryption_code",
    "encryption_type",
    "source_file",
    "output_file",
    "row_count",
    "column_count",
    "run_1_sec",
    "run_2_sec",
    "run_3_sec",
    "run_4_sec",
    "run_5_sec",
    "simulated_encryption_time_sec",
}

VALIDATION_COLUMNS = {
    "environment_id",
    "source_file",
    "output_file",
    "clear_text_exposure_percent",
    "status",
}


# Read the environment number

def get_environment_number(environment_id):
    match = re.fullmatch(r"ENV-(\d+)", str(environment_id).strip(), re.IGNORECASE)
    if not match:
        raise ValueError(f"Invalid environment ID: {environment_id}")
    return int(match.group(1))


# Load a required CSV file

def load_csv(file_path, required_columns):
    if not file_path.is_file():
        raise FileNotFoundError(f"Required file not found: {file_path}")

    dataframe = pd.read_csv(file_path, keep_default_na=False)
    missing_columns = required_columns.difference(dataframe.columns)
    if missing_columns:
        names = ", ".join(sorted(missing_columns))
        raise ValueError(f"{file_path.name} is missing columns: {names}")
    if dataframe.empty:
        raise ValueError(f"{file_path.name} does not contain records")

    return dataframe


# Check one transmission CSV

def load_transmission(file_path):
    if not file_path.is_file():
        raise FileNotFoundError(f"Transmission file not found: {file_path}")

    dataframe = pd.read_csv(file_path, dtype=str, keep_default_na=False)
    if list(dataframe.columns) != PROTECTED_COLUMNS:
        raise ValueError(f"{file_path.name} has an invalid column structure")
    if dataframe.empty:
        raise ValueError(f"{file_path.name} does not contain data rows")
    if dataframe.isna().any().any():
        raise ValueError(f"{file_path.name} contains missing values")

    return dataframe


# Measure the average CSV data-row length in bytes

def average_row_length_bytes(file_path, expected_rows):
    with file_path.open("r", encoding="utf-8", newline="") as csv_file:
        rows = list(csv.reader(csv_file))

    if len(rows) != expected_rows + 1:
        raise ValueError(f"{file_path.name} has an unexpected CSV row count")

    data_lengths = []
    with file_path.open("rb") as binary_file:
        lines = binary_file.read().splitlines()

    if len(lines) != expected_rows + 1:
        raise ValueError(f"{file_path.name} contains embedded or missing line breaks")

    for line in lines[1:]:
        data_lengths.append(len(line))

    if not data_lengths:
        raise ValueError(f"{file_path.name} does not contain measurable data rows")

    return sum(data_lengths) / len(data_lengths)


# Calculate clear-text exposure across all nine columns

def calculate_exposure(source_dataframe, output_dataframe):
    if len(source_dataframe) != len(output_dataframe):
        raise ValueError("Source and output row counts do not match")

    source_values = source_dataframe.to_numpy(dtype=str)
    output_values = output_dataframe.to_numpy(dtype=str)
    unchanged_values = int((source_values == output_values).sum())
    total_values = int(source_values.size)

    return (unchanged_values / total_values) * 100


# Check timing values and return the recorded median

def validate_timing(timing_row, condition):
    run_values = [
        float(timing_row[f"run_{run_number}_sec"])
        for run_number in range(1, 6)
    ]
    recorded_time = float(timing_row["simulated_encryption_time_sec"])
    calculated_median = statistics.median(run_values)

    if abs(recorded_time - calculated_median) > 0.000000001:
        raise ValueError(
            f"{timing_row['environment_id']} does not contain the five-run median"
        )

    if condition["code"] == 1:
        if any(value != 0 for value in run_values) or recorded_time != 0:
            raise ValueError("Unencrypted timing values must be zero")
    elif any(value <= 0 for value in run_values) or recorded_time <= 0:
        raise ValueError("Encrypted timing values must be greater than zero")

    return recorded_time


# Write a CSV without leaving a partial file

def write_csv(dataframe, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = output_path.with_suffix(".tmp")
    dataframe.to_csv(temporary_path, index=False)
    os.replace(temporary_path, output_path)


# Process one encryption condition

def process_condition(condition):
    timing_path = METRICS_DIR / condition["timing_file"]
    validation_path = VALIDATION_DIR / condition["validation_file"]
    output_dir = SAMPLE_DIR / condition["folder"]

    timing_data = load_csv(timing_path, TIMING_COLUMNS)
    validation_data = load_csv(validation_path, VALIDATION_COLUMNS)

    expected_ids = {
        f"ENV-{number:02d}"
        for number in range(condition["start"], condition["end"] + 1)
    }
    timing_ids = set(timing_data["environment_id"].astype(str))
    validation_ids = set(validation_data["environment_id"].astype(str))

    if timing_data["environment_id"].duplicated().any():
        raise ValueError(f"{timing_path.name} contains duplicate environments")
    if validation_data["environment_id"].duplicated().any():
        raise ValueError(f"{validation_path.name} contains duplicate environments")
    if timing_ids != expected_ids:
        raise ValueError(f"{timing_path.name} does not contain the expected environments")
    if validation_ids != expected_ids:
        raise ValueError(
            f"{validation_path.name} does not contain the expected environments"
        )

    validation_lookup = validation_data.set_index("environment_id")
    analysis_records = []
    audit_records = []

    for _, timing_row in timing_data.iterrows():
        environment_id = str(timing_row["environment_id"])
        environment_number = get_environment_number(environment_id)

        if not condition["start"] <= environment_number <= condition["end"]:
            raise ValueError(f"{environment_id} is assigned to the wrong condition")
        if int(timing_row["encryption_code"]) != condition["code"]:
            raise ValueError(f"{environment_id} has an invalid encryption code")
        if str(timing_row["encryption_type"]) != condition["name"]:
            raise ValueError(f"{environment_id} has an invalid encryption type")

        validation_row = validation_lookup.loc[environment_id]
        if str(validation_row["status"]).upper() != "PASS":
            raise ValueError(f"{environment_id} did not pass source validation")
        if str(validation_row["source_file"]) != str(timing_row["source_file"]):
            raise ValueError(f"{environment_id} source filenames do not match")
        if str(validation_row["output_file"]) != str(timing_row["output_file"]):
            raise ValueError(f"{environment_id} output filenames do not match")

        source_path = SOURCE_DIR / str(timing_row["source_file"])
        output_path = output_dir / str(timing_row["output_file"])
        source_dataframe = load_transmission(source_path)
        output_dataframe = load_transmission(output_path)

        expected_row_count = int(timing_row["row_count"])
        expected_column_count = int(timing_row["column_count"])
        if len(source_dataframe) != expected_row_count:
            raise ValueError(f"{environment_id} source row count does not match")
        if len(output_dataframe) != expected_row_count:
            raise ValueError(f"{environment_id} output row count does not match")
        if expected_column_count != len(PROTECTED_COLUMNS):
            raise ValueError(f"{environment_id} column count does not match")

        recorded_time = validate_timing(timing_row, condition)
        file_size_bytes = output_path.stat().st_size
        if file_size_bytes <= 0:
            raise ValueError(f"{environment_id} output file is empty")

        average_length = average_row_length_bytes(output_path, expected_row_count)
        exposure = calculate_exposure(source_dataframe, output_dataframe)
        recorded_exposure = float(validation_row["clear_text_exposure_percent"])

        if abs(exposure - recorded_exposure) > 0.000001:
            raise ValueError(f"{environment_id} clear-text exposure does not match")
        if abs(exposure - condition["expected_exposure"]) > 0.000001:
            raise ValueError(f"{environment_id} has an unexpected clear-text exposure")

        analysis_records.append(
            {
                "environment_id": environment_id,
                "encryption_code": condition["code"],
                "encryption_type": condition["name"],
                "file_size_kb": round(file_size_bytes / 1024, 6),
                "average_row_length_bytes": round(average_length, 6),
                "simulated_encryption_time_sec": round(recorded_time, 9),
                "clear_text_exposure_percent": round(exposure, 6),
                "row_count": expected_row_count,
                "column_count": expected_column_count,
                "source_file": source_path.name,
                "output_file": output_path.name,
            }
        )

        audit_records.append(
            {
                "environment_id": environment_id,
                "encryption_code": condition["code"],
                "encryption_type": condition["name"],
                "source_file_found": True,
                "output_file_found": True,
                "row_count_valid": True,
                "column_order_valid": True,
                "timing_median_valid": True,
                "file_size_bytes": file_size_bytes,
                "average_row_length_bytes": round(average_length, 6),
                "clear_text_exposure_percent": round(exposure, 6),
                "expected_exposure_percent": condition["expected_exposure"],
                "status": "PASS",
            }
        )

    return analysis_records, audit_records


# Combine all conditions

def main():
    try:
        analysis_records = []
        audit_records = []

        for condition in CONDITIONS:
            condition_analysis, condition_audit = process_condition(condition)
            analysis_records.extend(condition_analysis)
            audit_records.extend(condition_audit)

        analysis_data = pd.DataFrame(analysis_records)
        audit_data = pd.DataFrame(audit_records)

        analysis_data["environment_number"] = analysis_data["environment_id"].map(
            get_environment_number
        )
        analysis_data = analysis_data.sort_values("environment_number").drop(
            columns="environment_number"
        )
        audit_data["environment_number"] = audit_data["environment_id"].map(
            get_environment_number
        )
        audit_data = audit_data.sort_values("environment_number").drop(
            columns="environment_number"
        )

        if len(analysis_data) != 40:
            raise ValueError("The analysis dataset must contain 40 environments")
        if analysis_data["environment_id"].duplicated().any():
            raise ValueError("The analysis dataset contains duplicate environments")
        if analysis_data["output_file"].duplicated().any():
            raise ValueError("The analysis dataset contains duplicate output files")

        group_counts = analysis_data.groupby("encryption_code").size().to_dict()
        if group_counts != {1: 10, 2: 15, 3: 15}:
            raise ValueError("The encryption group counts are incorrect")

        write_csv(
            analysis_data,
            ANALYSIS_DIR / "iomt_encryption_analysis_ready.csv",
        )
        write_csv(
            audit_data,
            VALIDATION_DIR / "combined_metrics_validation_report.csv",
        )

        print("Completed 40 environments")
        return 0
    except Exception as error:
        print(f"Metric collection stopped: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
