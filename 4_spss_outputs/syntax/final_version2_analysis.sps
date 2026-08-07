* ==========================================================================.
* IoMT Encryption Simulation - Final Version 2 SPSS Analysis.
* Dissertation: Devin Anderson.
* ==========================================================================.

* This syntax reproduces the statistical procedures used for the corrected
* Version 2 dissertation analysis.
*
* Expected analytical variables:
*
* encryption_code
* file_size_kb
* avg_row_length_bytes
* simulated_encryption_time_sec
* cleartext_exposure_pct
*
* Expected group sizes:
*
* Unencrypted = 10
* ECC         = 15
* RSA-SHE     = 15
* Total       = 40
*
* IMPORTANT:
* RSA-SHE refers to the RSA-based simulated homomorphic encryption condition.
* It was not a production-grade fully or partially homomorphic encryption
* implementation.
*
* Open the final Version 2 analysis-ready .sav file before running this syntax.
* ==========================================================================.


* --------------------------------------------------------------------------.
* 1. VERIFY ENCRYPTION-GROUP COUNTS.
* --------------------------------------------------------------------------.

FREQUENCIES VARIABLES=encryption_code
  /ORDER=ANALYSIS.


* --------------------------------------------------------------------------.
* 2. DESCRIPTIVE STATISTICS FOR ALL STUDY OUTCOMES.
* --------------------------------------------------------------------------.

MEANS TABLES=
  file_size_kb
  avg_row_length_bytes
  simulated_encryption_time_sec
  cleartext_exposure_pct
  BY encryption_code
  /CELLS=COUNT MEAN STDDEV MIN MAX.


* --------------------------------------------------------------------------.
* 3. DISTRIBUTION AND DESCRIPTIVE REVIEW OF PERFORMANCE OUTCOMES.
* --------------------------------------------------------------------------.

EXAMINE VARIABLES=
  file_size_kb
  avg_row_length_bytes
  simulated_encryption_time_sec
  BY encryption_code
  /PLOT BOXPLOT NPPLOT
  /COMPARE GROUPS
  /STATISTICS DESCRIPTIVES
  /CINTERVAL 95
  /MISSING LISTWISE
  /NOTOTAL.


* --------------------------------------------------------------------------.
* 4. HOMOGENEITY-OF-VARIANCE TESTS.
*
* Levene's tests are requested for all three performance outcomes.
*
* Expected Version 2 Levene results:
*
* File size:
* F(2,37) = 15.965, p < .001
*
* Average row length:
* F(2,37) = 36.689, p < .001
*
* Simulated encryption time:
* F(2,37) = 17.781, p < .001
*
* Equal variances are therefore not supported for any performance outcome.
* --------------------------------------------------------------------------.

ONEWAY
  file_size_kb
  avg_row_length_bytes
  simulated_encryption_time_sec
  BY encryption_code
  /STATISTICS DESCRIPTIVES HOMOGENEITY
  /MISSING ANALYSIS.


* --------------------------------------------------------------------------.
* 5. FILE SIZE - WELCH'S ONE-WAY ANOVA AND GAMES-HOWELL COMPARISONS.
*
* Welch's ANOVA is the final omnibus procedure for file size because the
* homogeneity-of-variance assumption is not supported.
*
* Games-Howell is used for the three pairwise file-size comparisons because
* group variances and sample sizes are unequal.
*
* Expected Version 2 Welch result:
*
* F(2,18.667) = 79.262, p < .001
* --------------------------------------------------------------------------.

ONEWAY file_size_kb BY encryption_code
  /STATISTICS DESCRIPTIVES HOMOGENEITY WELCH
  /MISSING ANALYSIS
  /POSTHOC=GH ALPHA(.05).


* --------------------------------------------------------------------------.
* 6. AVERAGE ROW LENGTH - KRUSKAL-WALLIS.
*
* Welch's and Brown-Forsythe tests cannot be calculated appropriately for
* this outcome because at least one encryption group has zero within-group
* variance.
*
* The final inferential procedure is therefore an independent-samples
* Kruskal-Wallis test with pairwise comparisons.
*
* SPSS reports Bonferroni-adjusted significance values for the requested
* pairwise comparisons.
*
* Expected Version 2 omnibus result:
*
* H(2) = 38.334, p < .001
*
* Expected adjusted pairwise significance:
*
* Unencrypted vs ECC      = .017
* Unencrypted vs RSA-SHE  < .001
* ECC vs RSA-SHE          = .001
* --------------------------------------------------------------------------.

