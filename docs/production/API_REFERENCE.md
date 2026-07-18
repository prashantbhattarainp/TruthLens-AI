# Production Integration API Reference

## Public Node endpoints

| Endpoint | Purpose |
| --- | --- |
| `POST /api/predict` | Validated prediction request; Node returns the standard success/error envelope. |
| `GET /api/health` | Backend process health. |
| `GET /api/system/health` | Backend plus Python process-health view. |
| `GET /api/model/ready` | Proxies model package readiness. |
| `GET /api/model/metadata` | Proxies governed model lineage and limitations. |
| `GET /api/model/version` | Proxies service/model version state without triggering a load. |

## Internal Python endpoints

| Endpoint | Success | Failure |
| --- | --- | --- |
| `GET /health` | Process health and current lazy-load state. | Process-level failure only. |
| `GET /ready` | Package verified and model loaded. | `503` standardized package/readiness error. |
| `GET /metadata` | Model lineage, metrics summary, and limitations. | `503` package error. |
| `GET /version` | Service/model-version state. | None for unloaded package. |
| `POST /predict` | Raw validated prediction payload for Node. | `422` validation/empty processed input; `503` package error; `500` unexpected error. |

All Python error bodies use `{ "error": { "code", "message" }, "request_id" }`. Node wraps public results in the established `{ success, data|error, timestamp, request_id }` envelope.

## Prediction response changes

The shared prediction schema now represents the Linear SVM honestly:

```json
{
  "prediction": "Real",
  "confidence": null,
  "confidence_status": "unavailable",
  "decision_score": -0.42,
  "risk_level": "not_assessed"
}
```

`decision_score` is an uncalibrated classifier margin, not a probability. The frontend renders “Not calibrated” rather than a percentage. Full field definitions are in the [shared response schema](../../shared/contracts/prediction-response.schema.json).
