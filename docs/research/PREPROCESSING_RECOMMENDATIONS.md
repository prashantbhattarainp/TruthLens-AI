# Preprocessing Recommendations

**Status:** Phase 3.5 implements the configurable pipeline and its fixture tests, but no preprocessing has been run on BharatFakeNewsKosh. No cleaning, decoding, deduplication, label conversion, feature engineering, split, notebook, or model has been implemented on the dataset.

The implementation and conservative configuration are documented in [Preprocessing Pipeline](PREPROCESSING_PIPELINE.md) and [Preprocessing Configuration](PREPROCESSING_CONFIGURATION.md). They do not clear the readiness gates below.

## Mandatory readiness gates

1. Reconcile the raw label counts with the source release and document the creator-defined meaning of `True` and `False`.
2. Approve a source-label mapping register before assigning the project's REAL/FAKE values. Preserve `Label` verbatim in every later derivative.
3. Establish the provenance of formula-backed fields and the purpose of `Sheet1`; decide whether cached values are permitted in a derivative without editing the workbook.
4. Define the task unit. The `News Body` field is populated but compact, so it must not be presumed to be a full article. For the primary claim, verify native-English eligibility rather than using translation fields as a silent substitute.
5. Approve an exact and near-duplicate method, a source/group rule, and a temporal policy before generating any split.

## Future derivative recommendations

| Recommended future action | Why | Governance condition |
| --- | --- | --- |
| Create a new versioned working copy from the immutable archive | Raw data must remain authoritative and unchanged. | Parent hash, source member, code revision, configuration hash, and row accounting recorded. |
| Retain every raw field beside any canonical field | Category/platform spelling and case variants are evidence, not errors to overwrite. | Raw column remains immutable; canonical map has a version, evidence, and reviewer. |
| Apply a reviewed language/text-unit inclusion rule | English is only 38.16% of raw rows, and original/translation fields must not be conflated. | Rule states source language, native/translation treatment, inclusion counts, and exclusions. |
| Validate encoding on the selected text field | The container is structurally healthy and only two isolated diagnostic flags were found. | Any decode/repair must be demonstrably necessary, deterministic, reversible from raw, and separately reviewed. |
| Treat nonblank placeholders separately from literal missingness | Literal missingness is zero, but raw category values include items such as `NA`; cell presence is not semantic completeness. | Placeholder lexicon and treatment are documented without overwriting raw values. |
| Form exact and near-duplicate clusters | Exact body and text-pair repetition can leak across partitions. | Method, thresholds, language handling, cluster IDs, and partition restriction are versioned. |
| Standardise date representation only after format review | 12,504 nonblank dates are not safely parsed by the conservative rule. | Parser/version, ambiguity rule, failures, timezone/precision, and before/after counts are recorded. |
| Standardise category/platform/source vocabularies only for analysis | Raw variants otherwise fragment cohort counts. | Mapping is provenance-preserving; unknown values remain explicit rather than inferred. |
| Apply minimal text processing only after the above gates | Tokenisation, case handling, URLs, punctuation, numbers, named entities, negation, and Indic scripts can change model behaviour. | Frozen configuration, tests, before/after counts, language-specific justification, and experiment linkage required. |

## Recommended sequence

1. Approve the label, worksheet, text-unit, formula, and date decisions.
2. Produce a manifest-backed derivative with raw-to-derived row accounting and no silent exclusions.
3. Run duplicate clustering and source/time leakage checks on that derivative.
4. Freeze the approved inclusion and group rules, then create the split manifest.
5. Only then evaluate a minimal, configurable preprocessing policy on the frozen development workflow.

Any future preprocessing must preserve names, numbers, negation, URLs, and Indian-language script content unless a documented experiment demonstrates a justified alternative. It must never replace or overwrite the archived raw release.
