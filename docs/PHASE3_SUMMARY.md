# Phase 3 Summary

## Completed milestones

Phase 3.1 established methodology; 3.2 screened datasets; 3.3 acquired and validated raw data; 3.4 profiled it; 3.5 implemented preprocessing; 3.6 implemented features; 3.7 implemented baseline experiments; 3.7.5 froze the governed cohort and split; 3.8 evaluated the original baselines; 3.9 tuned only the approved baselines; and 3.10 packaged and integrated the conditional champion.

## Lessons learned

- Dataset versioning, duplicate grouping, and test-access controls are required before metric comparison is meaningful.
- The r1 literal-`nan` defect reinforced why governed derivatives and immutable records matter.
- Tuning raised validation results, but small differences and large train–validation gaps do not support broad performance claims.
- An uncalibrated Linear SVM must not expose a decision margin as user confidence.

## Final architecture and model

The final Phase 3 architecture is frontend → Node backend → Python ML microservice → immutable candidate package. The current package is `TL-LSVM-TFIDF-v1.1.0-rc.1`, backed by `TL-BFNK-EN-v1.0`, `DER-20260718-r2`, and `SPL-TL-BFNK-EN-v1.0`.

## Remaining work and Phase 4 readiness

Phase 4 can build product analytics and operational controls on the stable API. Before public deployment or consequential decision support, obtain a new data/model version and independently approve post-tuning evaluation, calibration, fairness/robustness tests, licence/deployment review, monitoring thresholds, incident response, and human-review workflows.
