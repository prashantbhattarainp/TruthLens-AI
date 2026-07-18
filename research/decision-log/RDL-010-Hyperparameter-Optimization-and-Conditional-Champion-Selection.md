# RDL-010 - Hyperparameter Optimization and Conditional Champion Selection

**Date:** 2026-07-18  
**Status:** Accepted  
**Phase:** 3.9

## Context

RDL-009 consumed the protected test partition exactly once for the original baseline Linear SVM. The frozen dataset `TL-BFNK-EN-v1.0`, r2 derivative, label mapping, grouped split, preprocessing, and TF-IDF feature configuration therefore had to remain unchanged while the three approved baselines were tuned.

## Decision

1. Tune only Logistic Regression, MNB, and Linear SVM with deterministic `GridSearchCV`, seed 42, Macro F1 scoring, and five-fold `StratifiedGroupKFold` on the training partition.
2. Permit the frozen validation partition only for the post-search comparison. Do not access the protected test partition after tuning.
3. Use a 0.005 validation-Macro-F1 practical-tie band. Resolve ties using grouped OOF Macro F1/stability, MCC, FAKE recall, resource footprint, and generalization gap; never accuracy alone.
4. Register `TL-LSVM-TFIDF-v1.1.0-rc.1` as the conditional champion because it is practically tied with MNB on validation Macro F1 but has higher grouped OOF Macro F1, higher MCC, and lower resource cost.
5. Retain tuned MNB and Logistic Regression as documented challengers. The champion is untested after tuning and cannot be deployed, used as a fact checker, or described as approved.

## Evidence

The candidate artifacts, manifests, OOF predictions, GridSearch results, and deterministic paired comparison reside under `ml/data/optimization/TL-BFNK-EN-v1.0/phase-3-9-r1/`. The governing interpretation is in [the optimization report](../../docs/research/HYPERPARAMETER_OPTIMIZATION_REPORT.md) and [the final selection report](../../docs/research/FINAL_MODEL_SELECTION_REPORT.md).

## Consequences

This decision preserves the protected-test boundary but also means there is no post-tuning test estimate. Any data, preprocessing, feature, threshold, calibration, or candidate change requires a new governed version and a new evaluation plan. No architecture decision is required: the modular experiment framework already supports this bounded search.
