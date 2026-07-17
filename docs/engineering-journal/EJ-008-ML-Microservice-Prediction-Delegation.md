# EJ-008 - ML Microservice Prediction Delegation

**Date:** 2026-07-17  
**Phase / milestone:** Phase 2 - Milestone 2.5  
**Status:** Complete

## Scope

Replaced the backend's internal mock prediction generator with a private FastAPI prediction endpoint that returns deterministic contract data.

## Delivered

- Python `POST /predict` with validated request and response schemas, privacy-safe logging, and deterministic mock prediction output.
- Backend ML-client support for JSON `POST` requests, request-ID forwarding, timeout, transient-failure retry, and response-time logging.
- Prediction Service delegation and upstream response-contract validation.
- Public standardized error mapping for unavailable ML service, timeout, unsuccessful upstream response, and invalid upstream data.
- Updated public API documentation and architecture decision records.

## Deliberate boundaries

- No model, NLP preprocessing, dataset, training, database, or explainability algorithm was added.
- The Python service ignores valid request content when producing its fixed mock payload.
- The frontend remains unchanged and continues to call only the Node.js backend.

## Verification focus

Verification covers the complete frontend-client to backend to Python service path, offline ML service behaviour, timeout handling, invalid request payloads, and the unchanged public response envelope.
