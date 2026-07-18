# Explanation Methodology

## Frozen inputs

| Item | Value |
| --- | --- |
| Model | `TL-LSVM-TFIDF-v1.1.0-rc.1` |
| Dataset | `TL-BFNK-EN-v1.0`, `DER-20260718-r2` |
| Global cohort | 512 deterministic, class-balanced training records |
| Validation/protected test access | None |
| SHAP reference | All-zero sparse TF-IDF vector |
| LIME seed/sample count | 42 / 1,000 |

## Reproducibility

Run the artifact generator from the repository root:

```powershell
& .\ml-service\.venv\Scripts\python.exe .\scripts\research\generate_phase_4_1_xai_report.py
```

The script records the derivative SHA-256, model/dataset versions, selected partition, sample count, methods, figures, and restrictions in [XAI_ARTIFACT_MANIFEST.json](XAI_ARTIFACT_MANIFEST.json). It does not train, tune, calibrate, score a held-out partition, or write raw text.

## Evaluation checks

- SHAP local additivity residual is checked against the LinearSVC decision margin.
- LIME records local surrogate fidelity and fixed configuration.
- Synthetic integration tests verify frozen preprocessing, response metadata, unavailable confidence, and bounded features.
