# Experiment Registry

**Scope:** Phase 4.2 transformer benchmark records. Historical Phase 3 experiment bundles remain in their immutable local artifact locations and are not reconstructed here.

| Experiment ID / candidate | Status | Frozen data evidence | Validation selection | Protected-test access | Artifact evidence |
| --- | --- | --- | --- | --- | --- |
| `P42-indicbert-20260718T115636Z` | `not_evaluated_access_limited` | Derivative hash and split verified by runner | None | None | Ignored manifest records gated upstream 401 failure |
| `P42-distilbert-20260718T115744Z` | `not_evaluated_resource_limited` | Derivative hash and split verified before load | None | None | Ignored resource-limitation record; stopped after >86 CPU-minutes without checkpoint/results |
| `P42-bert_base-*` | `not_evaluated_resource_limited` | Pre-specified | None | None | Not started after lower-cost CPU limitation |
| `P42-roberta-*` | `not_evaluated_resource_limited` | Pre-specified | None | None | Not started after lower-cost CPU limitation |

Every completed record must retain dataset/derivative/split identity, dataset SHA-256, code revision, model identifier and resolved revision, fixed protocol, runtime package versions, hardware, timing, checkpoint file checksums, full-precision metrics, confusion matrix, cohort/error aggregates, and an explicit research-only limitation statement. The tracker must not store raw article text or use protected-test results as model-selection evidence.
