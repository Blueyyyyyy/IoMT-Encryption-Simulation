# Output Data

This folder contains the measurement results, validation reports, and final analysis-ready dataset produced by the Version 2 IoMT Encryption Simulation.

## analysis_ready

This folder contains the final combined dataset used for statistical analysis.

### iomt_encryption_analysis_ready.csv

Contains all 40 study environments combined into one analysis-ready dataset.

For each environment, the dataset includes:

- Encryption condition and condition code
- Output file size in kilobytes
- Average row length in bytes
- Simulated encryption time in seconds
- Clear-text exposure percentage
- Row and column counts
- Associated source and output filenames

The dataset contains 10 unencrypted environments, 15 simulated ECC environments, and 15 RSA-SHE environments.

This is the primary dataset used for the final statistical analysis.

## run_metrics

This folder contains the timing measurements produced separately for each experimental condition.

### unencrypted_timing_results.csv

Contains timing results for ENV-01 through ENV-10.

Because no encryption operation occurs in the unencrypted baseline condition, all five timing runs and the retained simulated encryption time are recorded as 0 seconds.

### ecc_timing_results.csv

Contains timing results for ENV-11 through ENV-25.

Each environment includes five measured ECC encryption runs and the retained median simulated encryption time. Timing was measured using Python's `time.perf_counter()` after one untimed warm-up run.

### rsa_she_timing_results.csv

Contains timing results for ENV-26 through ENV-40.

Each environment includes five measured RSA-SHE runs, the retained median simulated encryption time, and the run number associated with the retained median result.

The file also includes diagnostic timings for the major stages of the RSA-SHE workflow:

- RSA key generation
- Homomorphic setup
- RSA encryption stage
- Hybrid randomizing layer
- Encrypted MAP-numerator evaluation
- Encrypted output-structure construction

These diagnostic stage timings are provided for reproducibility and validation and were not analyzed as separate primary dependent variables.

## validation_reports

This folder contains the validation records used to confirm that the generated outputs and measurements were produced correctly.

### unencrypted_validation_report.csv

Confirms that the unencrypted outputs match the original source data, preserve the expected row and column structure, contain no missing values, and maintain 100% clear-text exposure.

### ecc_validation_report.csv

Confirms that the simulated ECC outputs preserve the expected structure, contain valid encrypted values, successfully decrypt back to the original protected values, and produce 0% clear-text exposure.

### rsa_she_validation_report.csv

Contains the post-timing validation results for the RSA-SHE condition.

The report confirms:

- Expected row and column structure
- No missing values
- 0% clear-text exposure
- Valid serialized RSA-sized ciphertext
- Correct hybrid ciphertext construction for every protected value
- Sampled decrypt/unmask round-trip recovery across all nine protected fields
- Successful encrypted MAP-numerator validation for every source row
- The predefined encrypted operation `SBP + 2(DBP)`
- MAP division occurring only after validation decryption
- Valid homomorphic encoding range and arithmetic bounds
- 2048-bit RSA key size
- RSA public exponent of 65537
- Overall PASS status for each RSA-SHE environment

### combined_metrics_validation_report.csv

Provides the final validation summary across all 40 study environments.

The report verifies:

- Source and generated output availability
- Environment assignments
- Row and column structure
- All five recorded timing runs
- Five-run median timing
- File-size measurements
- Average row-length measurements
- Clear-text exposure
- Expected exposure by experimental condition
- Overall validation status

For RSA-SHE environments, the combined report also preserves the final diagnostic evidence for the RSA-SHE workflow, including stage timings, hybrid ciphertext checks, sampled decrypt/unmask checks, encrypted MAP-numerator validation, encoding and arithmetic checks, and RSA parameter verification.

Together, these files provide the measurement data, validation evidence, and final analysis-ready dataset used to support the statistical analysis reported in the dissertation.
