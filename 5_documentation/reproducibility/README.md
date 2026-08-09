# Version 2 Reproducibility Instructions

## Purpose

This document describes how to reproduce the final Version 2 analysis for the IoMT Encryption Simulation study.

The study used 40 simulated always-operating Internet of Medical Things (IoMT) environments divided across three experimental conditions:

- Unencrypted: ENV-01 through ENV-10
- Simulated ECC: ENV-11 through ENV-25
- RSA-SHE: ENV-26 through ENV-40

RSA-SHE refers to the RSA-based simulated homomorphic encryption condition evaluated in the study.

RSA-SHE used a controlled 2048-bit RSA-based hybrid simulated-homomorphic construction. It protected all nine transmission fields and performed the predefined encrypted MAP-numerator calculation `SBP + 2(DBP)` before validation decryption. Division by three to complete the MAP calculation occurred only after validation decryption.

RSA-SHE was a controlled simulated-homomorphic adaptation for this predefined operation. It was not a production-grade Fully Homomorphic Encryption implementation, was not an exact reproduction of MEHE, and did not support arbitrary ciphertext computation.

The study used synthetic data only. No real patient data, Protected Health Information (PHI), Personally Identifiable Information (PII), physical medical devices, or live healthcare networks were used.

## Repository Version

Use the final Version 2 repository contents from the `main` branch.

Superseded Version 1 scripts, outputs, and statistical analyses are retained under `Legacy/Version1/` for historical reference and should not be used to reproduce the final dissertation results.

The repository structure includes:

```text
IoMT-Encryption-Simulation/
├── 1_python_scripts/
├── 2_sample_data/
│   └── source_original/
├── 3_output_data/
│   ├── analysis_ready/
│   ├── run_metrics/
│   └── validation_reports/
├── 4_spss_outputs/
│   ├── exported_report/
│   ├── output/
│   └── syntax/
├── 5_documentation/
│   ├── citations/
│   ├── license/
│   ├── repository_configuration/
│   ├── reproducibility/
│   ├── requirements/
│   └── variable_dictionary/
├── Legacy/
│   └── Version1/
├── .gitignore
├── CITATION.cff
├── citation.bib
├── LICENSE
├── README.md
└── requirements.txt
```

Software Environment

The final Version 2 timing measurements were produced using:

Microsoft Windows 11 Home, 64-bit
Windows version 10.0.26200
Python 3.11.0
cryptography 45.0.4
pandas 2.3.0
IBM SPSS Statistics for statistical analysis

The test computer used:

Intel Core i9-9900K
3.60 GHz base clock speed
Approximately 16 GB physical memory

The same computer and software environment were used for all timed runs.

Exact encryption timing values may differ when the workflow is reproduced on different hardware or software environments.

Clone the Repository

Clone the repository and enter the project directory:

git clone https://github.com/Blueyyyyyy/IoMT-Encryption-Simulation.git
cd IoMT-Encryption-Simulation
git checkout main
Create a Python Virtual Environment

Create the environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

Install the required packages:

python -m pip install --upgrade pip
pip install -r requirements.txt

The root-level requirements.txt contains:

pandas==2.3.0
cryptography==45.0.4
Source Data

The original synthetic source CSV files are stored in:

2_sample_data/source_original/

The source files are named:

simulated_ENV-01.csv
through
simulated_ENV-40.csv

The condition assignments are fixed:

Environment Range	Condition	n
ENV-01 through ENV-10	Unencrypted	10
ENV-11 through ENV-25	Simulated ECC	15
ENV-26 through ENV-40	RSA-SHE	15

The original source files should not be modified when reproducing the study.

Protected Transmission Fields

The source CSV files contain nine protected transmission fields:

org_id
device_id
timestamp
heart_rate
bp_systolic
bp_diastolic
spo2
temperature
battery_level

All values under these nine fields are protected under the simulated ECC and RSA-SHE conditions.

Column headings are not treated as protected values. Row counts and column order are retained.

Generated Condition Data

The condition-specific transmission outputs are generated locally when the Python scripts are run.

They are written to:

2_sample_data/unencrypted/
2_sample_data/ecc/
2_sample_data/rsa_she/

