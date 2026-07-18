# Explainability UI Guide

## What the dashboard explains

The dashboard visualizes optional Phase 4.1 response metadata from the existing model service. It explains signed features of the uncalibrated LinearSVC decision margin. It does **not** explain factual truth, source credibility, calibrated confidence, or production readiness.

## UI mapping

| Response field | Dashboard treatment |
| --- | --- |
| `metadata.status`, `metadata.disclaimer` | Availability label and interpretation boundary. |
| `top_influential_features` | Ranked top contributing words/features with signed margin contribution. |
| `shap.method`, `baseline`, `base_value`, `additive_residual` | SHAP summary metadata. |
| `shap.top_positive_features` | Features supporting the Fake-class margin. |
| `shap.top_negative_features` | Features supporting the Real-class margin. |
| `lime.method`, `target`, `local_fidelity`, `sample_count`, `random_seed` | Deterministic local-surrogate metadata. |
| `lime.top_positive_features`, `lime.top_negative_features` | Local contributions for the Fake- and Real-class margins. |

Feature direction appears as text and colour:

- Supports the Fake-class margin
- Supports the Real-class margin
- Minimal effect on the model margin

Positive and negative refer only to the model's margin convention. They are not evidence that an article is factually fake or real.

## Availability states

If `explainability` is omitted, its metadata status is unavailable, or an individual SHAP/LIME result is `null`, the relevant panel says **Unavailable** and describes what was not returned. The UI never substitutes fabricated values, an inferred probability, or an explanation from a different request.

## Reading the panels responsibly

1. Start with the prediction label and research boundary.
2. Treat the decision margin as a signed classifier signal, not a confidence score.
3. Use the explanation panels to inspect model behaviour for that request only.
4. Keep the documented model limitations, multilingual limitations, and human-review requirement in view.

The backend preserves preprocessing and feature engineering for all reported XAI data. The dashboard displays that backend-produced metadata; it does not rerun SHAP, LIME, or model inference in the browser.
