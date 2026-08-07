import os
import re
from pathlib import Path

import pandas as pd


# Project folders
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
SOURCE_DIR = PROJECT_ROOT / "2_sample_data" / "source_original"
OUTPUT_DIR = PROJECT_ROOT / "2_sample_data" / "unencrypted"
METRICS_DIR = PROJECT_ROOT / "3_output_data" / "run_metrics"
VALIDATION_DIR = PROJECT_ROOT / "3_output_data" / "validation_reports"

# Study settings
ENVIRONMENT_START = 1
ENVIRONMENT_END = 10
TIMED_RUNS = 5

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


# Find one source file for each baseline environment
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


# Check that the baseline remains unchanged
def validate_output(source_dataframe, output_dataframe):
    if list(output_dataframe.columns) != PROTECTED_COLUMNS:
        raise ValueError("Baseline columns do not match the source columns")
    if len(output_dataframe) != len(source_dataframe):
        raise ValueError("Baseline row count does not match the source row count")
    if output_dataframe.isna().any().any():
        raise ValueError("Baseline output contains missing values")

    source_values = source_dataframe.to_numpy(dtype=str)
    output_values = output_dataframe.to_numpy(dtype=str)
    unchanged_values = int((source_values == output_values).sum())
    total_values = int(source_values.size)
    exposure = (unchanged_values / total_values) * 100

    if unchanged_values != total_values or exposure != 100:
        raise ValueError("Unencrypted output does not match the source data")

    return {
        "row_count_valid": True,
        "column_order_valid": True,
        "missing_values": 0,
        "protected_values": total_values,
        "unchanged_values": unchanged_values,
        "clear_text_exposure_percent": exposure,
        "source_match_valid": True,
    }


# Write a CSV without leaving a partial file
def write_csv(dataframe, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = output_path.with_suffix(".tmp")
    dataframe.to_csv(temporary_path, index=False)
    os.replace(temporary_path, output_path)


# Process one environment
def process_environment(environment_number, source_path):
    source_dataframe = load_source_file(source_path)
    output_dataframe = source_dataframe.copy(deep=True)
    validation = validate_output(source_dataframe, output_dataframe)

    environment_id = f"ENV-{environment_number:02d}"
    output_filename = f"unencrypted_{environment_id}.csv"
    write_csv(output_dataframe, OUTPUT_DIR / output_filename)

    metrics = {
        "environment_id": environment_id,
        "encryption_code": 1,
        "encryption_type": "Unencrypted",
        "source_file": source_path.name,
        "output_file": output_filename,
        "row_count": len(source_dataframe),
        "column_count": len(source_dataframe.columns),
    }
    for run_number in range(1, TIMED_RUNS + 1):
        metrics[f"run_{run_number}_sec"] = 0.0
    metrics["simulated_encryption_time_sec"] = 0.0

    validation_record = {
        "environment_id": environment_id,
        "source_file": source_path.name,
        "output_file": output_filename,
        **validation,
        "status": "PASS",
    }

    print(f"{environment_id}: 0.000000 seconds")
    return metrics, validation_record


# Run all unencrypted environments
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
            METRICS_DIR / "unencrypted_timing_results.csv",
        )
        write_csv(
            pd.DataFrame(validation_records),
            VALIDATION_DIR / "unencrypted_validation_report.csv",
        )

        print(f"Completed {len(metrics_records)} environments")
        return 0
    except Exception as error:
        print(f"Unencrypted baseline stopped: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