These generated folders are excluded from GitHub by .gitignore because of their combined file size. They are recreated during reproduction from the 40 source CSV files.

The resulting measurement data and validation evidence are retained in 3_output_data/.

Unencrypted Condition

ENV-01 through ENV-10 form the unencrypted baseline.

The script used is:

1_python_scripts/unencrypted_baseline.py

No encryption operation is performed. The source data are copied without changing the protected values.

The condition records:

simulated_encryption_time_sec = 0
clear_text_exposure_percent = 100

Five timing fields are also recorded as 0 seconds because no encryption operation occurs.

Generated outputs are written locally as:

2_sample_data/unencrypted/unencrypted_ENV-01.csv
through
2_sample_data/unencrypted/unencrypted_ENV-10.csv
Simulated ECC Condition

ENV-11 through ENV-25 form the simulated ECC condition.

The script used is:

1_python_scripts/ecc_encrypt.py

The final implementation uses:

Elliptic Curve Diffie-Hellman (ECDH)
SECP384R1
HKDF-SHA256
256-bit derived AES key
AES-256-GCM
Fresh 12-byte nonce for every protected-value encryption operation
Base64-encoded encrypted output

ECDH establishes shared key material, HKDF-SHA256 derives the AES key, and AES-256-GCM encrypts all nine protected fields.

One untimed warm-up run is completed before five timed runs. The median of the five measured runs is retained as simulated_encryption_time_sec.

Post-timing validation decrypts every encrypted protected value and confirms that it matches the original source value.

The expected clear-text exposure is:

clear_text_exposure_percent = 0

Generated outputs are written locally as:

2_sample_data/ecc/ecc_encrypted_ENV-11.csv
through
2_sample_data/ecc/ecc_encrypted_ENV-25.csv
RSA-SHE Condition

ENV-26 through ENV-40 form the RSA-SHE condition.

The script used is:

1_python_scripts/rsa_she_encrypt.py

The final implementation uses:

2048-bit RSA
RSA public exponent 65537
A new RSA key pair for each run
A run-specific exponent-encoding base for bp_systolic and bp_diastolic
Reversible integer encoding for the remaining protected fields
RSA modular encryption of all nine protected fields
A fresh randomized hybrid layer for every protected value
Fixed-width Base64 serialization of RSA-sized ciphertext
A predefined encrypted MAP-numerator calculation

The randomized hybrid construction follows the controlled relationship:

H = RSA(encoded) * RSA(r) mod n

where r is a fresh random invertible mask.

The predefined encrypted healthcare calculation is:

SBP + 2(DBP)

The systolic and diastolic operands remain encrypted during this operation.

Division by three to complete the MAP calculation is performed only after validation decryption and is not part of the encrypted-domain operation.

One untimed warm-up run is completed before five timed runs. The median of those five measured runs is retained as simulated_encryption_time_sec.

RSA-SHE is not:

Production-grade FHE
An exact reproduction of Kamatchi and Kumari's MEHE implementation
A general-purpose homomorphic encryption scheme
A scheme supporting arbitrary ciphertext computation

Generated outputs are written locally as:

2_sample_data/rsa_she/rsa_she_encrypted_ENV-26.csv
through
2_sample_data/rsa_she/rsa_she_encrypted_ENV-40.csv

The expected clear-text exposure is:

clear_text_exposure_percent = 0
Encryption Timing Procedure

Python's time.perf_counter() is used to measure actual elapsed processing time.

For both encrypted conditions:

Load and structurally validate the source CSV before timing begins.
Perform one untimed warm-up run.
Perform five timed runs.
Generate fresh run-specific cryptographic material.
Retain the median of the five timed runs as simulated_encryption_time_sec.
Perform correctness and exposure validation after the measured cryptographic workflow.

For simulated ECC, the measured workflow includes key generation, ECDH shared-secret establishment, HKDF key derivation, encryption of all nine protected fields, and creation of the encrypted in-memory output structure.

For RSA-SHE, timing begins immediately before run-specific RSA key generation and includes:

RSA key generation
Homomorphic setup and run-specific exponent-base generation
Encoding and RSA modular encryption of all nine protected fields
Randomized hybrid ciphertext construction
Encrypted MAP-numerator evaluation
Construction of the encrypted in-memory transmission structure

