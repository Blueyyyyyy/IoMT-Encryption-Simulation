# Python Scripts

This folder contains the Python scripts used for the Version 2 IoMT Encryption Simulation workflow.

## unencrypted_baseline.py

Creates the unencrypted baseline for ENV-01 through ENV-10.

The script copies the original source data without encryption, verifies that all nine protected fields remain unchanged, records five timing runs and a simulated encryption time of 0 seconds, and creates the unencrypted timing and validation reports.

## ecc_encrypt.py

Processes ENV-11 through ENV-25 using the simulated ECC condition.

The script uses Elliptic Curve Diffie-Hellman (ECDH) with SECP384R1 to establish shared key material, derives a 256-bit AES key using HKDF-SHA256, and encrypts all nine protected fields using AES-256-GCM with a fresh 12-byte nonce for each protected value.

The script performs one untimed warm-up run followed by five timed encryption runs using Python's `time.perf_counter()`. The median of the five timed runs is retained as the simulated encryption time. Output structure, decryption correctness, and clear-text exposure are validated after timing.

## rsa_she_encrypt.py

Processes ENV-26 through ENV-40 using the RSA-based simulated homomorphic encryption condition (RSA-SHE).

RSA-SHE is a controlled 2048-bit RSA-based hybrid simulated-homomorphic adaptation. For each run, the script generates a new RSA key pair, applies run-specific encoding, performs RSA modular encryption of all nine protected fields, and applies a randomized hybrid layer to the RSA ciphertext values.

The script also performs the predefined encrypted MAP-numerator calculation:

`SBP + 2(DBP)`

while the required blood-pressure values remain encrypted. Division by three to complete the MAP calculation is performed only after validation decryption.

One untimed warm-up run is followed by five timed runs using Python's `time.perf_counter()`, and the median timing value is retained. The timed interval includes RSA key generation, homomorphic setup, encryption of all nine protected fields, the hybrid randomizing layer, the encrypted MAP-numerator evaluation, and construction of the encrypted in-memory output structure.

Correctness validation occurs after timing and includes hybrid ciphertext construction checks, sampled decrypt/unmask round-trip checks across all nine protected fields, validation of the encrypted MAP-numerator calculation for every source row, arithmetic and encoding checks, and confirmation of 0% clear-text exposure.

RSA-SHE is not a production-grade Fully Homomorphic Encryption implementation, is not an exact reproduction of MEHE, and does not support arbitrary ciphertext computation.

## collect_metrics.py

Combines and validates the results from all three experimental conditions.

The script checks the condition-specific timing files, validation reports, generated transmission files, environment assignments, row and column structure, file sizes, average row lengths, simulated encryption times, and clear-text exposure.

For RSA-SHE, the script also validates the recorded diagnostic information, including the median timed run, RSA stage timings, hybrid ciphertext construction checks, decrypt/unmask checks, encrypted MAP-numerator validation, RSA key size, and public exponent.

After all checks pass, the script creates the final 40-environment analysis-ready dataset and the combined validation report.

## Recommended Run Order

1. `unencrypted_baseline.py`
2. `ecc_encrypt.py`
3. `rsa_she_encrypt.py`
4. `collect_metrics.py`

The first three scripts generate the condition-specific outputs, timing results, and validation reports. `collect_metrics.py` should be run last because it verifies those files and uses them to create the final analysis-ready dataset and combined validation report.
