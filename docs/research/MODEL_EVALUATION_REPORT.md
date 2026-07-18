# Phase 3.8 Baseline Model Evaluation Report

**Status:** Complete — research candidate only; not deployment approval  
**Dataset:** `TL-BFNK-EN-v1.0`, governed derivative `DER-20260718-r2`  
**Split:** `SPL-TL-BFNK-EN-v1.0` (seed 42; grouped 70/15/15)  
**Primary metric:** Macro F1  
**Selected candidate:** Linear SVM v1.0.0

## Protocol and lineage

Only the frozen English BharatFakeNewsKosh cohort was used: 9,732 records after the documented exclusion of 278 conflicting exact-pair records. The materialized r2 split contains 6,813 train, 1,461 validation, and 1,458 test records; duplicate groups do not cross partitions. The conservative spaCy preprocessing configuration (`52ce…3976f`) completed with 0 failures and 0 empty documents. TF-IDF unigram/bigram features (`fdec…4938`, 20,000 training-fitted features) were used for every baseline.

Logistic Regression, Multinomial Naive Bayes, and Linear SVM were evaluated with five-fold `stratified_group_kfold` on the training partition only. All three candidates were then fitted on train and evaluated on validation. Linear SVM was selected solely by validation Macro F1; it was refitted once on train+validation and evaluated once on the protected test partition. No threshold tuning, hyperparameter optimisation, or repeated test access occurred.

The first Phase 3.8 materialization (`r1`) rendered missing spreadsheet cells as the literal token `nan`. It was retained and invalidated; r2 corrects that implementation defect by rendering missing source text as an empty string. Cohort membership, label mapping, duplicate policy, split policy, seed, and frozen dataset version did not change.

## Cross-validation comparison

| Model | Accuracy | Macro F1 | Weighted F1 | FAKE recall | ROC-AUC | PR-AUC | Train time (5 folds) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Logistic Regression | 0.6168 | 0.4976 | 0.5500 | 0.1651 | 0.5531 | 0.4682 | 479 ms |
| Multinomial NB | 0.6157 | 0.4251 | 0.4960 | 0.0508 | 0.5452 | 0.4507 | 36 ms |
| Linear SVM | 0.5740 | **0.5323** | 0.5622 | **0.3504** | 0.5433 | 0.4510 | 860 ms |

Higher accuracy for Logistic Regression and Multinomial NB is driven by their strong REAL bias. Macro F1 and FAKE recall expose this imbalance, which is why accuracy was not used as the selection metric.

## Validation selection and protected test result

| Model | Validation accuracy | Validation Macro F1 | Validation FAKE recall |
| --- | ---: | ---: | ---: |
| Logistic Regression | 0.6304 | 0.5215 | 0.1948 |
| Multinomial NB | 0.6140 | 0.4358 | 0.0661 |
| Linear SVM | 0.5722 | **0.5274** | **0.3357** |

The selected Linear SVM was refitted on 8,274 train+validation records and evaluated once on 1,458 protected-test records.

| Test metric | Value |
| --- | ---: |
| Accuracy | 0.5857 |
| Macro / weighted F1 | **0.5486** / 0.5763 |
| Balanced accuracy | 0.5495 |
| FAKE precision / recall / F1 | 0.4668 / 0.3805 / 0.4192 |
| REAL precision / recall / F1 | 0.6418 / 0.7186 / 0.6780 |
| ROC-AUC / PR-AUC | 0.5780 / 0.4778 |
| MCC / Cohen's kappa | 0.1037 / 0.1024 |

The raw test confusion matrix is `[[636, 249], [355, 218]]` for REAL/FAKE rows and columns. Linear SVM has no calibrated probability output, so log loss is intentionally not reported.

## Interpretation and disposition

Linear SVM is the Phase 3.8 **evaluated research candidate** because it gave the best validation Macro F1 and materially higher FAKE recall than the other approved baselines. Its protected-test Macro F1 of 0.5486 and MCC of 0.1037 are modest. It must not be presented as a fact-checker, production model, or generally valid Indian-media detector.

The model's feature weights and error profile reveal source/text-template sensitivity, a 61.95% error rate for FAKE test records, and uncertainty for small sources. These are release-blocking limitations for deployment and motivate the next research-only comparison milestone.

## Evidence and figures

- [Model comparison](MODEL_COMPARISON.md), [statistical analysis](STATISTICAL_ANALYSIS.md), [error analysis](ERROR_ANALYSIS.md), and [feature-importance analysis](FEATURE_IMPORTANCE_ANALYSIS.md).
- [Validation Macro F1](figures/phase-3-8-validation-macro-f1.png), [ROC curves](figures/phase-3-8-validation-roc-curves.png), [PR curves](figures/phase-3-8-validation-pr-curves.png), [CV distribution](figures/phase-3-8-cv-macro-f1-distribution.png), [test confusion matrices](figures/phase-3-8-selected-test-confusion.png), [feature coefficients](figures/phase-3-8-feature-importance.png), [error slices](figures/phase-3-8-selected-test-error-analysis.png), and [resource profile](figures/phase-3-8-resource-profile.png).
- Checksummed r2 artifacts are retained below `ml/data/derived/`, `ml/data/processed/`, `ml/data/features/`, `ml/data/experiments/`, and `ml/data/evaluation/`; these paths are intentionally ignored by Git because they contain governed data/model artifacts.
