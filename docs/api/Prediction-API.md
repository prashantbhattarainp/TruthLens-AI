# Prediction API

## Purpose

`POST /api/predict` establishes the public prediction contract for TruthLens AI. The Node.js backend validates the request and delegates it to the private Python ML service at `POST /predict`. The Python service loads the versioned `TL-LSVM-TFIDF-v1.1.0-rc.1` internal candidate after package integrity checks. It is not deployment-approved, a fact checker, or a source of factual verdicts.

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
    "prediction": "Real",
    "confidence": null,
    "confidence_status": "unavailable",
    "decision_score": -0.42,
    "risk_level": "not_assessed",
    "explanation": {
      "summary": "Limited research classification signal only; it is not a factual verdict.",
      "reasons": [
        "The Linear SVM score is not a calibrated probability.",
        "This candidate is untested after tuning and is not deployment-approved."
      ]
    },
    "keywords": [],
    "processing_time_ms": 42,
    "model": "TruthLens Linear SVM conditional research champion",
    "model_version": "TL-LSVM-TFIDF-v1.1.0-rc.1",
    "dataset_version": "TL-BFNK-EN-v1.0"
  },
  "timestamp": "2026-07-17T12:00:00.000Z",
  "request_id": "uuid"
}
```

The Linear SVM candidate returns `confidence: null`, `confidence_status: "unavailable"`, an uncalibrated `decision_score`, and `risk_level: "not_assessed"`. A decision score is not a probability or factual-confidence value. See the updated [production API reference](../production/API_REFERENCE.md) for the current schema and model endpoints.

## Explainability metadata

Phase 4.1 adds an optional `explainability` object without changing the request contract or established prediction fields. On a normal successful response it contains bounded top features plus:

```json
{
  "metadata": {
    "status": "available",
    "prediction_confidence_status": "unavailable",
    "decision_score_interpretation": "uncalibrated_linear_svm_margin",
    "preprocessing_reused": true,
    "feature_engineering_reused": true
  },
  "shap": {
    "method": "linear_shap",
    "baseline": "zero_tfidf_reference"
  },
  "lime": {
    "method": "lime_text_margin_surrogate",
    "target": "fake_margin"
  }
}
```

Positive contributions increase the Fake-class margin; negative contributions increase the Real-class margin. They describe model behaviour only and are not factual evidence, causal explanations, or calibrated confidence. If an internal explanation dependency fails, prediction remains available and metadata reports `status: "unavailable"` without exposing request text.

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

The backend logs the prediction request ID, field lengths, validation outcome, ML-client request timing, retry activity, and response status. The Python service logs structured request ID, field lengths, prediction label, uncalibrated-score availability, latency, model version, and status. Neither service logs the supplied headline or article text.

## Contract references

- [Prediction request schema](../../shared/contracts/prediction-request.schema.json)
- [Prediction response data schema](../../shared/contracts/prediction-response.schema.json)
