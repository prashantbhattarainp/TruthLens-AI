# Hyperparameter Optimization Report

**Milestone:** Phase 3.9  
**Run:** `phase-3-9-r1` (2026-07-18)  
**Dataset:** `TL-BFNK-EN-v1.0`, corrected derivative `DER-20260718-r2`, split `SPL-TL-BFNK-EN-v1.0`

## Protocol and guardrails

Only the approved Logistic Regression, Multinomial Naive Bayes (MNB), and Linear SVM baselines were optimized. Every search used the frozen TF-IDF configuration (`fdec84…648938`), preprocessing configuration `v1.0.0`, seed 42, and five-fold `StratifiedGroupKFold` on the 6,813-document training partition. Duplicate clusters remain grouped inside each fold. The frozen 1,461-document validation partition was used once for the post-search comparison.

The protected 1,458-document test partition was not loaded, predicted, ranked, or used for a tuning, threshold, or candidate decision. Its Phase 3.8 result remains historical evidence for the *untuned* Linear SVM only; it is not evidence for any tuned model.

## Search spaces and results

| Model | Search | Configurations / fits | Best parameters | Train OOF Macro F1 | Validation Macro F1 | Δ validation Macro F1 vs baseline |
| --- | --- | ---: | --- | ---: | ---: | ---: |
| Logistic Regression | GridSearchCV | 24 / 120 | `C=10`, `penalty=l1`, `solver=liblinear`, `class_weight=balanced`, `max_iter=1000` | 0.5394 | 0.5371 | +0.0157 |
| MNB | GridSearchCV | 12 / 60 | `alpha=0.1`, `fit_prior=false` | 0.5269 | **0.5399** | +0.1041 |
| Linear SVM | GridSearchCV | 32 / 160 | `C=0.5`, `loss=squared_hinge`, `dual=false`, `class_weight=None`, `max_iter=5000` | 0.5346 | 0.5398 | +0.0124 |

Macro F1 was the sole search score; the final decision also considers cross-validation stability, held-out validation supporting metrics, resources, and safe-use constraints. Candidate-level artifacts are excluded from Git but are retained under `ml/data/optimization/TL-BFNK-EN-v1.0/phase-3-9-r1/` with manifests and checksums.

## Supporting validation evidence

| Model | FAKE recall | MCC | ROC-AUC | PR-AUC | Validation inference | Train–validation Macro F1 gap |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Logistic Regression | **0.4365** | 0.0743 | 0.5599 | 0.4620 | 163 ms | 0.4524 |
| MNB | 0.4226 | 0.0802 | **0.5652** | **0.4672** | 135 ms | **0.3605** |
| Linear SVM | 0.3183 | **0.1014** | 0.5576 | 0.4641 | **100 ms** | 0.4059 |

All fitted models have large apparent train-to-validation gaps. These figures are a diagnostic for limited generalization and source/template sensitivity, not evidence of a deployment-quality model.

## Paired analysis and interpretation

The deterministic paired analysis used the aligned training out-of-fold predictions only (1,000 bootstrap resamples, seed 42). Logistic Regression and MNB improved materially over their original baselines (paired-fold Macro F1 mean deltas +0.0417 and +0.1016); Linear SVM improved by +0.0023, whose five-fold confidence interval crosses zero. McNemar tests show altered accuracy behavior for all three, but they are supporting tests rather than selection criteria. Five folds are too few to claim conclusive statistical superiority.

The top validation scores are practically tied: MNB exceeds Linear SVM by 0.00013 Macro F1. Linear SVM has a higher OOF Macro F1 (0.5346 vs 0.5269), higher MCC (0.1014 vs 0.0802), the smallest serialized pipeline (0.85 MB), and lowest validation inference time. It is therefore the conditional champion under the documented tie-break rule; MNB remains the principal challenger because it has stronger FAKE recall and validation ranking metrics.

## Risks and next gate

- `penalty` emits a scikit-learn 1.8 deprecation warning for Logistic Regression. The exact environment and configuration are recorded; a future dataset/model version must update the compatible parameter API before upgrading scikit-learn.
- No tuned candidate has a post-tuning protected-test result. Releasing one as production-ready would be unsupported and would violate RDL-009.
- The low absolute scores, English-only frozen cohort, licence restrictions, and source/template sensitivity prohibit factual-verdict claims. Any future release needs new governed data/model versioning, calibration and robustness evidence, and a new protected test set.

## Reproduction

Run `scripts/research/run_phase_3_9_optimization.py` with the pinned local environment, then `scripts/research/generate_phase_3_9_statistical_comparison.py`. Both scripts consume only governed derivative/processed train and validation records; neither accepts a test partition.
