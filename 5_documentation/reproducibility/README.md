# Version 2 Reproducibility Instructions

## Purpose

This document describes how to reproduce the corrected Version 2 analysis for the IoMT Encryption Simulation study.

The study used 40 simulated always-operating Internet of Medical Things environments divided across three experimental conditions:

- Unencrypted: ENV-01 through ENV-10
- Simulated ECC: ENV-11 through ENV-25
- RSA-SHE: ENV-26 through ENV-40

RSA-SHE refers to the RSA-based simulated homomorphic encryption condition used in the study.

RSA-SHE used RSA-OAEP with SHA-256. It did not perform computations on ciphertext and was not a fully or partially homomorphic encryption implementation.

The study used synthetic data only. No real patient data, PHI, PII, physical medical devices, or live healthcare networks were used.

## Repository Version

Use the corrected Version 2 repository contents.

Superseded Version 1 scripts, outputs, or statistical analyses should not be used to reproduce the final dissertation results.

The final repository ROOT and folder structure include:

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

## Software Environment

The original Version 2 timing measurements were produced using:

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

Exact encryption timing values may differ on other hardware or software environments.

## Clone the Repository

Clone the repository and enter the project directory:

git clone https://github.com/Blueyyyyyy/IoMT-Encryption-Simulation.git
cd IoMT-Encryption-Simulation

Use the corrected Version 2 branch when reproducing the correction work:

git checkout correction-v2
Create a Python Environment

## Create a Python virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

Install the required Python packages:

python -m pip install --upgrade pip
pip install -r requirements.txt

The root-level requirements.txt contains the package versions required for the corrected Version 2 workflow.

## Source Data

The original synthetic source CSV files belong in:

2_sample_data/source_original/

The complete study contains 40 simulated environments:

ENV-01 through ENV-40

The condition assignments are fixed:

Environment Range	Condition	n
ENV-01 to ENV-10	Unencrypted	10
ENV-11 to ENV-25	Simulated ECC	15
ENV-26 to ENV-40	RSA-SHE	15

The same synthetic source structure was used to support controlled comparison across the three conditions.

## Protected Transmission Fields

Nine data fields were treated as protected values:

Organization identifier
Device identifier
Timestamp
Heart rate
Systolic blood pressure
Diastolic blood pressure
Oxygen saturation
Temperature
Battery level

Under both encrypted conditions, all values within these nine fields were encrypted.

Column headings were not treated as protected values.

Row count and column order were retained.

## Unencrypted Condition

ENV-01 through ENV-10 form the unencrypted baseline.

No encryption operation is performed.

The baseline output is stored under:

2_sample_data/unencrypted/

The unencrypted condition has:

simulated encryption time = 0 seconds
clear-text exposure = 100%

The zero encryption-time value represents the absence of an encryption operation.

## Simulated ECC Condition

ENV-11 through ENV-25 form the simulated ECC condition.

The corrected Version 2 implementation uses:

Elliptic Curve Diffie-Hellman
SECP384R1
HKDF with SHA-256
256-bit derived symmetric key
AES-256-GCM
New nonce for every protected-value encryption operation
Base64-encoded encrypted output

ECC is used for key agreement and key derivation. AES-256-GCM encrypts the protected values.

The output is stored under:

2_sample_data/ecc/

The expected clear-text exposure result is:

0%
## RSA-SHE Condition

ENV-26 through ENV-40 form the RSA-SHE condition.

The corrected Version 2 implementation uses:

RSA
OAEP padding
SHA-256
Encryption of all nine protected transmission fields
Base64-encoded encrypted output

The output is stored under:

2_sample_data/rsa_she/

RSA-SHE does not:

Perform computation on ciphertext
Implement fully homomorphic encryption
Implement partially homomorphic encryption
Reproduce the computational behavior of BFV, BGV, CKKS, or another production-grade FHE scheme

The expected clear-text exposure result is:

0%
## Encryption Timing Procedure

Timing is performed only for the encrypted conditions.

Python's:

time.perf_counter()

is used to measure actual elapsed processing time.

For each encrypted environment:

Load the source file before timing begins.
Perform one untimed warm-up run.
Perform five timed runs.
Begin timing immediately before condition-specific key generation and encryption.
Generate new cryptographic keys for each timed run.
Encrypt the complete set of protected values.
End timing after the complete encrypted data structure has been produced.
Record the five elapsed times.
Retain the median elapsed time as the analytical encryption-time value.

Source-file loading is excluded from the timed interval.

Output-file writing is excluded from the timed interval.

Cryptographic key generation is included in the timed interval.

For simulated ECC, new AES-GCM nonces are generated for every protected-value encryption operation.

No artificial latency, sleep() commands, or manually assigned timing values are used in Version 2.

## Clear-Text Exposure

Clear-text exposure is calculated across the nine protected transmission fields.

The calculation is:

