# IoMT Encryption Simulation

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21904513.svg)](https://doi.org/10.5281/zenodo.21904513)

## Correction Notice

I am updating this repository to correct the RSA-based simulated homomorphic encryption output files and the related statistical analysis. Version 1.0 is preserved for transparency but should not be used for final analysis. A corrected Version 2.0 will replace it. 

This repository contains all the code and data used for my doctoral dissertation research on encryption performance in Internet of Medical Things (IoMT) systems. The study compares unencrypted data, ECC encryption, and RSA-based fully homomorphic encryption (FHE) using simulated network environments.

Python was used to generate encrypted and unencrypted test files, simulate realistic encryption latency, and calculate metrics such as file size, row density, and encryption time. These metrics were then analyzed using IBM SPSS.

## Folder Overview

- `1_python_scripts/` – Python files used to generate and process the data  
- `2_sample_data/` – Simulated CSV files (Unencrypted, ECC, RSA-FHE)  
- `3_output_data/` – Combined dataset for statistical testing  
- `4_spss_outputs/` – Output from IBM SPSS  
- `5_documentation/` – Variable descriptions, requirements, and license

All simulations were performed offline and no real patient data was used.

To see DescriptiveStatisticsOutput.pdf, One-WayANOVAOutput.pdf, and/or TukeyOutput.pdf download the files. 

Here are the individual links:

Descriptive Statistics Output
https://github.com/Blueyyyyyy/IoMT-Encryption-Simulation/raw/main/4_spss_outputs/DescriptiveStatisticsOutput.pdf

One-Way ANOVA Output
https://github.com/Blueyyyyyy/IoMT-Encryption-Simulation/raw/main/4_spss_outputs/One-WayANOVAOutput.pdf

Tukey HSD Post-Hoc Output
https://github.com/Blueyyyyyy/IoMT-Encryption-Simulation/raw/main/4_spss_outputs/TukeyOutput.pdf

---

## Citation

If you use or reference this work, please cite the GitHub repository, CITATION.cff, citation.bib, or Anderson, D. (2025). IoMT encryption simulation dataset and Python scripts (Version 1.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.16659484
