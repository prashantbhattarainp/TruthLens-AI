# Experiment Registry

**Scope:** Phase 4.2 transformer benchmark records. Historical Phase 3 experiment bundles remain in their immutable local artifact locations and are not reconstructed here.

| Experiment ID / candidate | Status | Frozen data evidence | Validation selection | Protected-test access | Artifact evidence |
| --- | --- | --- | --- | --- | --- |
| `P42-indicbert-20260718T115636Z` | `not_evaluated_access_limited` | Derivative hash and split verified by runner | None | None | Ignored manifest records gated upstream 401 failure |
| `P42-distilbert-*` | `benchmark_in_progress` | Derivative hash and split verified before load | Pending | None until selection completes | Ignored run directory, checkpoint, manifest, results when complete |
| `P42-bert_base-*` | `queued_not_evaluated` | Pre-specified | Pending | None | No artifact yet |
| `P42-roberta-*` | `queued_not_evaluated` | Pre-specified | Pending | None | No artifact yet |

Every completed record must retain dataset/derivative/split identity, dataset SHA-256, code revision, model identifier and resolved revision, fixed protocol, runtime package versions, hardware, timing, checkpoint file checksums, full-precision metrics, confusion matrix, cohort/error aggregates, and an explicit research-only limitation statement. The tracker must not store raw article text or use protected-test results as model-selection evidence.
