# EJ-017: Baseline Model Evaluation and Candidate Selection

**Phase:** 3  
**Milestone:** 3.8 — Model Evaluation, Comparison & Candidate Selection  
**Date:** 2026-07-18  
**Status:** Complete

## Completed work

- Materialized the RDL-008 governed dataset derivative and atomic duplicate-group split from the immutable BharatFakeNewsKosh archive; verified cohort counts and no duplicate group crossing.
- Ran conservative spaCy preprocessing and training-only TF-IDF feature extraction with zero preprocessing failures and zero empty feature vectors.
- Extended the reusable experiment metric bundle with macro/weighted precision and recall, balanced accuracy, PR-AUC, log loss where probability scores exist, MCC, Cohen's kappa, and normalized confusion matrices.
- Completed grouped five-fold CV for Logistic Regression, Multinomial NB, and Linear SVM using only the frozen training partition.
- Performed validation-led candidate selection, then a single protected test evaluation after train+validation refit. Linear SVM was selected as a research candidate.
- Added aggregate-only ROC, PR, confusion-matrix, feature-importance, error-slice, CV-variability, and resource figures; added paired statistical evidence, registries, and Phase 3.8 reports.

## Corrected artifact release

The first controlled derivative r1 represented missing spreadsheet cells as literal `nan` because of pandas string conversion. It was preserved and invalidated. Corrected r2 represents missing cells as empty source text; source archive, cohort count, labels, duplicate policy, split policy, seed, configuration hashes, and dataset version remain unchanged. All recorded results use r2 only.

## Deliberately not implemented

- No hyperparameter optimisation, threshold tuning, calibration, resampling, neural model, transformer, external-dataset evaluation, deployment, or public inference-path change.
- No raw-data modification, raw-text report export, duplicate removal, or frontend/backend/ML-service integration.

## Outcome

Linear SVM is registered as an evaluated research candidate only. Its test Macro F1 is 0.5486 and FAKE recall is 0.3805; source/template sensitivity and error asymmetry make it unsuitable for deployment. The milestone stops here pending approval for Phase 3.9.
