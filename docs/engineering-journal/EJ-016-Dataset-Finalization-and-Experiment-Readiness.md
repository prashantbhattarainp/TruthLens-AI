# EJ-016: Dataset Finalization and Experiment Readiness

**Phase:** 3  
**Milestone:** 3.7.5 - Research Dataset Finalization and Experiment Readiness  
**Date:** 2026-07-18  
**Status:** Complete

## Objective

Resolve the remaining research-governance decisions before data-bearing model evaluation while keeping the raw archive immutable and performing no preprocessing, feature extraction, training, evaluation, optimisation, or deployment.

## Completed work

- Reconciled the acquired release with the official BharatFakeNewsKosh data card and source publication, then froze `LMAP-BFNK-v1.0`: `True -> REAL (0)` and `False -> FAKE (1)`.
- Recorded the public-count versus immutable-release-count divergence without changing either the raw archive or its observed values.
- Defined the English-first `TL-BFNK-EN-v1.0` cohort, source text-unit boundary, translation exclusion, formula-field exclusion, and auxiliary-sheet exclusion.
- Performed a read-only formula and auxiliary-sheet provenance inspection: selected experiment fields have no formulas, and `Sheet1` is an unlabelled auxiliary extract substantially overlapping dfrac.org primary records.
- Defined `DUP-BFNK-v1.0`, including exact conflict exclusion, exact/near duplicate clustering, and cross-dataset handling.
- Froze `SPL-TL-BFNK-EN-v1.0`: 70/15/15 grouped-stratified split, seed 42, source balance audit, date audit-only policy, five-fold grouped CV on the training partition, and one-time test access.
- Added [Dataset Governance](../research/DATASET_GOVERNANCE.md), [Dataset Manifest](../research/DATASET_MANIFEST.md), [Dataset Versioning](../research/DATASET_VERSIONING.md), [Experiment Readiness](../research/EXPERIMENT_READINESS.md), structured manifest metadata, and [RDL-008](../../research/decision-log/RDL-008-Dataset-Finalization-and-Experiment-Readiness.md).

## Deliberately not implemented

- No raw archive extraction, rewrite, cleanup, duplicate removal, preprocessing output, split file, feature matrix, vocabulary, model fit, model evaluation, optimisation, model selection, registry entry, or deployment artifact.
- No FactDrill or COVID-19 dataset acquisition or use.
- No ADR or change to the frontend, backend, FastAPI mock service, public API contract, or service boundary.

## Verification

The raw archive SHA-256 remained `330feb9b24b48f49c4113ca6de87695f1bd0821d29361a86e2b27ab35a77c69c`. The governance contract is consistent with the existing raw validation/EDA evidence and baseline framework safeguards. Data-bearing output directories remain empty.
