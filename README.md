# TruthLens AI

TruthLens AI is a research-oriented platform for explainable fake news detection in Indian digital media.

## Project status

Phase 4.2 completed at a documented resource-limited benchmark boundary. `TL-LSVM-TFIDF-v1.1.0-rc.1` remains the packaged internal champion with integrity checks, readiness, lineage metadata, privacy-safe logging, and bounded SHAP/LIME explanations. It remains **untested after tuning**, `integrated_not_deployment_approved`, and unsuitable as a fact checker or factual-verdict system. The Phase 3.8 protected test is not reused. IndicBERT was gated; DistilBERT exceeded the CPU window before checkpoint selection; BERT base and RoBERTa were not started. No transformer receives a performance score or can replace the incumbent automatically; see the [transformer benchmark](docs/research/TRANSFORMER_BENCHMARK.md), [model-selection update](docs/research/MODEL_SELECTION_UPDATE.md), [XAI framework](docs/research/EXPLAINABLE_AI.md), and [Phase 3 summary](docs/PHASE3_SUMMARY.md).

## Current architecture

```text
Frontend (HTML / CSS / JavaScript)
        ↓ public API
Node.js Backend (Express: validation, API envelope, timeout/retry)
        ↓ private API
Python ML Microservice (FastAPI: readiness, metadata, integrity-checked inference + XAI)
        ↓
Versioned internal candidate package (preprocessing + TF-IDF + Linear SVM)
```

The browser never calls the ML service directly. The current model response exposes an uncalibrated `decision_score`; `confidence` is intentionally unavailable and `risk_level` is not assessed. Successful predictions include optional explanation metadata for the same model margin; it is not a factual explanation or confidence score.

## Model information

- Model: `TL-LSVM-TFIDF-v1.1.0-rc.1` (Linear SVM, TF-IDF unigram/bigram)
- Dataset: `TL-BFNK-EN-v1.0`, `DER-20260718-r2`, `SPL-TL-BFNK-EN-v1.0`
- Internal status: `integrated_not_deployment_approved`
- Validation evidence: Macro F1 0.5398, MCC 0.1014; no post-tuning protected-test result

## API overview

- `POST /api/predict` – validated research-scope classification signal
- `GET /api/health` and `GET /api/system/health` – process health
- `GET /api/model/ready`, `/metadata`, and `/version` – model package state and governed lineage

See the [API reference](docs/production/API_REFERENCE.md) and [deployment guide](docs/production/PRODUCTION_DEPLOYMENT_GUIDE.md).

## Project structure

- `frontend/` – browser interface
- `backend/` – public Node.js API and ML-service client
- `ml-service/` – FastAPI inference service and Git-ignored versioned packages
- `ml/` – governed research pipeline, configurations, registries, and local artifacts
- `docs/research/`, `docs/production/`, `research/decision-log/` – research, integration, and governance evidence

## Planned platform

- HTML5, CSS3, and vanilla JavaScript frontend
- Node.js and Express backend
- Python, FastAPI, spaCy, and scikit-learn ML service
- SQLite initially, with a future PostgreSQL migration path

## Documentation

- [Research methodology](docs/research/RESEARCH_METHODOLOGY.md)
- [Research documentation package](docs/research/README.md)
- [Research decision log](research/decision-log/README.md)
- [Engineering journal](docs/engineering-journal/README.md)
- [Architecture decision records](docs/adr/README.md)

## Setup

Setup instructions will be added in a later milestone.

## Development roadmap

The implementation roadmap is maintained in the [research and implementation roadmap](docs/architecture/Research-Roadmap.md).

Phase 4.2 is complete at its resource-limited evidence boundary. Public deployment remains blocked pending a new governed release process, post-tuning evaluation plan, calibration, robustness/fairness evidence, rights review, monitoring, and human-review controls.
