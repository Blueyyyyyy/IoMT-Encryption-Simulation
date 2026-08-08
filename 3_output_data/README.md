# Output Data

This folder contains the measurement results, validation reports, and final analysis-ready dataset produced by the Version 2 IoMT Encryption Simulation.

## analysis_ready

This folder contains the final combined dataset used for statistical analysis.

### iomt_encryption_analysis_ready.csv

Contains all 40 study environments combined into one analysis-ready dataset. It includes the encryption condition, file size, average row length, simulated encryption time, clear-text exposure, row and column counts, and associated source/output filenames.

This is the primary dataset used for the final statistical analysis.

## run_metrics

This folder contains the timing measurements produced separately for each experimental condition.

### unencrypted_timing_results.csv

Contains timing results for ENV-01 through ENV-10. Because no encryption operation occurs in the baseline condition, all five timing runs and the retained encryption time are 0 seconds.

### ecc_timing_results.csv

Contains timing results for ENV-11 through ENV-25. Each environment includes five ECC encryption timing runs and the retained median encryption time.

### rsa_she_timing_results.csv

Contains timing results for ENV-26 through ENV-40. Each environment includes five RSA-SHE encryption timing runs and the retained median encryption time.

## validation_reports

This folder contains the validation records used to confirm that the generated outputs and measurements were produced correctly.

### unencrypted_validation_report.csv

Confirms that the unencrypted outputs match the original source data, preserve the expected structure, contain no missing values, and maintain 100% clear-text exposure.

### ecc_validation_report.csv

Confirms that the ECC outputs preserve the expected structure, contain valid ciphertext, successfully decrypt back to the original values, and produce 0% clear-text exposure.

### rsa_she_validation_report.csv

Confirms that the RSA-SHE outputs preserve the expected structure, contain valid RSA ciphertext, and produce 0% clear-text exposure.

### combined_metrics_validation_report.csv

Provides the final validation summary across all 40 study environments. It verifies source and output availability, row counts, column structure, timing medians, file-size measurements, average row lengths, clear-text exposure, and overall validation status.

Together, these folders provide the Version 2 measurement data and validation evidence used to support the final dissertation analysis.
