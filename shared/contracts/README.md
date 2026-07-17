# Shared API Contracts

This directory contains versioned, implementation-neutral contracts shared by the backend and ML service.

`prediction-request.schema.json` defines the payload accepted by `POST /api/predict`.

`prediction-response.schema.json` defines the successful `data` payload returned by that endpoint. The backend wraps it in the standard API success envelope.

Phase 2 uses deterministic mock data to establish this contract. It does not call the ML service.