The RSA-SHE timer stops before:

Correctness-validation decryption or unmasking
MAP-result verification
Clear-text-exposure checks
Validation and audit-report generation
Disk writing
File-size measurement
Average-row-length measurement

A new RSA key pair, homomorphic base, and fresh random masks are generated for every RSA-SHE run.

Fresh cryptographic material and a new AES-GCM nonce for every protected-value encryption operation are generated during simulated ECC runs.

No artificial latency, sleep() commands, or manually assigned encryption-time values are used.

The unencrypted condition is recorded as 0 seconds because no encryption operation is performed.

RSA-SHE Diagnostic Timing

The file:

3_output_data/run_metrics/rsa_she_timing_results.csv

also preserves diagnostic timing information for the median RSA-SHE run.

The diagnostic variables are:

median_run_number
median_rsa_keygen_time_sec
median_homomorphic_setup_time_sec
median_rsa_stage_time_sec
median_homomorphic_layer_time_sec
median_evaluation_time_sec
median_structure_time_sec

These values support reproducibility and validation. They are not additional primary SPSS dependent variables.

Clear-Text Exposure

Clear-text exposure is calculated across all data cells under the nine protected transmission fields.

The metric compares each generated protected value with the corresponding source value:

clear-text exposure (%) =
(unchanged protected values / total protected values) × 100

Column headings are excluded.

Expected results are:

Condition	Expected Clear-Text Exposure
Unencrypted	100%
Simulated ECC	0%
RSA-SHE	0%
Recommended Python Run Order

Run the scripts from the repository root in this order:

python 1_python_scripts/unencrypted_baseline.py
python 1_python_scripts/ecc_encrypt.py
python 1_python_scripts/rsa_she_encrypt.py
python 1_python_scripts/collect_metrics.py

The first three scripts create the condition-specific transmission outputs, timing records, and validation reports.

collect_metrics.py must be run last because it validates the complete experimental output and creates the final analysis-ready dataset.

Analysis-Ready Dataset

The final dataset is:

3_output_data/analysis_ready/iomt_encryption_analysis_ready.csv

It contains the following exact variable names:

environment_id
encryption_code
encryption_type
file_size_kb
average_row_length_bytes
simulated_encryption_time_sec
clear_text_exposure_percent
row_count
column_count
source_file
output_file

The four primary measured outcomes are:

file_size_kb
average_row_length_bytes
simulated_encryption_time_sec
clear_text_exposure_percent

The remaining fields identify the environment, experimental condition, source and output files, and transmission structure.

Complete variable definitions are documented in:

5_documentation/variable_dictionary/variable_dictionary.txt
Timing and Validation Files

Condition-specific timing files are stored in:

3_output_data/run_metrics/unencrypted_timing_results.csv
3_output_data/run_metrics/ecc_timing_results.csv
3_output_data/run_metrics/rsa_she_timing_results.csv

Validation reports are stored in:

3_output_data/validation_reports/unencrypted_validation_report.csv
3_output_data/validation_reports/ecc_validation_report.csv
3_output_data/validation_reports/rsa_she_validation_report.csv
3_output_data/validation_reports/combined_metrics_validation_report.csv
Validation Checks
Unencrypted

The validation process confirms:

Row count and column order are preserved
No values are missing
Every protected value matches the original source value
Clear-text exposure equals 100%
Simulated ECC

The validation process confirms:

Row count and column order are preserved
No values are missing
All nine protected fields contain encrypted values
Every encrypted protected value successfully decrypts to its original source value
Clear-text exposure equals 0%
RSA-SHE

Post-timing RSA-SHE validation confirms:

Row count and column order are preserved
No values are missing
All nine protected fields contain serialized RSA-sized ciphertext
Every hybrid ciphertext matches the expected public-key construction
A deterministic sample of up to 12 rows is decrypted and unmasked across all nine protected fields
The encrypted MAP-numerator operation is validated for every source row
The encrypted operation is exactly SBP + 2(DBP)
Division by three occurs only after validation decryption
The run-specific exponent base remains valid over the required MAP range
Arithmetic bounds remain valid
RSA key size equals 2048 bits
RSA public exponent equals 65537
Clear-text exposure equals 0%

