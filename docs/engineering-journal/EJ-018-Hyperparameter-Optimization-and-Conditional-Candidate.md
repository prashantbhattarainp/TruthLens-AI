# EJ-018 - Hyperparameter Optimization and Conditional Candidate

**Date:** 2026-07-18  
**Milestone:** Phase 3.9

## Completed work

- Added the modular `ml/src/optimization/` package with configuration validation, grouped-CV `GridSearchCV` runner, artifact writer, and explicit absence of a test-data input.
- Added versioned search configurations for only the approved Logistic Regression, MNB, and Linear SVM models.
- Ran 24, 12, and 32 bounded configurations respectively against the governed r2 training partition, then compared each fitted winner once on frozen validation.
- Persisted local manifests, best parameters, complete search tables, OOF predictions, candidate artifacts, resource evidence, and deterministic paired comparisons under the Phase 3.9 artifact root.
- Recorded the conditional champion/challenger decision, versioning rules, and production-candidate non-approval boundary. Updated experiment/model registries and project research documentation.

## Verification

The optimization runner enforces frozen TF-IDF, seed 42, five folds, grouped CV, matching baseline model configuration, non-empty binary grouped records, and train/validation separation. The run did not load or predict the protected test partition. Search result artifacts report Linear SVM as the conditional champion (`OPT-20260718-linear-svm-faafafe15e`).

## Important observations

All three tuned candidates retain weak absolute performance and substantial train-to-validation gaps. The very small MNB/SVM validation difference is not treated as decisive; the selected SVM is a conditional research candidate only. A Logistic Regression API deprecation warning from scikit-learn 1.8 was observed and recorded for future environment maintenance. No ADR was added because the established modular experiment architecture was extended without an architectural change.

## Next boundary

Phase 3.9 stops here. No protected-test reuse, model deployment, calibration, threshold optimization, or further model evaluation is authorized without approval and new governance evidence.
