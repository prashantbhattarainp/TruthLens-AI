# RDL-014 - Ensemble Evaluation and Validation-Only Boundary

**Date:** 2026-07-18  
**Status:** Accepted  
**Phase:** 4.3

## Decision

Phase 4.3 may combine the immutable Phase 3.9 LinearSVC, MultinomialNB, and Logistic Regression candidate artifacts into research-only ensembles using the existing frozen derivative `DER-20260718-r2`. Every base pipeline receives the same frozen preprocessing and the frozen validation partition only. The protected test is not transformed, predicted, labelled for a model, or used to select an ensemble.

The pre-specified variants are: three-component hard voting; three-component weighted hard voting with normalized train-only grouped-OOF Macro F1 weights; two-component soft voting using MultinomialNB and Logistic Regression FAKE-class probabilities; and a Logistic Regression stacker trained only on aligned base-model OOF scores from the frozen training partition. LinearSVC is excluded from soft voting because its margin is not a calibrated probability. Its clipped sigmoid mapping is permitted only as a bounded stacking feature and is not confidence or calibration evidence.

Blending is excluded because the frozen protocol has no independent blend-development partition. A classical-transformer hybrid is excluded because Phase 4.2 has no completed transformer prediction artifact. Neither exclusion is treated as a negative performance result.

## Champion-challenger consequence

Every evaluated ensemble is a validation-only research challenger. No validation result, including a result above an incumbent metric, can automatically replace `TL-LSVM-TFIDF-v1.1.0-rc.1`. The incumbent remains integrated, uncalibrated, untested after tuning, and not deployment-approved. Promotion remains subject to separately approved repeatability, evaluation, calibration, robustness/fairness, rights, operational, monitoring, and human-review gates.

## Architecture consequence

This phase adds no prediction-service path, public API field, package replacement, or trust-boundary change. ADR-009 and ADR-010 remain sufficient; no new ADR is required.