NPTESTS
  /INDEPENDENT TEST (avg_row_length_bytes)
    GROUP (encryption_code)
    KRUSKAL_WALLIS(COMPARE=PAIRWISE)
  /MISSING SCOPE=ANALYSIS USERMISSING=EXCLUDE
  /CRITERIA ALPHA=0.05 CILEVEL=95.


* --------------------------------------------------------------------------.
* 7. SIMULATED ENCRYPTION TIME - KRUSKAL-WALLIS.
*
* Welch's and Brown-Forsythe tests cannot be calculated appropriately for
* this outcome because the unencrypted group has zero within-group variance.
*
* The final inferential procedure is therefore an independent-samples
* Kruskal-Wallis test with pairwise comparisons.
*
* SPSS reports Bonferroni-adjusted significance values for the requested
* pairwise comparisons.
*
* Expected Version 2 omnibus result:
*
* H(2) = 34.838, p < .001
*
* Expected adjusted pairwise significance:
*
* Unencrypted vs ECC      = .025
* Unencrypted vs RSA-SHE  < .001
* ECC vs RSA-SHE          = .001
* --------------------------------------------------------------------------.

NPTESTS
  /INDEPENDENT TEST (simulated_encryption_time_sec)
    GROUP (encryption_code)
    KRUSKAL_WALLIS(COMPARE=PAIRWISE)
  /MISSING SCOPE=ANALYSIS USERMISSING=EXCLUDE
  /CRITERIA ALPHA=0.05 CILEVEL=95.


* --------------------------------------------------------------------------.
* 8. CLEAR-TEXT EXPOSURE - DESCRIPTIVE ANALYSIS ONLY.
*
* Clear-text exposure is not subjected to an ECC-versus-RSA-SHE inferential
* test because both encrypted conditions contain 0% exposure and zero
* within-group variance.
*
* Expected Version 2 results:
*
* Unencrypted = 100%
* ECC         = 0%
* RSA-SHE     = 0%
* --------------------------------------------------------------------------.

MEANS TABLES=cleartext_exposure_pct BY encryption_code
  /CELLS=COUNT MEAN STDDEV MIN MAX.


CROSSTABS
  /TABLES=encryption_code BY cleartext_exposure_pct
  /CELLS=COUNT ROW.


* --------------------------------------------------------------------------.
* 9. VERSION 2 EXPECTED DESCRIPTIVE RESULTS.
*
* Unencrypted, n=10:
* File size mean = 61.64150 KB.
* File size SD = .005922.
* Average row length mean = 61.02590 bytes.
* Average row length SD = .006064.
* Encryption time mean = .00000000 seconds.
* Clear-text exposure = 100%.
*
* ECC, n=15:
* File size mean = 1825.35319 KB.
* File size SD = 1186.218687.
* Average row length mean = 428.00000 bytes.
* Average row length SD = .000000.
* Encryption time mean = .06399869 seconds.
* Encryption time SD = .039449822.
* Clear-text exposure = 0%.
*
* RSA-SHE, n=15:
* File size mean = 35791.88965 KB.
* File size SD = 12089.403372.
* Average row length mean = 3104.00000 bytes.
* Average row length SD = .000000.
* Encryption time mean = 2.92742547 seconds.
* Encryption time SD = .974129258.
* Clear-text exposure = 0%.
* --------------------------------------------------------------------------.


* --------------------------------------------------------------------------.
* 10. VERSION 2 HYPOTHESIS DECISIONS.
*
* RQ1:
* Reject the null hypothesis.
*
* RQ2:
* Do not reject the null hypothesis.
*
* RQ3:
* Reject the null hypothesis for all three operationalized performance
* measures: file size, average row length, and simulated encryption time.
*
* End of final Version 2 SPSS analysis syntax.
* --------------------------------------------------------------------------.
