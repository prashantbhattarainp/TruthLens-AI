# EJ-012: Exploratory Data Analysis and Dataset Assessment

**Phase:** 3  
**Milestone:** 3.4 - Exploratory Data Analysis (EDA), Data Profiling and Dataset Assessment  
**Date:** 2026-07-17  
**Status:** Complete

## Objective

Understand the acquired raw dataset and document its statistical, quality, and governance characteristics without preprocessing, cleaning, deduplication, feature work, splitting, notebooks, or model training.

## Completed work

- Ran a reproducible, in-memory, read-only EDA against the immutable BharatFakeNewsKosh v1 ZIP and verified its archive checksum before and after analysis.
- Added aggregate [EDA metadata](../../ml/metadata/bharatfakenewskosh-v1.eda.json) and a read-only [EDA procedure](../../scripts/research/run_phase_3_4_eda.py).
- Created the [EDA Report](../research/EDA_REPORT.md), [Data Profile](../research/DATA_PROFILE.md), [Dataset Statistics](../research/DATASET_STATISTICS.md), [Data Quality Assessment](../research/DATA_QUALITY_ASSESSMENT.md), and [Preprocessing Recommendations](../research/PREPROCESSING_RECOMMENDATIONS.md).
- Generated 14 vector figures in [docs/research/figures](../research/figures/README.md) covering labels, source/workbook composition, text distributions, missingness, exact duplicates, source/language/category distributions, time coverage, raw tokens, and an encoding diagnostic.
- Added [RDL-004](../../research/decision-log/RDL-004-Raw-EDA-and-Data-Readiness-Gate.md) to preserve the data-readiness gate.

## Findings retained without modification

- The declared primary sheet has 26,232 rows, 0 literal missing primary-field values, 0 duplicate IDs, and 0 exact duplicate complete rows.
- Raw label counts remain 15,913 `True` and 10,319 `False`, which still conflict with the public description; no semantic label mapping was made.
- Exact repeated text is material: 1,872 extra duplicate body rows and 858 extra duplicate statement/body-pair rows.
- English is 38.16% of the nine-language corpus; the largest fact-check source contributes 41.56% of rows.
- Nearly half of nonblank publication dates cannot be conservatively parsed, formula-backed fields remain present, and the auxiliary sheet remains undocumented.

## Deliberately not implemented

- No raw archive extraction, modification, resave, or replacement.
- No text preprocessing, decoding, cleaning, category/platform normalisation, label conversion, row deletion, deduplication, or derivative dataset.
- No split, feature engineering, notebook, model, experiment, evaluation, or application-flow change.
- No acquisition of deferred datasets and no ADR.

## Architecture decision assessment

The work adds research evidence, metadata, and static figures only. It changes no architecture, public API, service boundary, runtime, deployment, or deterministic mock prediction flow; no ADR was created.
