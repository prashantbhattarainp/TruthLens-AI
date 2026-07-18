# TruthLens AI v1.0.0 Release Notes

TruthLens AI v1.0.0 is the first public release of the AI-assisted fake-news detection system.

## Highlights

- Product navigation: Home, Predict, Dashboard, About, Contact, and Settings.
- A streamlined prediction API that does not return runtime-package identifiers.
- Explainability views that help users inspect contributing text features.
- On-demand service-health checks and a transparent, stateless dashboard.
- Deployment and operating guidance for the frontend, backend, and ML service.

## Upgrade notes

- Clients should use the v1.0.0 prediction response schema. Deprecated metadata fields are no longer returned by `POST /api/predict`.
- The public backend no longer serves `/api/model/*` endpoints.
- Update `SERVICE_VERSION` and `ML_SERVICE_VERSION` to `1.0.0` when deploying.

See [CHANGELOG.md](CHANGELOG.md) for the full change list and [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md) for current product boundaries.
