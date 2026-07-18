# Experiment Readiness: TL-BFNK-EN-v1.0

**Milestone:** Phase 3.7.5, completed by Phase 3.8 execution  
**Status:** Satisfied by governed r2 materialization and baseline evaluation; protected test result is now frozen.

## Readiness decision

RDL-008 resolves the Phase 3.4 governance gate for the narrowly defined `TL-BFNK-EN-v1.0` experiment specification. RDL-009 records the resulting Phase 3.8 decision. Direct raw-file input remains prohibited; the raw archive remains immutable.

The r2 governed derivative reconciles 9,732 included records, 278 excluded conflicting records, and `SPL-TL-BFNK-EN-v1.0` with no duplicate group crossing. The r1 materialization/experiments are retained but invalidated because missing spreadsheet cells were rendered as literal `nan` tokens. The corrected r2 release preserves the frozen cohort and governance rules, and is the sole evidence-bearing release.

The next authorised data-bearing workflow must first materialize the documented English cohort and immutable split manifest. It may then use the existing Phase 3.5 preprocessing pipeline, Phase 3.6 TF-IDF feature pipeline, and Phase 3.7 baseline experiment runner. No model evaluation, optimisation, production deployment, or mock-service replacement occurs in this milestone.

## Preconditions satisfied

| Requirement | Status | Evidence |
| --- | --- | --- |
| Exact primary source release and hash | Frozen | [Dataset Manifest](DATASET_MANIFEST.md) |
| Semantic binary mapping | Frozen | `LMAP-BFNK-v1.0`; `True -> REAL (0)`, `False -> FAKE (1)` |
| English text-unit and translation boundary | Frozen | Raw `Language == "English"`; source text fields only |
| Formula and auxiliary-sheet handling | Resolved by exclusion | Selected fields have no formulas; `Sheet1`/`Sheet3` are outside the population |
| Duplicate and conflict policy | Frozen | `DUP-BFNK-v1.0` |
| Source and temporal leakage policy | Frozen | Source/date audit-only; duplicate groups are partition-atomic |
| Train/validation/test plan | Frozen | `SPL-TL-BFNK-EN-v1.0`, 70/15/15, seed 42 |
| Preprocessing configuration | Frozen | `conservative-en-v1.json` / pipeline `1.0.0` |
| Baseline feature configuration | Frozen | `tfidf-unigram-bigram-v1.json` / pipeline `1.0.0` |
| Research-use licence boundary | Recorded | CC BY-NC 4.0; no deployment/commercial inference |

## Required execution order

1. Verify the raw archive and workbook hashes against [Dataset Manifest](DATASET_MANIFEST.md).
2. Generate the new governed derivative from the frozen cohort and mapping rules, including the exact-pair conflict exclusions. Do not overwrite or alter raw data.
3. Run and record `DUP-BFNK-v1.0`; assign duplicate clusters, validate that no cluster crosses partitions, and create `SPL-TL-BFNK-EN-v1.0`.
4. Reconcile all row, class, source, duplicate, and exclusion counts to the frozen manifest; halt on mismatch.
5. Apply the frozen preprocessing configuration only to the derived train/validation/test records. Preserve output manifests, configuration hashes, failures, and raw-parent lineage.
6. Fit TF-IDF on training text only. Keep validation and test text outside vocabulary/IDF fitting.
7. Run only the approved baselines with the data-specific grouped-CV configuration. The test partition is inaccessible until model/configuration selection is frozen.

## Evaluation guardrails for the next milestone

- The 15% test partition is not an input to cross-validation, feature fitting, hyperparameter selection, threshold selection, calibration, error-driven configuration changes, or model choice.
- Five-fold grouped stratified CV uses only the frozen training partition and the duplicate group IDs. Existing generic `*-v1.json` experiment configurations are fixture-framework configurations; data-bearing runs use the new `*-bfnk-en-v1.json` grouped-CV counterparts.
- Macro F1 remains primary. Every result reports the dataset, mapping, split, preprocessing, feature, model, and environment identities.
- Source and date fields remain out of the vectorizer. Results are in-domain English Indian fact-checked-news results only; they do not prove unseen-source, temporal, multilingual, or general fact-checking performance.
- FactDrill and the COVID-19 dataset remain unavailable to training, validation, selection, and comparison. No cross-dataset result is permitted under this dataset version.

## Stop conditions

Stop and mark the planned run invalid if the raw hash differs, raw labels are not exactly the mapped values, a selected field becomes formula-backed, an auxiliary-sheet row is included, exact conflict exclusions do not reconcile, a duplicate cluster crosses a partition, an unapproved configuration is used, or a required manifest/checksum is absent.
