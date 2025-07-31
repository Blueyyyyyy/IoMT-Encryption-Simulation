# IoMT Encryption Simulation

This repository contains all the code and data used for my doctoral dissertation research on encryption performance in Internet of Medical Things (IoMT) systems. The study compares unencrypted data, ECC encryption, and RSA-based fully homomorphic encryption (FHE) using simulated network environments.

Python was used to generate encrypted and unencrypted test files, simulate realistic encryption latency, and calculate metrics such as file size, row density, and encryption time. These metrics were then analyzed using IBM SPSS.

## Folder Overview

- `python_scripts/` – Python files used to generate and process the data
- `sample_data/` – Simulated CSV files representing unencrypted, ECC, and RSA-FHE traffic
- `output_data/` – Combined summary dataset used for statistical testing
- `spss_outputs/` – Statistical analysis output from IBM SPSS
- `documentation/` – Variable descriptions, requirements, and license

All simulations were performed offline and no real patient data was used.

---

## Citation

If you use or reference this work, please cite the GitHub repository or final dissertation DOI (coming soon).
