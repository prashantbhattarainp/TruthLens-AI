# Prediction API

The public API is served by the Node.js backend. Responses use a consistent envelope.

## Health

### GET /api/health

Returns backend availability and version.

### GET /api/system/health

Returns backend availability and whether the backend can reach the ML service.

## Create a prediction

### POST /api/predict

Request body:

    {
      "headline": "Example headline",
      "article": "Article text with at least 100 characters."
    }

Constraints:

| Field | Requirement |
| --- | --- |
| headline | 1–300 characters |
| article | 100–15,000 characters |

Successful response:

    {
      "success": true,
      "data": {
        "prediction": "Fake",
        "explanation": {
          "summary": "AI-assisted content assessment. Verify important information independently.",
          "reasons": [
            "Use this classification as a review signal, not a factual verdict."
          ]
        },
        "keywords": ["example"],
        "processing_time_ms": 42
      },
      "request_id": "…",
      "timestamp": "2026-07-18T00:00:00.000Z"
    }

The optional explainability object contains feature-contribution details. Refer to the JSON schema in shared/contracts/prediction-response.schema.json for the complete shape.

## Errors

The backend returns:

    {
      "success": false,
      "error": {
        "code": "VALIDATION_ERROR",
        "message": "Request validation failed."
      },
      "request_id": "…",
      "timestamp": "2026-07-18T00:00:00.000Z"
    }

Common status codes:

| Status | Meaning |
| --- | --- |
| 400 | Malformed JSON or unsupported request content |
| 422 | Validation failed |
| 502 | Invalid response from the ML service |
| 503 | ML service unavailable |
| 504 | ML service timeout |

A prediction is automated guidance only. Verify important claims with reliable, independent sources.
