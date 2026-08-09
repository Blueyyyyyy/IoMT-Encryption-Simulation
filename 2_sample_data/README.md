# Source Original Data

This folder contains the original unencrypted synthetic CSV files used as the input data for the Version 2 IoMT Encryption Simulation study.

These files represent the predefined source data before any encryption is applied. The study uses 40 simulated environments assigned across three experimental conditions:

- ENV-01 through ENV-10: Unencrypted baseline
- ENV-11 through ENV-25: Simulated ECC condition
- ENV-26 through ENV-40: RSA-SHE condition

The condition-specific Python scripts read these source files and generate the corresponding transmission outputs for each experimental condition.

All nine protected transmission fields are stored in clear text in the original source files. These files are intentionally unencrypted so the study can compare the original values with the outputs produced under the unencrypted, simulated ECC, and RSA-SHE conditions.

The data are synthetic and do not contain real patient data, Protected Health Information (PHI), Personally Identifiable Information (PII), or information collected from live medical devices or healthcare networks.

These files should be treated as the original Version 2 experimental inputs and should not be modified when reproducing the study.
