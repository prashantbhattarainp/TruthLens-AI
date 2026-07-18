# Final System Architecture

TruthLens AI retains its established three-layer architecture.

```mermaid
flowchart TB
  UI["Frontend\nHTML / CSS / JavaScript"]
  API["Node.js Backend\nExpress validation, public API envelope, retries, observability"]
  MLS["Python ML Microservice\nFastAPI, readiness, metadata, integrity checks, SHAP/LIME"]
  PKG["Immutable candidate package\npreprocessing config + TF-IDF + LinearSVC + metadata"]
  GOV["Research governance\ndataset manifest, experiment registry, model registry"]
  UI --> API --> MLS --> PKG
  GOV -. "lineage and release controls" .-> PKG
```

The browser has no direct model-service access. The backend is the public trust boundary. The Python service owns versioned inference package loading and in-process explanation generation; it does not train or select models. Governance artifacts bind the package to its frozen dataset, configuration, experiment evidence, and train-only XAI report. The package's current status is integration-only, not deployment-approved.
