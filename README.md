# IoMT Encryption Simulation

## Version 2

This repository contains the Python scripts, synthetic source data, measurement results, validation evidence, SPSS analysis files, and supporting documentation used for my doctoral dissertation:

**Examining Simulated Homomorphic Encryption on Data Transmissions of Always-Operating Internet of Medical Things**

Version 2 contains the final implementation, analysis, validation, and interpretation used for the dissertation.

The study compared three experimental conditions:

- Unencrypted transmissions
- Simulated Elliptic Curve Cryptography (ECC)
- RSA-based simulated homomorphic encryption condition (RSA-SHE)

RSA-SHE was implemented as a controlled 2048-bit RSA-based hybrid simulated-homomorphic adaptation. It protected all nine transmission fields and supported the predefined encrypted MAP-numerator calculation `SBP + 2(DBP)` before validation decryption.

Division by three to complete the MAP calculation occurred only after validation decryption.

RSA-SHE was not a production-grade Fully Homomorphic Encryption (FHE) implementation, was not an exact reproduction of MEHE, and did not support arbitrary ciphertext computation.

Superseded Version 1 files are retained under `Legacy/Version1/` for research transparency and should not be used as the final analytical results of the study.

## Study Design

The study used a controlled Python-based simulation consisting of 40 simulated always-operating Internet of Medical Things (IoMT) environments.

| Encryption Condition | n |
| --- | ---: |
| Unencrypted | 10 |
| Simulated ECC | 15 |
| RSA-SHE | 15 |
| **Total** | **40** |

Environment assignments were fixed:

- ENV-01 through ENV-10: Unencrypted
- ENV-11 through ENV-25: Simulated ECC
- ENV-26 through ENV-40: RSA-SHE

Synthetic data were used throughout the experiment.

No real patient data, Protected Health Information (PHI), Personally Identifiable Information (PII), physical medical devices, or live healthcare networks were used.

The simulation evaluated implementation-specific differences in operational performance and clear-text exposure under controlled conditions.

## Protected Transmission Fields

The source CSV files contain nine protected transmission fields:

```text
org_id
device_id
timestamp
heart_rate
bp_systolic
bp_diastolic
spo2
temperature
battery_level
```

All values under these nine fields were protected under the simulated ECC and RSA-SHE conditions.

Column headings were excluded from the clear-text exposure calculation.

## Encryption Conditions

### Unencrypted

ENV-01 through ENV-10 form the unencrypted baseline.

The script used is:

```text
1_python_scripts/unencrypted_baseline.py
```

No encryption operation is performed. The protected values remain unchanged from the original synthetic source data.

The condition records:

```text
simulated_encryption_time_sec = 0
clear_text_exposure_percent = 100
```

### Simulated ECC

ENV-11 through ENV-25 form the simulated ECC condition.

The script used is:

```text
1_python_scripts/ecc_encrypt.py
```

The implementation uses:

- Elliptic Curve Diffie-Hellman (ECDH)
- SECP384R1
- HKDF-SHA256
- 256-bit derived AES key
- AES-256-GCM
- Fresh 12-byte nonce for each protected-value encryption operation
- Base64-encoded encrypted output

ECDH establishes shared key material, HKDF-SHA256 derives the AES key, and AES-256-GCM encrypts all nine protected fields.

Post-timing validation decrypts the encrypted protected values and confirms that they match the original source values.

The simulated ECC condition produced:

```text
clear_text_exposure_percent = 0
```

### RSA-SHE

ENV-26 through ENV-40 form the RSA-based simulated homomorphic encryption condition.

The script used is:

```text
1_python_scripts/rsa_she_encrypt.py
```

The final RSA-SHE implementation uses:

- 2048-bit RSA
- RSA public exponent 65537
- A new RSA key pair for each run
- Run-specific exponent encoding for the blood-pressure fields
- Reversible encoding for the remaining protected fields
- RSA modular encryption of all nine protected fields
- A randomized hybrid layer applied to every protected ciphertext
- Fixed-width Base64 serialization of RSA-sized ciphertext
- A predefined encrypted MAP-numerator calculation

The controlled randomized hybrid construction uses the relationship:

```text
H = RSA(encoded) * RSA(r) mod n
```

where `r` is a fresh random invertible mask.

The predefined encrypted healthcare calculation is:

