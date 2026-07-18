# Experiment Registry

**Scope:** Phase 4.2 transformer and Phase 4.3 ensemble benchmark records. Historical Phase 3 experiment bundles remain in their immutable local artifact locations and are not reconstructed here.

| Experiment ID / candidate | Status | Frozen data evidence | Validation selection | Protected-test access | Artifact evidence |
| --- | --- | --- | --- | --- | --- |
| `P42-indicbert-20260718T115636Z` | `not_evaluated_access_limited` | Derivative hash and split verified by runner | None | None | Ignored manifest records gated upstream 401 failure |
| `P42-distilbert-20260718T115744Z` | `not_evaluated_resource_limited` | Derivative hash and split verified before load | None | None | Ignored resource-limitation record; stopped after >86 CPU-minutes without checkpoint/results |
| `P42-bert_base-*` | `not_evaluated_resource_limited` | Pre-specified | None | None | Not started after lower-cost CPU limitation |
| `P42-roberta-*` | `not_evaluated_resource_limited` | Pre-specified | None | None | Not started after lower-cost CPU limitation |
| `P43-classical-ensemble-20260718T125724Z` | `evaluated_research_only_validation_only` | Hash/split verified; immutable Phase 3.9 components | Frozen validation only | None | Ignored run manifest, aggregate metrics, and stacking meta-model; no raw text/predictions |
| `P44-multilingual-assessment-20260718T133030Z` | `completed_research_only_multilingual_compatibility_assessment` | Hash/split verified; English derivative scanned only for descriptive language appearance | Frozen validation descriptive slices only; no selection | None | Ignored aggregate manifest/results; 12-record synthetic language-processing fixture has no REAL/FAKE labels |
| `P45-reliability-assessment-20260718T140601Z` | `completed_research_only_reliability_assessment` | Hash/split verified; integrity-checked packaged champion and frozen preprocessing | Frozen validation stress/slice diagnostics only; no selection | None | Ignored aggregate results/manifest plus tracked aggregate figure hashes; no raw text, identifiers, scores, or predictions |

Every completed record must retain dataset/derivative/split identity, dataset SHA-256, code revision, model identifier and resolved revision, fixed protocol, runtime package versions, hardware, timing, checkpoint file checksums, full-precision metrics, confusion matrix, cohort/error aggregates, and an explicit research-only limitation statement. The tracker must not store raw article text or use protected-test results as model-selection evidence.

The Phase 4.3 record evaluates hard voting, weighted voting, soft voting, and stacking. Blending and classical-transformer hybrid variants are explicit exclusions, not missing metrics: no independent blend-development partition or completed transformer prediction artifact exists.

The Phase 4.4 record neither trains nor compares a multilingual classifier. Its Devanagari-bearing and Hinglish-heuristic validation slices are not independently labelled language datasets, so their descriptive metrics cannot select a model or establish Hindi/Hinglish performance. The protected test remains untouched.

The Phase 4.5 record runs pre-specified deterministic perturbations, non-fitted margin-proxy reliability diagnostics, descriptive slices, and inference-only ablations. It does not fit calibration, modify the champion, establish fairness/generalization claims, or access the protected test.
