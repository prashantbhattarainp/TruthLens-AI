# Multilingual Error Analysis - Phase 4.4

## Method

Errors are evaluated only on the frozen validation partition. False positive means a REAL-labelled derivative record predicted FAKE; false negative means a FAKE-labelled record predicted REAL. Cohorts overlap and are descriptive text heuristics, never topic labels or factual determinations. No raw text, score, or document identifier is stored in the tracked report.

## Error counts

| Appearance slice | False positives | False negatives | Short FP / FN | Long FP / FN | Political FP / FN | Health FP / FN | Social-media FP / FN | Named entity/acronym FP / FN | Transliterated FP / FN |
| --- | ---: | ---: | --- | --- | --- | --- | --- | --- | --- |
| Full frozen validation | 201 | 392 | 19 / 60 | 26 / 48 | 63 / 113* | 28 / 55* | Not previously recorded | Not previously recorded | Not applicable |
| English/unclassified | 198 | 391 | 19 / 60 | 25 / 48 | 52 / 98 | 23 / 49 | 102 / 174 | 112 / 206 | Not applicable |
| Devanagari-bearing | 2 | 1 | 0 / 0 | 1 / 0 | 1 / 1 | 0 / 0 | 2 / 0 | 2 / 0 | Not applicable |
| Hinglish heuristic | 1 | 0 | 0 / 0 | 0 / 0 | 1 / 0 | 0 / 0 | 0 / 0 | 1 / 0 | 1 / 0 |

\* These are the established Phase 4.3 all-validation cohort counts. The Phase 4.4 multilingual cohort definition adds social-media and named-entity/acronym heuristics, so those columns are intentionally not retrospectively reconstructed for the full-validation row.

## Reading the slices safely

The 9-record Devanagari-bearing and 2-record Hinglish-heuristic samples are too small to support a pattern claim. They are retained to identify where a future corpus needs coverage: transliterated grammar, named entities/acronyms, political references, health claims, and social-media styling. The Hinglish observation is one REAL-labelled record predicted FAKE; it is not evidence about Hinglish false-positive rate.

The majority English/unclassified slice mirrors the incumbent’s existing asymmetry: 391 false negatives versus 198 false positives. That remains an English validation limitation. Across all slices, a model output is a bounded research signal, not a verdict about a claim, person, organisation, or language community.

## Future error-review requirements

For a governed multilingual corpus, error review should pre-register language-aware political and health term lists, annotate social-media/style and named-entity handling transparently, preserve language/mix annotations without exposing raw text in reports, and assess false-positive/false-negative burdens with adequate sample sizes. Any operational use also needs human review and the existing calibration, robustness, rights, and monitoring gates.
