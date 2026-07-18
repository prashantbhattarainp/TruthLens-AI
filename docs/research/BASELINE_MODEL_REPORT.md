# Baseline Model Report

**Phase:** 3 - Milestone 3.7  
**Report type:** Framework and synthetic-fixture verification report; not a BharatFakeNewsKosh result.

## Implemented baselines

| Model | Registry key | Versioned configuration | Role |
| --- | --- | --- | --- |
| Logistic Regression | `logistic_regression` | [`logistic-regression-v1.json`](../../ml/config/experiments/logistic-regression-v1.json) | Regularized linear probabilistic baseline. |
| Multinomial Naive Bayes | `multinomial_naive_bayes` | [`multinomial-naive-bayes-v1.json`](../../ml/config/experiments/multinomial-naive-bayes-v1.json) | Sparse nonnegative lexical baseline. |
| Linear SVM | `linear_svm` | [`linear-svm-v1.json`](../../ml/config/experiments/linear-svm-v1.json) | Linear margin-based sparse-feature baseline. |

The model registry is intentionally closed. Random Forest, XGBoost, LightGBM, CatBoost, recurrent networks, and transformer models are not implemented, registered, downloaded, or selectable by the factory.

## Feature protocol

All three models receive sparse features through the Phase 3.6 `FeaturePipeline`. The runner instantiates a fresh TF-IDF/Count pipeline per training fold, fits it only on that fold's training text, then transforms the held-out fold. This gives every baseline the same feature configuration in a given experiment while preventing vocabulary/IDF leakage.

## Configuration identities

| Configuration | SHA-256 |
| --- | --- |
| Logistic Regression v1 | `d50e9fceab2b3536199de20699ac84282a8304394b9a2e966199a1c59e7dcf79` |
| Multinomial Naive Bayes v1 | `8be45037b31e80bc1d452b1fa99f75d4826861b17a5cd5255af06588eb4aa8b6` |
| Linear SVM v1 | `eb4960b05c903b5ac5a9ee7c68b610e675d7e7bc5ec7d80675525cd835282d28` |

Each baseline configuration declares its hyperparameters, five-fold cross-validation policy, random seed (`42`), and metric policy. Configuration loading and unsupported model selection fail explicitly.

## Synthetic verification only

The synthetic fixture suite fit and cross-validated each of the three baselines with the Phase 3.6 TF-IDF implementation, generated temporary candidate records and artifacts, and verified continuous-score ROC-AUC handling for all three. These tests establish plumbing, not research performance. No numerical fixture score is reported as a benchmark, and no candidate is registered in the project model registry.

## Not implemented

- No BharatFakeNewsKosh model training, cross-validation, validation-set evaluation, held-out test evaluation, model comparison result, or deployable model.
- No class weighting, resampling, threshold tuning, calibration, external evaluation, error analysis, or explainability result.
- No unapproved model family.

RDL-008 froze the governance contract and Phase 3.8 subsequently exercised the approved baselines on corrected governed derivative r2. The result-bearing evidence, limitations, and selected research candidate are recorded in [Model Evaluation Report](MODEL_EVALUATION_REPORT.md); this implementation report remains the baseline design reference.
