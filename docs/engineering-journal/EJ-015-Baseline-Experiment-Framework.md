# EJ-015: Baseline Experiment Framework

**Phase:** 3  
**Milestone:** 3.7 - Baseline Model Development & Experiment Framework  
**Date:** 2026-07-18  
**Status:** Complete

## Objective

Implement a modular, reproducible baseline-model and experiment framework while respecting the existing data-readiness gate.

## Completed work

- Added a closed baseline-model registry/factory for Logistic Regression, Multinomial Naive Bayes, and Linear SVM only.
- Added strict versioned configurations for all three models, with declared hyperparameters, five-fold stratified CV, seed, and Macro F1 metric policy.
- Added deterministic seed management, automatic unique experiment IDs, Stratified K-Fold and optional Stratified Group K-Fold planning, and fold-specific Phase 3.6 feature fitting.
- Added reusable metrics for accuracy, precision, recall, Macro F1, weighted F1, ROC-AUC when a continuous score exists, confusion matrices, and classification reports.
- Added structured experiment records, out-of-fold prediction records, JSONL logs, candidate model-registry records, saved fold models/vectorizers, checksummed artifact manifests, canonical configuration/metrics summaries, classification reports, numeric and PNG confusion matrices, immutable notes, and local experiment-registry sidecars.
- Added command-line raw-path/output-root safeguards plus Git-ignored experiment output/log directories.
- Added seven synthetic fixture tests covering the model allowlist, deterministic five-fold CV, group isolation, all three baselines, automatic IDs, artifacts, dataset-hash validation, and governance safeguards.
- Added [Experiment Framework](../research/EXPERIMENT_FRAMEWORK.md), [Baseline Model Report](../research/BASELINE_MODEL_REPORT.md), [Model Comparison Plan](../research/MODEL_COMPARISON_PLAN.md), [Reproducibility Guide](../research/REPRODUCIBILITY_GUIDE.md), and [RDL-007](../../research/decision-log/RDL-007-Baseline-Experiment-Framework.md).

## Deliberately not implemented

- No BharatFakeNewsKosh raw/processed data read, derivative, label mapping, split, feature artifact, dataset-backed model fit, CV result, validation/test result, comparison table, or model-registry entry.
- No Random Forest, XGBoost, LightGBM, CatBoost, LSTM, BiLSTM, BERT-family, or other unapproved model implementation.
- No calibration, threshold tuning, resampling, external evaluation, explainability, notebook, or prediction-service change.
- No ADR, because this is an internal framework extension below the established service boundary.

## Verification

The seven synthetic experiment-framework tests passed after fitting each allowed baseline against synthetic TF-IDF fixtures. Temporary models and artifacts were removed with their test directories. [experiment-framework-implementation.json](../../ml/metadata/experiment-framework-implementation.json) records the environment and test evidence; the tracked model registry remains empty.
