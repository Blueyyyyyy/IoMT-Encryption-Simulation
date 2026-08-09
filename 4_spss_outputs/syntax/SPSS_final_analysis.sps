* SPSS final statistical analysis.
* Project: IoMT Encryption Simulation final rebuild.

OUTPUT NEW NAME=SPSS_final_analysis.
SET DECIMAL DOT.

* Import the final 40-environment analysis-ready dataset.
GET DATA
  /TYPE=TXT
  /FILE='D:\RSA_SHE_Rebuild_Test\3_output_data\analysis_ready\iomt_encryption_analysis_ready.csv'
  /ENCODING='UTF8'
  /DELCASE=LINE
  /DELIMITERS=","
  /QUALIFIER='"'
  /ARRANGEMENT=DELIMITED
  /FIRSTCASE=2
  /VARIABLES=
    environment_id A6
    encryption_code F1.0
    encryption_type A12
    file_size_kb F20.6
    average_row_length_bytes F20.6
    simulated_encryption_time_sec F20.9
    clear_text_exposure_percent F8.3
    row_count F10.0
    column_count F2.0
    source_file A60
    output_file A80.

DATASET NAME iomt_data.

VARIABLE LABELS
  environment_id 'Simulated environment identifier'
  encryption_code 'Encryption condition code'
  encryption_type 'Encryption condition'
  file_size_kb 'Output file size in kilobytes'
  average_row_length_bytes 'Average row length in bytes'
  simulated_encryption_time_sec 'Measured encryption time in seconds'
  clear_text_exposure_percent 'Clear-text exposure percentage'
  row_count 'Number of data rows'
  column_count 'Number of protected columns'.

VALUE LABELS encryption_code
  1 'Unencrypted'
  2 'ECC'
  3 'RSA-SHE'.

VARIABLE LEVEL
  encryption_code (NOMINAL)
  file_size_kb average_row_length_bytes simulated_encryption_time_sec
  clear_text_exposure_percent row_count column_count (SCALE).

FORMATS
  file_size_kb (F16.3)
  average_row_length_bytes (F12.3)
  simulated_encryption_time_sec (F12.6)
  clear_text_exposure_percent (F8.2).

EXECUTE.

* Save the final SPSS data file.
SAVE OUTFILE='D:\RSA_SHE_Rebuild_Test\4_spss_outputs\iomt_encryption_final_data.sav'.

* Confirm the 10/15/15 group counts.
FREQUENCIES VARIABLES=encryption_code
  /ORDER=ANALYSIS.

* Descriptive statistics for all four primary outcomes.
MEANS TABLES=file_size_kb average_row_length_bytes
  simulated_encryption_time_sec clear_text_exposure_percent BY encryption_code
  /CELLS=COUNT MEAN STDDEV MIN MAX.

* Distribution and normality diagnostics for the three performance outcomes.
EXAMINE VARIABLES=file_size_kb average_row_length_bytes
  simulated_encryption_time_sec BY encryption_code
  /PLOT=BOXPLOT NPPLOT
  /COMPARE=GROUPS
  /STATISTICS=DESCRIPTIVES
  /CINTERVAL=95
  /MISSING=LISTWISE
  /NOTOTAL.

* File size: Levene, Welch, Brown-Forsythe, and Games-Howell.
ONEWAY file_size_kb BY encryption_code
  /STATISTICS=DESCRIPTIVES HOMOGENEITY WELCH BROWNFORSYTHE
  /POSTHOC=GH ALPHA(.05)
  /MISSING=ANALYSIS.

* Average row length: document variance tests and robust-test availability.
ONEWAY average_row_length_bytes BY encryption_code
  /STATISTICS=DESCRIPTIVES HOMOGENEITY WELCH BROWNFORSYTHE
  /MISSING=ANALYSIS.

* Measured encryption time: document variance tests and robust-test availability.
ONEWAY simulated_encryption_time_sec BY encryption_code
  /STATISTICS=DESCRIPTIVES HOMOGENEITY WELCH BROWNFORSYTHE
  /MISSING=ANALYSIS.

* Average row length: Kruskal-Wallis with Bonferroni-adjusted pairwise comparisons.
NPTESTS
  /INDEPENDENT TEST(average_row_length_bytes) GROUP(encryption_code)
    KRUSKAL_WALLIS(COMPARE=PAIRWISE)
  /MISSING SCOPE=ANALYSIS USERMISSING=EXCLUDE
  /CRITERIA ALPHA=0.05 CILEVEL=95.

* Measured encryption time: Kruskal-Wallis with Bonferroni-adjusted pairwise comparisons.
NPTESTS
  /INDEPENDENT TEST(simulated_encryption_time_sec) GROUP(encryption_code)
    KRUSKAL_WALLIS(COMPARE=PAIRWISE)
  /MISSING SCOPE=ANALYSIS USERMISSING=EXCLUDE
  /CRITERIA ALPHA=0.05 CILEVEL=95.

* Clear-text exposure is evaluated descriptively only.
MEANS TABLES=clear_text_exposure_percent BY encryption_code
  /CELLS=COUNT MEAN STDDEV MIN MAX.

* Save the complete SPSS Viewer output.
OUTPUT SAVE NAME=SPSS_final_analysis
  OUTFILE='D:\RSA_SHE_Rebuild_Test\4_spss_outputs\SPSS_final_analysis.spv'.
