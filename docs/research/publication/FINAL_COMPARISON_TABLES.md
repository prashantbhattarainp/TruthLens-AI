# Final Comparison Tables

These comparisons consolidate the evidence actually collected in Phases 4.1-4.5. Different rows were measured in different bounded research harnesses; blank cells are retained where a comparable measurement does not exist.

## Computational and operational comparison

| Candidate | Serialized components | Recorded refit time | Component validation inference | Explainability | Deployment complexity | Status |
| --- | ---: | ---: | ---: | --- | --- | --- |
| LinearSVC | 0.81 MiB | 911 ms | 126 ms / 1,461 records | Integrated SHAP and LIME margin explanations | Lowest: one package and one sparse pipeline | Internal research champion only |
| MultinomialNB | 1.27 MiB | 978 ms | 140 ms / 1,461 records | No integrated XAI path | One additional package/pipeline | Challenger only |
| Logistic Regression | 0.81 MiB | 1,348 ms | 137 ms / 1,461 records | No integrated XAI path | One additional package/pipeline | Challenger only |
| Hard / weighted vote | 2.90 MiB combined | Component refits above | Three component passes plus 84 ms aggregation / 1,461 | Component labels/weights only; no faithful combined SHAP/LIME | High: component alignment, integrity, failure, and explanation handling | Research challenger only |
| Soft vote | 2.08 MiB derived from two listed components | Component refits above | Two component passes plus aggregation; no standalone timing | No integrated ensemble explanation | Medium-high; probability/threshold governance needed | Research challenger only |
| OOF stacker | 2.90 MiB + 895-byte meta-model | 8.1 ms stacker fit after component work | Three component passes plus meta-model; no standalone timing | Composite explanation is more difficult | Highest: three pipelines, score alignment, and meta-model | Rejected |
| Transformer candidates | No completed local package | — | — | — | Would require model/runtime packaging and suitable compute | Unevaluated |

The component times are benchmark-process measurements, not end-to-end API latency or a production capacity guarantee. The ensemble harness observed process RSS increasing from 148.4 MB before component load to 368.9 MB after evaluation; this is a host/process observation, not a deployment memory specification.

## Capability, robustness, and calibration comparison

| Approach | Valid multilingual evidence | Robustness evidence | Calibration evidence | Principal strength | Principal limitation |
| --- | --- | --- | --- | --- | --- |
| LinearSVC incumbent | Unicode accepted; English validation only | Ten deterministic validation stressors; major capitalization and expansion sensitivity | None; ECE/Brier are non-fitted margin proxies | Integrated, reproducible, sparse and explainable | Weak absolute performance; margin is not confidence |
| Classical individual challengers | None beyond same English derivative | Not separately assessed | MNB/LR probabilities exist, but no calibration evidence for a release | Alternative recall/ranking trade-offs | Not integrated or release-reviewed |
| Classical ensembles | None beyond same English derivative | Not assessed | No calibrated ensemble-confidence evidence | Slight Macro-F1 or ranking changes | Higher false-positive burden/complexity; validation only |
| Transformers | None | None | None | Relevant future architectures | No completed local artifact or metric |
| Multilingual audit layer | 12/12 synthetic routing; 9 Devanagari and 2 Hinglish appearance records | Input compatibility only | Not applicable | Preserves Unicode text for research audit | Not a Hindi/Hinglish fake-news evaluation |

## Selection trade-offs

| Decision factor | LinearSVC | Best evaluated alternative | Selection result |
| --- | --- | --- | --- |
| Macro F1 | 0.5398 | Hard/weighted vote: 0.5447 | Difference is inside the 0.005 practical tie tolerance |
| FAKE false negatives | 392 | Soft vote: 325 | Soft vote adds 106 false positives and lowers accuracy/MCC |
| Ranking | ROC-AUC 0.5576; PR-AUC 0.4641 | Soft vote: 0.5688 / 0.4769 | Ranking gain does not establish calibrated confidence or promotion |
| Explainability | Same-model SHAP/LIME margin evidence | No comparable ensemble evidence | Incumbent retained |
| Integration | Integrity-checked service package | No ensemble/transformer service package | Incumbent retained |
| Production suitability | Not approved | Not approved | No production model selected |

The final decision is a constrained research-integration choice, not a claim that the LinearSVC is accurate enough for factual verification or deployment.
