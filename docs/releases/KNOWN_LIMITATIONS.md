# Known Limitations — v1.0.0-RC1

## Release status

RC1 is an internal integration release candidate only. It is not a production model release, public deployment approval, or assurance of fitness for consequential use.

## Research and model limits

- `TL-LSVM-TFIDF-v1.1.0-rc.1` is an internal LinearSVC TF-IDF research champion with frozen validation Macro F1 `0.5398`, MCC `0.1014`, and FAKE recall `0.3183`.
- It is untested after tuning on a protected test set; `production_model=false` and `integrated_not_deployment_approved` remain authoritative.
- The decision score is an uncalibrated margin. Confidence is intentionally unavailable and risk is not assessed.
- Outputs are not factual verdicts, source-credibility assessments, causal explanations, or autonomous moderation decisions.
- Evidence is English-only. Unicode processing compatibility does not establish Hindi/Hinglish fake-news performance.
- Transformer candidates did not complete evaluation; evaluated ensembles did not promote a new champion.
- Reliability, fairness, calibration, external generalization, data-rights, and human-review gates remain unresolved for deployment.

## System and deployment limits

- No database, user account, authentication, session management, prediction retention, telemetry store, or database-health endpoint is implemented.
- Dashboard prediction distribution is illustrative; dashboard database status is intentionally `Not instrumented`.
- This repository contains no production container manifests, infrastructure-as-code, reverse-proxy configuration, deployment CI/CD pipeline, or runtime rate-limit implementation.
- CORS configuration is present but is not a substitute for authentication, network isolation, HTTPS, a CSP, security headers, or rate limiting.
- Browser QA ran in the available Chromium-based in-app surface. Chrome, Edge, and Firefox require a deployment-owner manual compatibility pass before an external release claim.

## Documentation and evidence limits

- Local RC screenshots are evidence of the local controlled run, not public-production screenshots or performance benchmarks.
- Measured latency and memory depend on the developer machine, warm model state, and synthetic input; they are not capacity guarantees.
- No model/data/research artifacts were regenerated for RC1.
