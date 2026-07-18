# Reproducibility Guide

## Scope and availability

This guide reproduces the documented Phase 4 protocols and verifies the publication package. It does **not** authorize a new training run, a new model-selection run, protected-test access, or a production deployment. Raw data, fitted model packages, checkpoints, and run bundles are intentionally local/ignored; an authorized reproducer needs those governed artifacts in addition to this repository.

## Immutable identities

| Item | Value |
| --- | --- |
| Dataset | `TL-BFNK-EN-v1.0` |
| Derivative | `DER-20260718-r2` |
| Split | `SPL-TL-BFNK-EN-v1.0` |
| Derivative SHA-256 | `978931f41ece219a3e3e27d052cfb35dfe557af02a604d6f913d4ad8e6ca59ad` |
| Partition counts | Train 6,813; validation 1,461; protected test 1,458 |
| Label mapping | `REAL=0`, `FAKE=1` |
| Champion model | `MDL-TL-LSVM-TFIDF-v1.1.0-rc.1` / `TL-LSVM-TFIDF-v1.1.0-rc.1` |
| Package-manifest SHA-256 | `20b6efe11714f263d90fe892640ac6d9dce1da90c2d9c364a23a3bf624850a9e` |
| Model status | `production_model=false`, `integrated_not_deployment_approved` |

## Protocol controls

| Study | Source | Partition | Seed / fixed controls | Protected-test policy |
| --- | --- | --- | --- | --- |
| XAI | `scripts/research/generate_phase_4_1_xai_report.py` | Train-only global cohort of 512; local synthetic smoke | LIME seed 42; 1,000 samples; zero-TFIDF SHAP reference | None |
| Transformer benchmark | `ml/transformer_benchmark/protocol.py` | Train/validation; test only after checkpoint in a future completed run | Seed 42; max length 192; batch 8/16; 1 epoch; AdamW 2e-5 | Tuned LinearSVC: none; transformer: one non-selection evaluation only after checkpoint |
| Ensemble benchmark | `ml/ensemble_benchmark/protocol.py` | Validation only; stacker OOF train scores | Seed 42; fixed votes and OOF weights | None |
| Multilingual audit | `ml/multilingual_benchmark/protocol.py` | Validation appearance slices plus 12-record no-label fixture | Fixed Unicode/script/marker rules | None |
| Reliability audit | `ml/reliability_evaluation/protocol.py` | Validation only | Fixed deterministic stressors; no fitted calibrator | None |

## Environment

The service `pyproject.toml` targets Python 3.12. The local Phase 4.6 verification environment was Python 3.12.13 with these resolved packages:

| Package | Version |
| --- | --- |
| FastAPI | 0.139.2 |
| Uvicorn | 0.51.0 |
| spaCy | 3.8.14 |
| scikit-learn | 1.9.0 |
| SHAP | 0.52.0 |
| LIME | 0.2.0.1 |
| pandas | 2.3.3 |
| NumPy | 2.4.6 |
| joblib | 1.5.3 |
| Pillow | 11.3.0 |
| matplotlib | 3.11.0 |
| datasketch | 1.10.0 |
| PyTorch | 2.13.0 |
| safetensors | 0.8.0 |
| psutil | 7.2.2 |

Declared compatibility ranges are in [`ml-service/requirements.txt`](../../../ml-service/requirements.txt). The historical transformer run used a separate short-path environment and recorded PyTorch 2.13.0, Transformers 5.14.1, and Accelerate 1.14.0 in its local artifact context. Its ignored manifest, not this service environment, is the authoritative exact record for that aborted run.

## Folder map

| Location | Purpose |
| --- | --- |
| `ml/metadata/model-registry.json` | Machine-readable model and finalization state |
| `ml/*_benchmark/`, `ml/reliability_evaluation/` | Fixed research protocols and runners |
| `ml-service/` | Integrity-checked service and XAI implementation |
| `ml-service/artifacts/` | Ignored governed packages and local artifacts |
| `docs/research/` | Research reports, cards, registries, figures, publication package |
| `research/decision-log/` | Methodological decisions |
| `docs/engineering-journal/` | Milestone implementation journal |
| `scripts/research/` | Report generation and publication QA scripts |

## Verification order

From the repository root on Windows, create an isolated Python 3.12 environment, install the declared requirements, and place only authorized governed artifacts in their expected ignored locations. Do not substitute new data or artifacts under the same version IDs.

```powershell
$env:PYTHONPATH = (Get-Location).Path
& .\ml-service\.venv\Scripts\python.exe -m unittest discover -s .\ml-service\tests
& .\ml-service\.venv\Scripts\python.exe .\scripts\research\verify_phase_4_publication.py
```

The verification script checks required publication files, registry invariants, tracked figure hashes, and repository Markdown links. The existing Phase 4 runners reject hash/split mismatches before they retain evaluated records.

## Controlled reruns

- Run the XAI artifact generator only with the existing approved package and frozen train-only policy.
- Run the ensemble, multilingual, and reliability harnesses only as documented research audits; they must preserve validation-only and aggregate-only restrictions.
- A transformer rerun needs separately approved compute and access, a new immutable artifact, and the fixed Phase 4.2 protocol (or a new decision for a changed protocol).
- Calibration, retraining, threshold changes, model promotion, a multilingual corpus, a new external evaluation, and any protected-test plan require a new governed decision and versioned data/model scope.

## Expected limitations of a reproduction

An authorized reproduction can verify code, registry state, figures, and hashes. It cannot infer public deployment readiness from a successful run. `confidence` must remain unavailable, and no output may be presented as a factual verdict, calibrated probability, reliability score, or Hindi/Hinglish classification result.
