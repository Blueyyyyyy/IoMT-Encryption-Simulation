# SPSS Outputs

This folder contains the Version 2 IBM SPSS Statistics files used for the final statistical analysis of the IoMT Encryption Simulation study.

## exported_report

This folder contains the human-readable exported version of the final SPSS results.

### SPSS_analysis.pdf

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

This folder contains the working SPSS data and native output files.

### iomt_encryption_analysis_ready.sav

SPSS data file containing the final 40-environment Version 2 analysis-ready dataset.

The dataset contains:

- 10 unencrypted environments
- 15 simulated ECC environments
- 15 RSA-SHE environments

The four primary analysis outcomes are file size, average row length, simulated encryption time, and clear-text exposure.

### SPSS_analysis.spv

Native IBM SPSS Statistics Viewer file containing the complete final analysis output, including descriptive statistics, assumption testing, robust omnibus tests, pairwise comparisons, diagnostic plots, and clear-text exposure results.

## syntax

This folder contains the SPSS syntax used to perform the final Version 2 statistical analysis.

### SPSS_analysis.sps

SPSS syntax file containing the commands used to analyze the final 40-environment dataset and generate the statistical output.

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
