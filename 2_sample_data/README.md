# Source Original Data

This folder contains the original unencrypted synthetic CSV files used as the input data for the Version 2 IoMT Encryption Simulation study.

These files represent the clean source data before any encryption is applied. The study uses 40 simulated environments:

- ENV-01 through ENV-10: Unencrypted baseline
- ENV-11 through ENV-25: ECC condition
- ENV-26 through ENV-40: RSA-SHE condition

The encryption scripts read these source files and generate the corresponding condition-specific outputs.

All nine protected data fields are stored in clear text in these original source files. These files are intentionally unencrypted so that the study can compare the original data against the unencrypted, ECC, and RSA-SHE conditions.

The data are synthetic and do not contain real patient data, PHI, PII, or information from live medical devices.

These files should be treated as the original Version 2 test inputs and should not be modified when reproducing the study.
