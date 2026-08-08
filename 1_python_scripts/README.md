# Python Scripts

This folder contains the Python scripts used for the Version 2 IoMT Encryption Simulation workflow.

## unencrypted_baseline.py

Creates the unencrypted baseline for ENV-01 through ENV-10.

The script copies the original source data without encryption, verifies that all protected values remain unchanged, records a simulated encryption time of 0 seconds, and creates the unencrypted timing and validation reports. :contentReference[oaicite:0]{index=0}

## ecc_encrypt.py

Processes ENV-11 through ENV-25 using the ECC condition.

The script uses ECDH with SECP384R1 to establish key material, derives an AES-256 key with HKDF-SHA256, and encrypts all nine protected fields using AES-256-GCM. It performs one warm-up run and five timed encryption runs and records the median encryption time and validation results. :contentReference[oaicite:1]{index=1}

## rsa_she_encrypt.py

Processes ENV-26 through ENV-40 using the RSA-SHE condition.

The script generates a new 2048-bit RSA key pair for each timed run and encrypts all nine protected fields using RSA-OAEP with SHA-256. It performs one warm-up run and five timed runs and records the median encryption time and validation results. RSA-SHE is a simulated condition and does not perform computation on encrypted ciphertext. :contentReference[oaicite:2]{index=2}

## collect_metrics.py

Combines and validates the results from all three experimental conditions.

The script checks the timing files, validation reports, generated transmission files, environment assignments, file sizes, average row lengths, encryption times, and clear-text exposure. It then creates the combined analysis-ready dataset and a combined validation report for the 40 study environments. :contentReference[oaicite:3]{index=3}

## Recommended Run Order

1. `unencrypted_baseline.py`
2. `ecc_encrypt.py`
3. `rsa_she_encrypt.py`
4. `collect_metrics.py`

The first three scripts generate the condition-specific outputs and measurements. `collect_metrics.py` should be run last because it uses those generated files to build the final analysis-ready dataset.
