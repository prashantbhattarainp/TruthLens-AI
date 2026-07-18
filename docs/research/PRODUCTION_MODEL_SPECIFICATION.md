# Production Model Specification

## Conditional candidate definition

| Item | Specification |
| --- | --- |
| Candidate ID | `TL-LSVM-TFIDF-v1.1.0-rc.1` |
| Algorithm | `sklearn.svm.LinearSVC`, linear decision function; binary label `0=REAL`, `1=FAKE` |
| Feature representation | Frozen TF-IDF word unigrams/bigrams; 20,000-feature cap; training-fitted vocabulary only |
| Hyperparameters | `C=0.5`, `loss=squared_hinge`, `dual=false`, `class_weight=None`, `max_iter=5000`, seed 42 |
| Data lineage | `TL-BFNK-EN-v1.0`, `DER-20260718-r2`, `SPL-TL-BFNK-EN-v1.0`; train 6,813 / validation 1,461 |
| Artifact | Governed `fitted-validation-candidate.joblib` beside `OPT-20260718-linear-svm-faafafe15e` |
| Validation evidence | Macro F1 0.5398, MCC 0.1014, FAKE recall 0.3183, 100 ms validation-batch inference |

## Operational contract

If a future release gate authorizes integration, it must preserve input size/encoding checks, the exact preprocessing and TF-IDF artifacts, deterministic version logging, and a clearly worded uncertainty-oriented output. A Linear SVM decision score is **not a calibrated probability**; it must not be displayed as a confidence percentage without separately approved calibration evidence.

The model must not be represented as a fact-checker, a detector of factual truth, or reliable outside its English BFNK-derived research scope. It requires human review for consequential use and must retain the dataset licence/attribution constraints.

## Non-approval

This specification is a production-candidate definition only. Deployment is prohibited because the tuned candidate has not received a new protected-test evaluation, absolute performance is weak, and Phase 3.8 analysis identified source/template sensitivity. The existing application continues to use deterministic mock predictions.
