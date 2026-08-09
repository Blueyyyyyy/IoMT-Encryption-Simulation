# SPSS Outputs

This folder contains the Version 2 IBM SPSS Statistics files used for the final statistical analysis of the IoMT Encryption Simulation study.

## exported_report

This folder contains the human-readable exported version of the final SPSS results.

### SPSS_final_analysis.pdf

PDF export of the final SPSS statistical output.

The report contains:

- Encryption-condition frequencies and case processing summaries
- Descriptive statistics for file size, average row length, simulated encryption time, and clear-text exposure
- Tests of normality and related diagnostic plots
- Levene's tests of homogeneity of variance
- Welch's one-way ANOVA for file size
- Games–Howell pairwise comparisons for file size
- Kruskal–Wallis tests for average row length and simulated encryption time
- Bonferroni-adjusted pairwise comparisons following the Kruskal–Wallis tests
- Descriptive clear-text exposure results

Clear-text exposure was evaluated descriptively because both encrypted conditions produced 0% exposure with no within-group variation.

This PDF contains the final statistical results used in the dissertation.

## output

This folder contains the final SPSS data file and native output file.

### iomt_encryption_final_data.sav

SPSS data file containing the final 40-environment Version 2 dataset used for the statistical analysis.

The dataset contains:

- 10 unencrypted environments
- 15 simulated ECC environments
- 15 RSA-SHE environments

The four primary analysis outcomes are file size, average row length, simulated encryption time, and clear-text exposure.

### SPSS_final_analysis.spv

Native IBM SPSS Statistics Viewer file containing the complete final statistical analysis output, including descriptive statistics, assumption testing, robust omnibus tests, pairwise comparisons, diagnostic plots, and clear-text exposure results.

## syntax

This folder contains the SPSS syntax used to perform the final Version 2 statistical analysis.

### SPSS_final_analysis.sps

SPSS syntax file containing the commands used to import the final 40-environment analysis-ready CSV, create the SPSS dataset, and generate the final statistical output.

The syntax includes procedures for:

- Frequencies and descriptive statistics
- Normality assessment
- Homogeneity-of-variance testing
- Welch's one-way ANOVA
- Games–Howell multiple comparisons
- Kruskal–Wallis testing
- Bonferroni-adjusted pairwise comparisons
- Descriptive analysis of clear-text exposure

Together, these folders preserve the final SPSS dataset, analysis syntax, native output, and exported PDF report used to support the dissertation findings.
