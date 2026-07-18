# Phase 3.4 EDA Figures

All figures are accessible vector SVG files generated from aggregate, read-only analysis of BharatFakeNewsKosh v1. They contain no copied article or claim text; the token figure contains aggregate token forms only. SVG preserves publication-scale quality and editability.

| Figure | Purpose |
| --- | --- |
| [01 - Label distribution](01_label_distribution.svg) | Raw `True`/`False` counts; not a canonical label mapping. |
| [02 - Workbook composition](02_dataset_composition.svg) | Primary, auxiliary, and empty source-sheet composition. |
| [03 - Article length](03_article_length_histogram.svg) | Raw `News Body` token-length histogram. |
| [04 - Headline length](04_headline_length_histogram.svg) | Raw `Statement` token-length histogram. |
| [05 - Word counts](05_word_count_distribution.svg) | Raw token-count distributions for body and statement fields. |
| [06 - Character counts](06_character_count_distribution.svg) | Stored-character distributions for body and statement fields. |
| [07 - Missing values](07_missing_values.svg) | Literal missing/exact-empty cells by declared field. |
| [08 - Exact duplicates](08_duplicate_analysis.svg) | Exact-equality duplicate counts; no rows removed. |
| [09 - Source distribution](09_source_distribution.svg) | Top raw `Fact_Check_Source` values. |
| [10 - Raw tokens](10_top_raw_word_tokens.svg) | Top case-preserving `News Body` token forms before processing. |
| [11 - Languages](11_language_distribution.svg) | Source-provided language values. |
| [12 - Categories](12_category_distribution.svg) | Top raw category values, including cached formula values. |
| [13 - Publication years](13_publication_year_distribution.svg) | Conservative parseable-date subset only. |
| [14 - Encoding diagnostic](14_possible_encoding_artifacts.svg) | Isolated text-representation diagnostic indicators; no decoding applied. |

The figures are reproducible through [run_phase_3_4_eda.py](../../../scripts/research/run_phase_3_4_eda.py) and the accompanying [EDA metadata](../../../ml/metadata/bharatfakenewskosh-v1.eda.json).

## Phase 3.8 Evaluation Figures

The following PNG figures are generated from the corrected r2 governed artifacts and aggregate prediction data only. They contain no article/claim text.

| Figure | Purpose |
| --- | --- |
| [Validation Macro F1](phase-3-8-validation-macro-f1.png) | Validation selection metric for all baselines. |
| [Validation ROC curves](phase-3-8-validation-roc-curves.png) | Threshold-independent ranking comparison. |
| [Validation PR curves](phase-3-8-validation-pr-curves.png) | Positive-class ranking under class imbalance. |
| [CV Macro F1 distribution](phase-3-8-cv-macro-f1-distribution.png) | Grouped five-fold training-only variability. |
| [Selected test confusion](phase-3-8-selected-test-confusion.png) | Raw and normalized one-time protected-test confusion matrices. |
| [Feature importance](phase-3-8-feature-importance.png) | Aggregate training-partition linear coefficients; diagnostic only. |
| [Selected test error analysis](phase-3-8-selected-test-error-analysis.png) | Aggregate class and source error rates. |
| [Resource profile](phase-3-8-resource-profile.png) | Local training time and serialized model size. |
