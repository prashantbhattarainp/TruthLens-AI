# Production Deployment Impact - Phase 4.3

## Resource comparison

| Item | Observed Phase 4.3 evidence |
| --- | --- |
| Base refit time | LinearSVC 911 ms; MultinomialNB 978 ms; Logistic Regression 1,348 ms (historical Phase 3.9 artifacts) |
| Component package sizes | 0.81 MiB, 1.27 MiB, 0.81 MiB; 2.90 MiB combined before preprocessing/XAI assets |
| Stacking meta-model | 895 bytes; 8.1 ms fit on 6,813 OOF rows |
| Validation preprocessing | 3.47 s for 1,461 records in the benchmark process |
| Component validation inference | 126 ms LinearSVC; 140 ms MultinomialNB; 137 ms Logistic Regression |
| Ensemble aggregation + stacker inference | 84 ms for 1,461 records |
| Process RSS change | 148.4 MB before component load to 368.9 MB after evaluation (host/process observation, not a deployment sizing guarantee) |

## Operational conclusion

An ensemble requires three vectorizers/classifiers, duplicate preprocessing/vectorization work in the research harness, more artifact integrity checks, component failure handling, version alignment, and an explanation strategy. Its small Macro F1 improvement does not offset those operational costs for the current internal service. The existing LinearSVC remains simpler to package, serve, monitor, and explain.

Soft-vote and stacking scores must not be exposed as calibrated user confidence. No ensemble is deployed, production-approved, or added to the FastAPI/Node architecture. A future operational candidate would need a versioned composite package, deterministic component loading, latency/load testing, failure/rollback policy, ensemble-specific explainability, calibration evidence, and all existing release gates.
