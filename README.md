# TruthLens AI

TruthLens AI is a research-oriented platform for transparent fake-news classification research in Indian digital-media contexts. **Phase 4 is complete.** The repository now contains the Phase 4.6 publication package; Phase 5 has not begun.

## Research status

`TL-LSVM-TFIDF-v1.1.0-rc.1` is the final **internal research champion**: TF-IDF unigram/bigram plus LinearSVC, integrated through an integrity-checked package. It is not a production model (`production_model=false`) and has no post-tuning protected-test result.

| Evidence | Result |
| --- | --- |
| Frozen validation performance | Macro F1 0.5398; MCC 0.1014; FAKE recall 0.3183 |
| Best evaluated alternative | Hard/weighted ensemble Macro F1 0.5447, within the 0.005 practical-tie tolerance |
| Explainability | Bounded SHAP/LIME explanations of the uncalibrated LinearSVC margin |
| Transformer benchmark | No completed candidate metric: access/resource limited |
| Multilingual assessment | Unicode compatibility only; no validated Hindi/Hinglish fake-news performance |
| Reliability assessment | Capitalization and neutral expansion flip 29.0% and 27.0% of validation predictions |
| Calibration | Unavailable; sigmoid ECE/Brier values are non-fitted proxies, not confidence |

The model must not be described as a fact checker, factual-verdict tool, calibrated probability model, general Indian-media reliability assessor, Hindi/Hinglish detector, or autonomous moderation system. Public deployment remains blocked pending new governed data/model scope, post-tuning evaluation, calibration, robustness/fairness, rights, monitoring, and human-review evidence.

## Final architecture

```text
Frontend (HTML / CSS / JavaScript)
        ↓ public API
Node.js Backend (Express: validation, API envelope, timeout/retry)
        ↓ private API
Python ML Microservice (FastAPI: readiness, metadata, integrity-checked inference + XAI)
        ↓
Versioned internal candidate package (preprocessing + TF-IDF + LinearSVC)
```

The browser never calls the ML service directly. The response exposes an uncalibrated `decision_score`; `confidence` remains unavailable and `risk_level` is not assessed. Optional explanation metadata describes the model margin, not factual truth or confidence.

## Phase 4 milestones

| Milestone | Outcome |
| --- | --- |
| 4.1 | Explainable AI: SHAP/LIME model-behaviour evidence without changing the champion |
| 4.2 | Transformer benchmark protocol; no completed transformer result |
| 4.3 | Classical ensembles: bounded validation trade-off analysis; no champion change |
| 4.4 | Unicode/Hindi/Hinglish processing audit; no multilingual classifier claim |
| 4.5 | Robustness, calibration-proxy, slice, error, and inference-only ablation assessment |
| 4.6 | Research finalization, publication artifacts, reproducibility, and documentation QA |

## Publication and research documentation

- [Phase 4 publication package](docs/research/publication/README.md)
- [Project research summary](docs/research/PROJECT_RESEARCH_SUMMARY.md)
- [Phase 4 summary](docs/PHASE4_SUMMARY.md)
- [Final results tables](docs/research/publication/FINAL_RESULTS_TABLES.md)
- [Final comparison tables](docs/research/publication/FINAL_COMPARISON_TABLES.md)
- [Model Card](docs/research/MODEL_CARD.md) and [Data Card](docs/research/DATA_CARD.md)
- [Experiment Registry](docs/research/EXPERIMENT_REGISTRY.md) and [Model Registry](docs/research/MODEL_REGISTRY.md)
- [Research Decision Log](research/decision-log/README.md), [Engineering Journal](docs/engineering-journal/README.md), and [ADRs](docs/adr/README.md)

## Project structure

- `frontend/` - browser interface
- `backend/` - public Node.js API and ML-service client
- `ml-service/` - FastAPI inference service and Git-ignored versioned packages
- `ml/` - research protocols, multilingual/reliability harnesses, fixtures, and machine-readable registry
- `docs/research/` - reports, cards, figures, and publication package
- `research/decision-log/` - methodological governance evidence

## Verification

See the [reproducibility guide](docs/research/publication/REPRODUCIBILITY_GUIDE.md) for immutable identifiers, environment detail, execution order, and the publication-package verification command. Do not regenerate completed work or change the frozen protocol without a new governed decision.

## Roadmap

Phase 4 is closed. Future multilingual/external data, transformer compute, calibrated release evidence, robustness/fairness remediation, and deployment review require approval before Phase 5. See [future work](docs/research/publication/FUTURE_WORK.md).