clear-text exposure (%) =
(readable and unchanged protected values / total protected values) × 100

Column headings are excluded.

Expected results are:

Condition	Expected Clear-Text Exposure
Unencrypted	100%
Simulated ECC	0%
RSA-SHE	0%

A value is counted as exposed only when the protected output value remains readable and unchanged from the corresponding original source value.

## Version 2 Metrics

The analysis-ready dataset contains the following primary variables:

environment
encryption_type
file_size_kb
avg_row_length_bytes
simulated_encryption_time_sec
cleartext_exposure_pct

See:

5_documentation/variable_dictionary.txt

for complete definitions.

Condition-level timing and validation information is retained under:

3_output_data/run_metrics/
3_output_data/validation_reports/

The dataset used for statistical analysis is retained under:

3_output_data/analysis_ready/
## Validation Checks

Before statistical analysis, confirm the following.

Group Counts
Unencrypted = 10
ECC = 15
RSA-SHE = 15
Total = 40
## Encryption Completeness

For both encrypted conditions:

All nine protected fields are encrypted.
No protected value remains readable and unchanged.
Row counts remain unchanged.
Column order remains unchanged.
Encryption errors are not silently substituted into the dataset.
## Clear-Text Exposure

Expected values are:

Unencrypted = 100%
ECC = 0%
RSA-SHE = 0%
## Timing

For each encrypted environment:

One warm-up run is not retained.
Five timed runs are recorded.
All retained timed-run values are actual measured elapsed times.
The median of the five runs is the analytical value.
No artificial processing delays are present.
## Statistical Analysis

IBM SPSS Statistics is used for the corrected Version 2 inferential analysis.

The final SPSS syntax is stored under:

4_spss_outputs/syntax/

Use the final Version 2 analysis-ready dataset from:

3_output_data/analysis_ready/

The corrected procedures are:

## File Size

Use:

Welch's one-way ANOVA
Games-Howell pairwise comparisons

Expected omnibus result:

F(2, 18.667) = 79.262, p < .001

All three file-size pairwise comparisons should be statistically significant.

## Average Row Length

Use:

Independent-samples Kruskal-Wallis test
Bonferroni-adjusted pairwise comparisons

Expected omnibus result:

H(2) = 38.334, p < .001

Expected adjusted pairwise results:

Unencrypted vs ECC:      p = .017
Unencrypted vs RSA-SHE:  p < .001
ECC vs RSA-SHE:          p = .001
## Simulated Encryption Time

Use:

Independent-samples Kruskal-Wallis test
Bonferroni-adjusted pairwise comparisons

Expected omnibus result:

H(2) = 34.838, p < .001

Expected adjusted pairwise results:

Unencrypted vs ECC:      p = .025
Unencrypted vs RSA-SHE:  p < .001
ECC vs RSA-SHE:          p = .001
## Clear-Text Exposure

Evaluate clear-text exposure descriptively.

Do not conduct an inferential ECC-versus-RSA-SHE test because both encrypted conditions contain:

0% exposure
0 within-group variance
## Expected Descriptive Results

The corrected Version 2 results are:

Condition	n	File Size Mean KB	Average Row Length Mean Bytes	Encryption Time Mean Seconds	Clear-Text Exposure
Unencrypted	10	61.64150	61.02590	0.00000000	100%
ECC	15	1825.35319	428.00000	0.06399869	0%
RSA-SHE	15	35791.88965	3104.00000	2.92742547	0%

Standard deviations for the three performance measures are:

Condition	File Size SD	Average Row Length SD	Encryption Time SD
Unencrypted	0.005922	0.006064	0.000000000
ECC	1186.218687	0.000000	0.039449822
RSA-SHE	12089.403372	0.000000	0.974129258
## Hypothesis Decisions

The reproduced Version 2 analysis should support the following decisions.

## Research Question 1

Reject the null hypothesis.

RSA-SHE differs significantly from the unencrypted condition in the operationalized network-traffic measures of file size and average row length.

## Research Question 2

Do not reject the null hypothesis.

Both simulated ECC and RSA-SHE produce 0% clear-text exposure.

RSA-SHE is not shown to improve the measured confidentiality outcome beyond simulated ECC.

## Research Question 3

Reject the null hypothesis for all three operationalized performance measures.

RSA-SHE differs significantly from simulated ECC in:

File size
Average row length
Simulated encryption time

RSA-SHE produces the larger values for all three measured performance outcomes.

## Interpretation Boundary

Successful reproduction of these results demonstrates reproduction of the controlled Version 2 simulation and statistical analysis.

It does not establish:

Production-grade FHE performance
Homomorphic computation performance
Post-quantum security
Quantum resistance
Protection against malware
Protection against denial-of-service attacks
Protection against compromised endpoints
Physical IoMT device performance
Real-world healthcare deployment performance

The findings apply to the tested implementations and controlled simulated environment.
