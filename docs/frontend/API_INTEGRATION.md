# Frontend API Integration

## Ownership boundary

`frontend/src/js/api/api.js` is the only browser fetch boundary. `prediction-api.js` uses it to send `POST /api/predict` to the public Node.js backend. The browser never calls the private Python ML service directly.

Public runtime configuration is limited to `frontend/public/config.js`:

```js
window.TruthLensConfig = {
  apiBaseUrl: 'http://127.0.0.1:3000',
  apiTimeoutMs: 12000,
};
```

Deployments may replace those public values before the application module loads. Credentials, model paths, or other secrets must never be placed in this file.

## Prediction request

```http
POST /api/predict
Content-Type: application/json

{
  "headline": "string, 1-300 characters",
  "article": "string, 100-15,000 characters"
}
```

The frontend validates those same limits for quick feedback, then the Node backend validates them again. URL input is deliberately not sent because the current public contract has no URL field.

## Success handling

The API client requires the established envelope:

```json
{
  "success": true,
  "data": { "prediction": "Real" },
  "timestamp": "2026-07-18T00:00:00.000Z",
  "request_id": "..."
}
```

`prediction-api.js` passes `data`, `timestamp`, and `request_id` to the result card. Optional `data.explainability` is rendered only when present; missing or unavailable data produces an explanatory placeholder, not a fabricated contribution or confidence score.

## Failure handling

| API/client condition | Dashboard message |
| --- | --- |
| `VALIDATION_ERROR`, `EMPTY_PROCESSED_INPUT` | Content needs attention |
| `REQUEST_TIMEOUT`, `ML_SERVICE_TIMEOUT` | Request timed out |
| `NETWORK_ERROR` | Backend unavailable |
| `ML_SERVICE_NOT_CONFIGURED`, `ML_SERVICE_UNAVAILABLE`, `ML_SERVICE_HTTP_ERROR`, `ML_SERVICE_INVALID_RESPONSE`, model-unavailable codes | Model service unavailable |
| Other server failure | Prediction unavailable |

The existing API client continues to map unreadable JSON to `INVALID_RESPONSE`, aborted fetches to `REQUEST_TIMEOUT`, and transport failures to `NETWORK_ERROR`. No API route, payload, timeout contract, or backend behaviour was changed for this dashboard.

For the authoritative endpoint and schema reference, see [Production Integration API Reference](../production/API_REFERENCE.md) and the [shared response schema](../../shared/contracts/prediction-response.schema.json).