```text
SBP + 2(DBP)
```

The systolic and diastolic blood-pressure values remain encrypted while this numerator operation is performed.

Division by three to complete the MAP calculation occurs only after validation decryption.

RSA-SHE does not:

- Implement production-grade FHE
- Reproduce a general-purpose homomorphic encryption scheme
- Support arbitrary ciphertext computation
- Exactly reproduce the MEHE implementation described in prior research
- Establish post-quantum security or quantum resistance

The RSA-SHE condition produced:

```text
clear_text_exposure_percent = 0
```

## Clear-Text Exposure

Clear-text exposure was the measured confidentiality outcome.

The implementation calculates the percentage of protected output values that remain unchanged from the corresponding original source values:

```text
clear-text exposure (%) =
(unchanged protected values / total protected values) × 100
```

Column headings are excluded.

The final results were:

| Condition | Clear-Text Exposure |
| --- | ---: |
| Unencrypted | 100% |
| Simulated ECC | 0% |
| RSA-SHE | 0% |

Because both encrypted conditions produced 0% clear-text exposure, RSA-SHE did not demonstrate an additional measured confidentiality advantage over simulated ECC on this outcome.

## Primary Measured Outcomes

The study evaluated four primary outcomes.

### File Size

`file_size_kb`

Total size of the generated condition-specific transmission output in kilobytes.

File size was used as an indicator of encrypted data expansion and transmission or storage demand.

### Average Row Length

`average_row_length_bytes`

Average number of bytes contained in each data row of the generated transmission output.

Average row length was used as an indicator of transmission-record growth.

### Simulated Encryption Time

`simulated_encryption_time_sec`

Actual elapsed processing time, measured in seconds, required to complete the timed cryptographic workflow in the Python-based simulated environment.

Despite the variable name, this was not an artificial delay or modeled timing value. The measurements were actual elapsed times obtained with Python's `time.perf_counter()`.

### Clear-Text Exposure

`clear_text_exposure_percent`

Percentage of protected output values that remained unchanged from the corresponding source values.

## Encryption Timing Procedure

Python's `time.perf_counter()` was used to measure actual elapsed processing time.

For the two encrypted conditions:

1. The source CSV was loaded and structurally validated before timing began.
2. One untimed warm-up run was performed.
3. Five timed runs were performed.
4. Fresh condition-specific cryptographic material was generated for each run.
5. The complete protected dataset was encrypted.
6. The median of the five timed runs was retained as `simulated_encryption_time_sec`.
7. Correctness and clear-text-exposure validation occurred after the measured cryptographic workflow.

For simulated ECC, the timed workflow includes ECDH key generation and shared-secret establishment, HKDF-SHA256 key derivation, AES-256-GCM encryption of all nine protected fields, fresh nonce generation, and construction of the encrypted in-memory data structure.

For RSA-SHE, the timed interval includes:

- RSA key generation
- Run-specific homomorphic setup
- Encoding and RSA modular encryption of all nine protected fields
- Randomized hybrid ciphertext construction
- Predefined encrypted MAP-numerator evaluation
- Construction of the encrypted in-memory transmission structure

For RSA-SHE, timing stops before:

- Correctness-validation decryption and unmasking
- MAP-result verification
- Clear-text-exposure checks
- Validation and audit-report generation
- Disk writing
- File-size measurement
- Average-row-length measurement

No `sleep()` commands, artificial latency, or manually assigned encryption-time values were used.

The unencrypted condition is recorded as 0 seconds because no encryption operation occurs.

## Test Environment

All encryption timing was conducted using the same computer and software environment:

- Processor: Intel Core i9-9900K
- Base clock speed: 3.60 GHz
- Physical memory: approximately 16 GB
- Operating system: Microsoft Windows 11 Home, 64-bit
- Windows version: 10.0.26200
- Python: 3.11.0
- `cryptography`: 45.0.4
- `pandas`: 2.3.0

The measured encryption times are specific to the tested implementations and documented test computer.

They should not be interpreted as universal execution times for ECC, RSA, production-grade FHE, or physical IoMT devices.

## Version 2 Descriptive Results

