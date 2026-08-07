# Version 1 SPSS Analysis — Legacy

This directory preserves superseded Version 1 statistical-analysis files from the IoMT Encryption Simulation project for research transparency.

These files do **not** represent the final statistical analysis reported in the corrected Version 2 dissertation.

## Superseded Files

- `DescriptiveStatisticsOutput.pdf`
- `One-WayANOVAOutput.pdf`
- `TukeyOutput.pdf`

The Version 1 analysis used procedures and implementation assumptions that were subsequently corrected.

In particular, the original one-way ANOVA and Tukey HSD analyses are not the final inferential procedures used in Version 2.

## Version 2 Statistical Procedures

The corrected Version 2 analysis uses:

- Welch's one-way ANOVA with Games-Howell pairwise comparisons for file size
- Kruskal-Wallis testing with Bonferroni-adjusted pairwise comparisons for average row length
- Kruskal-Wallis testing with Bonferroni-adjusted pairwise comparisons for simulated encryption time
- Descriptive evaluation of clear-text exposure

The final Version 2 SPSS syntax is located at:

`4_spss_outputs/syntax/final_version2_analysis.sps`

These legacy files are retained only to document the history of the research process.

They should not be used to reproduce, interpret, or cite the final Version 2 dissertation results.
