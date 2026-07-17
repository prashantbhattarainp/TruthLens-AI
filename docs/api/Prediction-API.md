# Prediction API

## Purpose

`POST /api/predict` establishes the public prediction contract for TruthLens AI. The Node.js backend validates the request and delegates it to the private Python ML service at `POST /predict`. The Python service currently returns deterministic mock data only; it does not load a dataset or perform NLP or machine-learning inference.

## Endpoint

```text
POST /api/predict
Content-Type: application/json
```

## Browser integration

The frontend sends this request only through `frontend/src/js/api/prediction-api.js`. Its fetch implementation is isolated in `frontend/src/js/api/api.js`.

For local development, `frontend/public/config.js` points the browser client to `http://127.0.0.1:3000` with an 8-second request timeout. The backend allows browser requests only from origins configured through `CORS_ALLOWED_ORIGINS`, for example:

```text
CORS_ALLOWED_ORIGINS=http://127.0.0.1:5500,http://localhost:5500
```

Production deployments must replace both values with their deployed frontend and backend origins. The frontend never calls the Python ML service directly.

## Internal ML-service delegation

The backend forwards the validated request to `${ML_SERVICE_URL}/predict` as JSON and forwards the `X-Request-Id` header for cross-service log correlation. The Python response is validated against the existing prediction response contract before the backend returns its standard public envelope.

The ML client uses `REQUEST_TIMEOUT_MS`, `ML_SERVICE_RETRY_ATTEMPTS`, and `ML_SERVICE_RETRY_DELAY_MS` from the backend environment. The default `ML_SERVICE_RETRY_ATTEMPTS=2` results in one retry after an initial transient failure.

| Upstream condition                               | Public HTTP status | Error code                                               |
| ------------------------------------------------ | ------------------ | -------------------------------------------------------- |
| Service unavailable or network failure           | 503                | `ML_SERVICE_UNAVAILABLE`                                 |
| Upstream request timeout                         | 504                | `ML_SERVICE_TIMEOUT`                                     |
| Invalid upstream payload or non-success response | 502                | `ML_SERVICE_INVALID_RESPONSE` or `ML_SERVICE_HTTP_ERROR` |

## Request schema

```json
{
  "headline": "string",
  "article": "string"
}
```

Validation occurs after trimming leading and trailing whitespace.

| Field      | Required | Rules                                |
| ---------- | -------- | ------------------------------------ |
| `headline` | Yes      | 1–300 characters after trimming      |
| `article`  | Yes      | 100–15,000 characters after trimming |

Additional request properties are rejected.

## Successful response

All successful responses use the established API envelope.

```json
{
  "success": true,
  "data": {
    "prediction": "Fake",
    "confidence": 0.87,
    "risk_level": "high",
    "explanation": {
      "summary": "Deterministic mock explanation for API-contract verification only.",
      "reasons": [
        "Sensational language detected",
        "Clickbait patterns",
        "Unverified claims",
        "Emotional wording"
      ]
    },
    "keywords": ["breaking", "shocking", "viral", "urgent", "exclusive"],
    "processing_time_ms": 42,
    "model": "mock-logistic-regression",
    "model_version": "0.1.0-mock",
    "dataset_version": "indian-digital-media-demo-v1"
  },
  "timestamp": "2026-07-17T12:00:00.000Z",
  "request_id": "uuid"
}
```

The `confidence` value is a decimal in the inclusive range `0` to `1`. The response fields are deterministic in this milestone and must not be interpreted as a content assessment.

## Validation error response

Validation failures use the standard error envelope and return HTTP `400`.

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed."
  },
  "timestamp": "2026-07-17T12:00:00.000Z",
  "request_id": "uuid"
}
```

Malformed JSON returns `INVALID_JSON`. Unknown routes return `NOT_FOUND`.

## Example request

```bash
curl -X POST http://127.0.0.1:3000/api/predict \
  -H "Content-Type: application/json" \
  -d "{\"headline\":\"Example headline\",\"article\":\"This example article contains at least one hundred characters so it satisfies the mock API validation requirements for this request.\"}"
```

## Logging and privacy

The backend logs the prediction request ID, field lengths, validation outcome, ML-client request timing, retry activity, and response status. The Python service logs the correlated request ID and field lengths. Neither service logs the supplied headline or article text.

## Contract references

- [Prediction request schema](../../shared/contracts/prediction-request.schema.json)
- [Prediction response data schema](../../shared/contracts/prediction-response.schema.json)
