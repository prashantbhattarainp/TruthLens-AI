# Shared API Contracts

This directory contains versioned, implementation-neutral contracts shared by the backend and ML service.

`prediction-request.schema.json` defines the payload accepted by `POST /api/predict`.

`prediction-response.schema.json` defines the successful `data` payload returned by that endpoint. The backend wraps it in the standard API success envelope.

Phase 2 established this contract with deterministic mock data. In Phase 2.5, the backend delegates that same deterministic contract data to the private ML service; no dataset, NLP pipeline, or trained model is involved.

Phase 4.1 adds an optional `explainability` response object. It carries SHAP/LIME metadata for the uncalibrated LinearSVC margin while preserving all established request and response fields; it does not introduce a confidence probability.
