# Model Comparison Plan

**Status:** Design only. No dataset-backed baseline comparison has been performed.

## Comparison set

The first governed comparison contains exactly Logistic Regression, Multinomial Naive Bayes, and Linear SVM using the same approved Phase 3.6 sparse feature configuration. Each model is configured separately and receives a distinct automatically generated experiment ID.

## Controlled conditions

For results to be comparable, every candidate must share:

1. The same approved dataset derivative, label mapping, cohort definition, and raw-parent lineage.
2. The same frozen split manifest, duplicate/group rule, and training partition.
3. The same preprocessing configuration and feature configuration/version, unless the study explicitly evaluates a feature-method change as a separate cohort.
4. The same five-fold stratified-group CV policy where groups are available; a plain stratified CV exception must be documented.
5. Training-only fitting of feature vocabulary/IDF, class-weight policy, seed strategy, metrics configuration, code/environment evidence, and reporting template.

## Selection evidence

Macro F1 is the primary selection metric. Each candidate additionally reports accuracy, positive-class precision and recall, weighted F1, ROC-AUC when it has a continuous score, confusion matrix, full classification report, per-fold timings, and aggregate out-of-fold predictions. Linear SVM decision scores are suitable for ROC-AUC ranking but are not calibrated probabilities.

Candidate selection after cross-validation must be confirmed according to the frozen validation protocol. The held-out test partition remains inaccessible until selection/configuration freeze. A score difference alone is insufficient: class-wise failure, resource use, leakage-audit status, data scope, and later error/cohort analysis remain required evidence.

## Non-comparability and stop conditions

Do not rank runs together if data lineage, split, labels, feature fitting scope, preprocessing, feature configuration, metric definition, or model protocol differs. Stop and record the experiment as invalid if a derivative/split lacks evidence, feature fitting includes held-out rows, group leakage is detected, labels are unresolved, or required artifacts/checksums are missing.

No baseline is selected in Phase 3.7.5. The plan becomes executable only after the frozen `TL-BFNK-EN-v1.0` derivative and `SPL-TL-BFNK-EN-v1.0` split manifest are materialized and verified.