| Encryption Condition | n | Mean File Size (KB) | Mean Average Row Length (Bytes) | Mean Encryption Time (s) | Clear-Text Exposure |
| --- | ---: | ---: | ---: | ---: | ---: |
| Unencrypted | 10 | 61.64150 | 61.02590 | 0.00000000 | 100% |
| Simulated ECC | 15 | 1825.35319 | 428.00000 | 0.06475018 | 0% |
| RSA-SHE | 15 | 35791.88965 | 3104.00000 | 32.24001641 | 0% |

RSA-SHE produced the largest mean file size, average row length, and simulated encryption time.

Simulated ECC produced intermediate values, while the unencrypted condition produced the smallest values.

Both encrypted conditions produced 0% clear-text exposure.

## Statistical Analysis

IBM SPSS Statistics was used for the final statistical analysis.

Homogeneity of variance was evaluated using Levene's test.

The final Levene results were:

| Outcome | F | df1 | df2 | p |
| --- | ---: | ---: | ---: | ---: |
| File size | 15.965 | 2 | 37 | < .001 |
| Average row length | 36.689 | 2 | 37 | < .001 |
| Simulated encryption time | 20.325 | 2 | 37 | < .001 |

Equal variances were therefore not supported for the three measured performance outcomes.

Outcome-specific robust or nonparametric procedures were used.

### File Size

File size was analyzed using:

- Welch's one-way ANOVA
- Games–Howell pairwise comparisons

The Welch omnibus result was:

```text
F(2, 18.667) = 79.262, p < .001
```

All three Games–Howell file-size comparisons were statistically significant at `p < .001`.

### Average Row Length

Average row length contained zero within-group variance in the encrypted groups.

It was analyzed using:

- Independent-samples Kruskal–Wallis test
- Bonferroni-adjusted pairwise comparisons

The omnibus result was:

```text
H(2) = 38.334, p < .001
```

Adjusted pairwise results were:

```text
Unencrypted vs ECC:      p = .017
Unencrypted vs RSA-SHE:  p < .001
ECC vs RSA-SHE:          p = .001
```

### Simulated Encryption Time

The unencrypted condition contained zero within-group variance because all encryption-time values were 0 seconds.

Simulated encryption time was analyzed using:

- Independent-samples Kruskal–Wallis test
- Bonferroni-adjusted pairwise comparisons

The omnibus result was:

```text
H(2) = 34.838, p < .001
```

Adjusted pairwise results were:

```text
Unencrypted vs ECC:      p = .025
Unencrypted vs RSA-SHE:  p < .001
ECC vs RSA-SHE:          p = .001
```

### Clear-Text Exposure

Clear-text exposure was evaluated descriptively.

An inferential ECC-versus-RSA-SHE comparison was not performed because both encrypted conditions produced:

```text
0% clear-text exposure
0 within-group variation
```

## Research Question Decisions

### Research Question 1

The null hypothesis was rejected.

RSA-SHE differed significantly from the unencrypted condition in the operationalized network-traffic measures of file size and average row length.

### Research Question 2

The null hypothesis was not rejected.

Simulated ECC and RSA-SHE both produced 0% clear-text exposure.

RSA-SHE was therefore not shown to improve the measured confidentiality outcome beyond simulated ECC.

### Research Question 3

The null hypothesis was rejected for the three operationalized performance measures.

RSA-SHE differed significantly from simulated ECC in:

- File size
- Average row length
- Simulated encryption time

RSA-SHE produced the larger values for all three measured performance outcomes.

Within the tested implementations, RSA-SHE introduced greater measured processing and transmission demands than simulated ECC without producing an additional advantage on the measured clear-text exposure outcome.

## Reproducing the Python Workflow

Install the required packages:

```text
pip install -r requirements.txt
```

Run the scripts from the repository root in this order:

```text
python 1_python_scripts/unencrypted_baseline.py
python 1_python_scripts/ecc_encrypt.py
python 1_python_scripts/rsa_she_encrypt.py
python 1_python_scripts/collect_metrics.py
```

The first three scripts generate the condition-specific transmission outputs, timing results, and validation reports.

`collect_metrics.py` runs last and validates the complete experiment before creating the final analysis-ready dataset.

## Generated Condition Data

The original 40 synthetic source CSV files are retained in:

```text
2_sample_data/source_original/
```

The condition-specific transmission outputs are generated locally in:

```text
2_sample_data/unencrypted/
2_sample_data/ecc/
2_sample_data/rsa_she/
```

