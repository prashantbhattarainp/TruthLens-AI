# Shared API Contracts

This directory contains implementation-neutral JSON schemas shared by the backend and ML service.

- prediction-request.schema.json defines the payload accepted by POST /api/predict.
- prediction-response.schema.json defines the successful data payload returned by that endpoint.

The backend wraps successful data in a standard API envelope. Optional explainability details describe contributing classification signals and do not establish factual truth.