A failed required validation causes processing to stop rather than silently accept an invalid environment.

Combined Metrics Validation

collect_metrics.py independently confirms:

Expected 10/15/15 group assignments
Source and generated output availability
Row and column structure
Five timing runs
Correct five-run median
File-size measurements
Average-row-length measurements
Clear-text exposure
RSA-SHE diagnostic timing and validation information
Final total of 40 analysis-ready environments
SPSS Statistical Analysis

The final SPSS syntax file is:

4_spss_outputs/syntax/SPSS_final_analysis.sps

The final SPSS data file is:

4_spss_outputs/output/iomt_encryption_final_data.sav

The final native SPSS output is:

4_spss_outputs/output/SPSS_final_analysis.spv

The exported final report is:

4_spss_outputs/exported_report/SPSS_final_analysis.pdf

The SPSS syntax currently contains the original local Windows paths used during the final analysis. When reproducing the statistical analysis on another computer, update the file paths in SPSS_final_analysis.sps to point to the corresponding locations within the local repository clone before running the syntax.

The statistical procedures are described below.

File Size

Use:

Welch's one-way ANOVA
Games–Howell pairwise comparisons

Expected omnibus result:

F(2, 18.667) = 79.262, p < .001

All three file-size pairwise comparisons are statistically significant.

Average Row Length

Use:

Independent-samples Kruskal–Wallis test
Bonferroni-adjusted pairwise comparisons

Expected omnibus result:

H(2) = 38.334, p < .001

Expected adjusted pairwise results:

Unencrypted vs ECC:      p = .017
Unencrypted vs RSA-SHE:  p < .001
ECC vs RSA-SHE:          p = .001
Simulated Encryption Time

Use:

Independent-samples Kruskal–Wallis test
Bonferroni-adjusted pairwise comparisons

Expected omnibus result:

H(2) = 34.838, p < .001

Expected adjusted pairwise results:

Unencrypted vs ECC:      p = .025
Unencrypted vs RSA-SHE:  p < .001
ECC vs RSA-SHE:          p = .001
Clear-Text Exposure

Evaluate clear-text exposure descriptively.

No inferential ECC-versus-RSA-SHE comparison is conducted because both encrypted conditions contain:

0% clear-text exposure
0 within-group variation
Expected Descriptive Results

The final Version 2 descriptive results are:

Condition	n	File Size Mean KB	Average Row Length Mean Bytes	Encryption Time Mean Seconds	Clear-Text Exposure
Unencrypted	10	61.64150	61.02590	0.00000000	100%
ECC	15	1825.35319	428.00000	0.06475018	0%
RSA-SHE	15	35791.88965	3104.00000	32.24001641	0%

Standard deviations for the three performance measures are:

Condition	File Size SD	Average Row Length SD	Encryption Time SD
Unencrypted	0.005922	0.006064	0.000000000
ECC	1186.218687	0.000000	0.039775335
RSA-SHE	12089.403372	0.000000	11.560739492
Hypothesis Decisions
Research Question 1

Reject the null hypothesis.

RSA-SHE differed significantly from the unencrypted condition in the operationalized network-traffic measures of file size and average row length.

Research Question 2

Do not reject the null hypothesis.

Both simulated ECC and RSA-SHE produced 0% clear-text exposure. RSA-SHE was not shown to improve the measured confidentiality outcome beyond simulated ECC.

Research Question 3

Reject the null hypothesis for the three operationalized performance measures.

RSA-SHE differed significantly from simulated ECC in:

File size
Average row length
Simulated encryption time

RSA-SHE produced the larger values for all three measured performance outcomes.

Interpretation Boundary

Successful reproduction of these results demonstrates reproduction of the controlled Version 2 simulation, RSA-SHE predefined encrypted MAP-numerator workload, and statistical analysis.

It does not establish:

Production-grade FHE performance
General-purpose or arbitrary homomorphic computation capability
Real-world IoMT device execution times
Physical-device power or battery consumption
Post-quantum security or quantum resistance
Protection against malware
Protection against denial-of-service attacks
Protection against compromised endpoints
Real-world healthcare deployment performance

The findings apply to the tested implementations, documented test computer, and controlled simulated environment.