These three generated folders are excluded from GitHub because of their combined file size.

They are recreated by running the condition-specific Python scripts.

The measurement results and validation evidence derived from the generated files are retained under `3_output_data/`.

## Final Analysis-Ready Dataset

The final analysis-ready dataset is:

```text
3_output_data/analysis_ready/iomt_encryption_analysis_ready.csv
```

Its exact variables are:

```text
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
```

The four primary study outcomes are:

```text
file_size_kb
average_row_length_bytes
simulated_encryption_time_sec
clear_text_exposure_percent
```

## Timing and Validation Files

Timing results:

```text
3_output_data/run_metrics/unencrypted_timing_results.csv
3_output_data/run_metrics/ecc_timing_results.csv
3_output_data/run_metrics/rsa_she_timing_results.csv
```

Validation reports:

```text
3_output_data/validation_reports/unencrypted_validation_report.csv
3_output_data/validation_reports/ecc_validation_report.csv
3_output_data/validation_reports/rsa_she_validation_report.csv
3_output_data/validation_reports/combined_metrics_validation_report.csv
```

## Final SPSS Files

Final SPSS syntax:

```text
4_spss_outputs/syntax/SPSS_final_analysis.sps
```

Final SPSS data file:

```text
4_spss_outputs/output/iomt_encryption_final_data.sav
```

Final native SPSS output:

```text
4_spss_outputs/output/SPSS_final_analysis.spv
```

Final exported SPSS report:

```text
4_spss_outputs/exported_report/SPSS_final_analysis.pdf
```

## Repository Structure

```text
IoMT-Encryption-Simulation/
├── 1_python_scripts/
│   ├── README.md
│   ├── collect_metrics.py
│   ├── ecc_encrypt.py
│   ├── rsa_she_encrypt.py
│   └── unencrypted_baseline.py
├── 2_sample_data/
│   ├── README.md
│   └── source_original/
├── 3_output_data/
│   ├── README.md
│   ├── analysis_ready/
│   │   └── iomt_encryption_analysis_ready.csv
│   ├── run_metrics/
│   │   ├── ecc_timing_results.csv
│   │   ├── rsa_she_timing_results.csv
│   │   └── unencrypted_timing_results.csv
│   └── validation_reports/
│       ├── combined_metrics_validation_report.csv
│       ├── ecc_validation_report.csv
│       ├── rsa_she_validation_report.csv
│       └── unencrypted_validation_report.csv
├── 4_spss_outputs/
│   ├── README.md
│   ├── exported_report/
│   │   └── SPSS_final_analysis.pdf
│   ├── output/
│   │   ├── iomt_encryption_final_data.sav
│   │   └── SPSS_final_analysis.spv
│   └── syntax/
│       └── SPSS_final_analysis.sps
├── 5_documentation/
│   ├── citations/
│   │   ├── citation.bib
│   │   └── citation.cff
│   ├── license/
│   │   └── license.txt
│   ├── repository_configuration/
│   │   └── README.md
│   ├── reproducibility/
│   │   └── README.md
│   ├── requirements/
│   │   └── requirements.txt
│   └── variable_dictionary/
│       └── variable_dictionary.txt
├── Legacy/
│   └── Version1/
├── .gitignore
├── CITATION.cff
├── citation.bib
├── LICENSE
├── README.md
└── requirements.txt
```

## Interpretation Boundary

The final Version 2 findings apply to the tested implementations, synthetic datasets, documented test computer, and controlled simulation.

The study does not establish:

- Production-grade FHE performance
- General-purpose or arbitrary homomorphic computation capability
- Physical IoMT device performance
- Physical-device power or battery consumption
- Real-world packet interception performance
- Post-quantum security or quantum resistance
- Protection against malware
- Protection against denial-of-service attacks
- Protection against compromised endpoints
- Real-world healthcare deployment performance

The encrypted MAP-numerator calculation was a predefined RSA-SHE implementation and validation workload and was not treated as an additional SPSS dependent variable.

## License

This repository is licensed under the MIT License. See `LICENSE` for details.

## Citation

Repository citation metadata are provided in:

```text
CITATION.cff
citation.bib
5_documentation/citations/citation.cff
5_documentation/citations/citation.bib
```

The citation metadata will be finalized with the updated archival DOI after the final repository version is deposited in Zenodo.
