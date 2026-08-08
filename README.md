# IoMT Encryption Simulation

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21845613.svg)](https://doi.org/10.5281/zenodo.21845613)

## Version 2

This repository contains the Python scripts, synthetic data, analysis files, and supporting documentation used for my doctoral dissertation research on encryption-related performance and clear-text exposure in simulated always-operating Internet of Medical Things (IoMT) environments.

Version 2 contains the corrected implementation documentation, statistical analysis, and interpretation used for the final dissertation manuscript.

The study compared three experimental conditions:

- Unencrypted transmissions
- Simulated Elliptic Curve Cryptography (ECC)
- RSA-based simulated homomorphic encryption condition (RSA-SHE)

The RSA-SHE condition was an experimental RSA-OAEP encryption condition. It was not a production-grade Fully Homomorphic Encryption (FHE) implementation, did not perform computations on ciphertext, and was neither fully nor partially homomorphic encryption. Results from RSA-SHE should therefore not be interpreted as performance or security benchmarks for production-grade FHE systems such as BFV, BGV, or CKKS.

Version 1 files that were superseded by the corrected analysis are retained separately for research transparency and should not be used as the final analytical results of the study.

## Study Design

The study used a controlled Python-based simulation consisting of 40 simulated always-operating IoMT environments.

The experimental groups were:

| Encryption Condition | n |
| --- | ---: |
| Unencrypted | 10 |
| Simulated ECC | 15 |
| RSA-SHE | 15 |
| **Total** | **40** |

Synthetic data were used throughout the experiment. No real patient data, Protected Health Information (PHI), Personally Identifiable Information (PII), physical medical devices, or live healthcare networks were used.

The simulation evaluated implementation-specific differences in operational performance and clear-text exposure under controlled conditions.

## Encryption Conditions

### Unencrypted

The unencrypted condition retained the protected values in readable form and served as the baseline condition.

No encryption operation was performed for this condition. Simulated encryption time was therefore recorded as 0 seconds.

### Simulated ECC

The simulated ECC condition used:

- Elliptic Curve Diffie-Hellman (ECDH)
- SECP384R1 elliptic curve
- HKDF with SHA-256
- AES-256-GCM for protected-value encryption
- A new nonce for each protected value
- Base64-encoded encrypted output

ECC was used for key agreement and key derivation rather than for directly encrypting the complete dataset. For this reason, the condition is described as simulated ECC.

### RSA-SHE

The RSA-based simulated homomorphic encryption condition used:

- RSA encryption
- OAEP padding
- SHA-256
- Encryption of all protected data values
- Newly generated cryptographic keys for each timed run
- Base64-encoded encrypted output

RSA-SHE was used to evaluate implementation-specific ciphertext expansion, elapsed encryption time, and clear-text exposure.

RSA-SHE did not:

- Perform computations on ciphertext
- Implement Fully Homomorphic Encryption
- Implement Partially Homomorphic Encryption
- Approximate the computational behavior of production-grade FHE
- Test post-quantum security
- Test quantum resistance

The term RSA-SHE is retained as the study's experimental-condition label and should not be interpreted as a claim that RSA-OAEP is homomorphic encryption.

## Protected Data and Clear-Text Exposure

Clear-text exposure was the measured confidentiality outcome.

Protected values included all data cells under the nine transmission columns representing:

1. Organization identifier
2. Device identifier
3. Timestamp
4. Heart rate
5. Systolic blood pressure
6. Diastolic blood pressure
7. Oxygen saturation
8. Temperature
9. Battery level

Column headings were excluded from the clear-text exposure calculation.

Clear-text exposure was calculated as:

**Clear-text exposure (%) = (readable and unchanged protected values / total protected values) × 100**

The expected interpretation was:

- 100% = all protected values remained readable and unchanged
- 0% = no protected values remained readable and unchanged

The unencrypted condition produced 100% clear-text exposure.

Both simulated ECC and RSA-SHE produced 0% clear-text exposure.

Because both encrypted conditions produced the same 0% result, RSA-SHE did not demonstrate an additional measured confidentiality advantage over simulated ECC on the clear-text exposure measure used in this study.

## Measured Outcomes

The study evaluated four primary outcomes:

### File Size

Total size of the generated transmission output, measured in kilobytes (KB). File size represented ciphertext expansion and transmission/storage demand.

### Average Row Length

Average number of bytes contained in each simulated transmission record. Average row length represented encrypted payload growth.

### Simulated Encryption Time

Actual elapsed processing time, measured in seconds, required to complete the condition-specific encryption process within the simulated environment.

Despite the variable name, simulated encryption time was not an artificial delay. It represented actual elapsed processing time for the tested implementation.

### Clear-Text Exposure

Percentage of protected data values that remained readable and unchanged in the generated transmission output.

## Encryption Timing Procedure

Encryption time was measured using Python's `time.perf_counter()` function.

For each simulated encrypted environment:

1. The source file was loaded before timing began.
2. One untimed warm-up run was performed.
3. Five timed runs were performed.
4. Timing began immediately before condition-specific key generation and encryption.
5. Timing ended after the complete encrypted data structure was produced.
6. The median of the five timed runs was retained as the simulated encryption time.
7. New cryptographic keys were generated for each timed run.
8. New AES-GCM nonces were generated for every protected-value encryption operation in the simulated ECC condition.

Source-file loading and output-file writing were excluded from the timing measurement.

No `sleep()` commands, artificial latency, or other artificial processing delays were used to produce the Version 2 timing results.

The unencrypted condition was recorded as 0 seconds because no encryption operation was performed.

## Test Environment

All encryption timing was conducted using the same computer and software environment:

- Processor: Intel Core i9-9900K
- Base clock speed: 3.60 GHz
- Physical memory: approximately 16 GB
- Operating system: Microsoft Windows 11 Home, 64-bit
- Windows version: 10.0.26200
- Python: 3.11.0
- cryptography: 45.0.4
- pandas: 2.3.0

The measured encryption times are specific to this implementation and test environment. They should not be interpreted as universal execution times for ECC, RSA, or production-grade FHE systems.

## Version 2 Descriptive Results

| Encryption Condition | n | Mean File Size (KB) | Mean Average Row Length (Bytes) | Mean Encryption Time (s) | Clear-Text Exposure |
| --- | ---: | ---: | ---: | ---: | ---: |
| Unencrypted | 10 | 61.64 | 61.03 | 0.000 | 100% |
| Simulated ECC | 15 | 1,825.35 | 428.00 | 0.064 | 0% |
| RSA-SHE | 15 | 35,791.89 | 3,104.00 | 2.927 | 0% |

RSA-SHE produced the largest mean file size, average row length, and simulated encryption time. Simulated ECC produced intermediate values, and the unencrypted condition produced the smallest values.

Both encrypted conditions eliminated observable clear-text exposure.

## Statistical Analysis

IBM SPSS was used for statistical analysis.

Homogeneity of variance was evaluated using Levene's test. Significant Levene tests were observed for all three measured performance outcomes:

- File size
- Average row length
- Simulated encryption time

Because equal variances were not supported, outcome-specific robust procedures were used.

### File Size

File size was analyzed using:

- Welch's one-way ANOVA
- Games-Howell pairwise comparisons

The Welch omnibus result was statistically significant:

**F(2, 18.667) = 79.262, p < .001**

All three Games-Howell pairwise file-size comparisons were statistically significant.

### Average Row Length

Welch's and Brown-Forsythe tests could not be calculated because the RSA-SHE condition had zero within-group variance for average row length.

Average row length was therefore analyzed using:

- Independent-samples Kruskal-Wallis test
- Bonferroni-adjusted pairwise comparisons

The omnibus result was statistically significant:

**H(2) = 38.334, p < .001**

All three Bonferroni-adjusted pairwise comparisons were statistically significant.

### Simulated Encryption Time

Welch's and Brown-Forsythe tests could not be calculated because the unencrypted condition had zero within-group variance for simulated encryption time.

Simulated encryption time was therefore analyzed using:

- Independent-samples Kruskal-Wallis test
- Bonferroni-adjusted pairwise comparisons

The omnibus result was statistically significant:

**H(2) = 34.838, p < .001**

All three Bonferroni-adjusted pairwise comparisons were statistically significant.

### Clear-Text Exposure

Clear-text exposure was evaluated descriptively.

Inferential comparison between simulated ECC and RSA-SHE was not applicable because both encrypted conditions produced 0% clear-text exposure with no within-group variation.

## Research Question Decisions

The corrected Version 2 analysis produced the following hypothesis decisions:

- **Research Question 1:** The null hypothesis was rejected. RSA-SHE differed significantly from the unencrypted condition in the measured network-traffic outcomes of file size and average row length.
- **Research Question 2:** The null hypothesis was not rejected. Simulated ECC and RSA-SHE both produced 0% clear-text exposure, and RSA-SHE was not shown to improve the measured confidentiality outcome beyond simulated ECC.
- **Research Question 3:** The null hypothesis was rejected for all three operationalized performance measures. RSA-SHE differed significantly from simulated ECC in file size, average row length, and simulated encryption time.

Within the tested implementations, RSA-SHE introduced greater measured processing and transmission demands than simulated ECC without producing an additional advantage on the clear-text exposure measure.

These findings do not establish the performance, security, feasibility, or privacy-preserving computation capabilities of production-grade FHE.

## Repository Structure

The Version 2 repository is organized around the following directories and root-level files:

```text
IoMT-Encryption-Simulation/
├── 1_python_scripts/
├── 2_sample_data/
├── 3_output_data/
├── 4_spss_outputs/
├── 5_documentation/
├── Legacy/
│   └── Version1/
├── .gitignore
├── CITATION.cff
├── citation.bib
├── LICENSE
├── README.md
└── requirements.txt
