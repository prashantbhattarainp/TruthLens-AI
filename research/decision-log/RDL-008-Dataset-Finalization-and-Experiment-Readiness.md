# RDL-008: Dataset Finalization and Experiment Readiness

**Status:** Accepted for Phase 3.7.5  
**Date:** 2026-07-18  
**Related documents:** [Dataset Governance](../../docs/research/DATASET_GOVERNANCE.md), [Dataset Manifest](../../docs/research/DATASET_MANIFEST.md), [Dataset Versioning](../../docs/research/DATASET_VERSIONING.md), [Experiment Readiness](../../docs/research/EXPERIMENT_READINESS.md)

## Context

RDL-004 appropriately blocked data-bearing activity after raw EDA identified label-count disagreement, formula-backed fields, undocumented auxiliary content, repeated text, source concentration, and incomplete time parsing. Phase 3.7.5 is expressly authorised to resolve those governance choices without running preprocessing, feature extraction, training, evaluation, optimisation, or deployment.

## Decisions

1. Freeze `TL-BFNK-EN-v1.0` as the sole primary Phase 3 research-dataset specification. It is anchored to DSR-001's immutable BharatFakeNewsKosh Kaggle v1 archive and its recorded SHA-256 values. DSR-002 and DSR-003 remain deferred and are not merged, trained on, or evaluated.
2. Adopt `LMAP-BFNK-v1.0`: raw `True` maps to REAL = 0 and raw `False` maps to FAKE = 1. This follows the source data card/publication definitions. The release-specific archive counts are authoritative for this version; the public count discrepancy is retained as a documented metadata divergence.
3. Limit the cohort to worksheet `A`, raw `Language == "English"`, and original `Statement` plus `News Body` fields. Exclude translation fields, `Sheet1`, and `Sheet3`. The selected text, label, identity, source, and date fields have no formula cells; formula-backed fields are outside model input and eligibility.
4. Adopt `DUP-BFNK-v1.0`. Exact conflicting text-pair clusters are excluded; all other exact/near-duplicate clusters are retained as partition-atomic groups. Cross-dataset duplicates are prohibited from pooled data and require a new versioned review.
5. Freeze `SPL-TL-BFNK-EN-v1.0`: 70% train, 15% validation, 15% test, seed 42, binary stratification, and duplicate-group atomicity. Source counts are audited after allocation but source is neither a feature nor a primary-split allocation constraint; no held-out-source generalisation claim is authorised. Dates remain audit-only; no temporal split or temporal claim is authorised.
6. Freeze the conservative preprocessing and TF-IDF baseline configuration identities. Data-bearing baseline CV uses five-fold `stratified_group_kfold` on the training partition only; model selection and test access are separated.
7. Require a new version for any change to source/hash, cohort, mapping, duplicates, grouping, source/time policy, split, licence interpretation, or representation configuration. Preserve invalidated artifacts and manifests.
8. Resolve RDL-004's DSR-001 Phase 3 readiness gate only for this exact version and controlled materialization path. Direct raw-file processing remains prohibited, and no result or model registry entry exists until a later data-bearing experiment completes.

## Consequences

- Future Phase 3 execution has a reviewable, reproducible input contract without guessing label semantics or using auxiliary/translated content.
- The data count discrepancy, source concentration, short body-field limitation, and date limitations remain reportable threats to validity; they are not silently removed.
- The existing preprocessing, feature, and experiment packages can consume a later governed derivative without changing the frontend, backend, ML-service boundary, or deterministic mock inference path.

## Architecture impact

None. This is a dataset-governance and experiment-readiness decision. No public API, service boundary, deployment topology, runtime architecture, or mock inference behavior changes; no ADR is created.
