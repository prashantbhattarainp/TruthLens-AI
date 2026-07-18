# Final Model Selection Report

## Decision

`TL-LSVM-TFIDF-v1.1.0-rc.1` is selected as the **conditional Phase 3.9 champion**. It is a research production candidate definition, not an approved production deployment, fact-checker, or newly test-evaluated model.

| Field | Value |
| --- | --- |
| Algorithm | Linear SVM with frozen TF-IDF word unigram/bigram representation |
| Optimization record | `OPT-20260718-linear-svm-faafafe15e` |
| Dataset / split | `TL-BFNK-EN-v1.0` / `SPL-TL-BFNK-EN-v1.0` |
| Best parameters | `C=0.5`, `loss=squared_hinge`, `dual=false`, `class_weight=None`, `max_iter=5000` |
| Seed / CV | 42 / five-fold `StratifiedGroupKFold` on training only |
| OOF Macro F1 | 0.5346 |
| Frozen validation Macro F1 / MCC | 0.5398 / 0.1014 |
| Artifact | `ml/data/optimization/TL-BFNK-EN-v1.0/phase-3-9-r1/OPT-20260718-linear-svm-faafafe15e/fitted-validation-candidate.joblib` |
| Status | Conditional champion; untested after tuning |

## Rationale

MNB achieved the numerically highest validation Macro F1 (0.5399), but its advantage over Linear SVM (0.00013) is below the 0.005 practical-tie margin. In the tied set, Linear SVM has the stronger grouped training OOF Macro F1 (0.5346), higher validation MCC (0.1014), smaller artifact, and lower inference time. The decision does not use accuracy as a tie-breaker. Logistic Regression has the highest OOF Macro F1 (0.5394) and FAKE recall (0.4365), but lower held-out Macro F1, lower MCC, and the largest train–validation gap.

## Challenger disposition

| Candidate | Role | Reason retained |
| --- | --- | --- |
| Tuned MNB `v1.1.0` | Primary challenger | Near-tied validation Macro F1; better FAKE recall, ROC-AUC, PR-AUC, and smallest generalization gap. |
| Tuned Logistic Regression `v1.1.0` | Fairness/recall challenger | Highest FAKE recall and OOF Macro F1; investigate only under a new approved protocol. |
| Phase 3.8 baseline Linear SVM `v1.0.0` | Historical comparator | Only candidate with a one-time protected-test result, but it was not tuned and cannot be compared as post-tuning evidence. |

## Selection limits

No further test access is authorized for this model version. Threshold optimization, calibration, retraining, data changes, or a new candidate comparison require a new governed dataset/model version and a fresh protected test plan. The result is restricted to reproducible research comparison; it must not produce factual truth verdicts or claims of broad Indian-media reliability.
