# Model Registry

**Scope:** Model-candidate and release-governance design
**Status:** Empty by design — no trained or approved model exists
**Related documents:** [Experiment registry](EXPERIMENT_REGISTRY.md), [Research methodology](RESEARCH_METHODOLOGY.md)

## Purpose

The model registry binds a model artefact to the exact experiment, dataset, split, fitted features, label mapping, evaluation report, and limitations that justify it. A file named as a model is not a registered model until this evidence is complete.

## Lifecycle vocabulary

| Status | Meaning |
| --- | --- |
| Candidate | Training artefact exists but has not completed release review. |
| Evaluated | Frozen validation and held-out evaluation evidence is attached. |
| Approved for research reporting | Required evidence, limitations, and reproducibility checks passed; not a production deployment approval. |
| Superseded | Later model replaces it for a stated comparison scope; record remains available. |
| Retracted | Material defect, leakage, data-rights issue, or invalid result prevents use; reason is retained. |
| Archived | Retained for reproducibility but not recommended for new use. |

## Required model-release record

| Field | Required evidence |
| --- | --- |
| Model ID, version, and status | Immutable identifier, semantic/version convention, lifecycle state, and dates. |
| Parent experiment | Experiment ID and report that produced the candidate. |
| Algorithm and intent | Classifier, task/text unit, intended research use, and non-goals. |
| Data lineage | Dataset derivative, split, raw-source lineage, label mapping, and checksums. |
| Fitted components | Model, vectorizer/feature artefact, preprocessing configuration, threshold/calibration artefact, and checksums. |
| Training context | Code revision, environment/dependency evidence, seed, hyperparameters, and class-imbalance treatment. |
| Evaluation evidence | Primary and supporting metrics, support counts, uncertainty estimate, calibration/ranking evidence where valid, cohort slices, and error analysis. |
| Explainability evidence | Method, input/output relationship, stability review, filtered features, and explicit non-fact-checking warning. |
| Limitations and risk | Language/source/time scope, potential bias, drift risk, leakage findings, legal/data restrictions, and unsuitable uses. |
| Approvals and retention | Reviewer, decision date, report location, retention/access restrictions, and supersession or retraction links. |

## Approval gate

A model may be described only as research-evaluated when it has a versioned dataset and split, frozen configuration, evaluation report, model metadata, artefact checksums, and experiment record. It must not be described as fact-checking, generally valid for all Indian media, or production-ready based only on a held-out metric.

## Current entries and mock boundary

The tracked registry is [`ml/metadata/model-registry.json`](../../ml/metadata/model-registry.json). The Phase 3.7 experiment framework creates an immutable `model-registry-record.json` beside each approved experiment bundle with the required model version, dataset version, dataset SHA-256 hash, feature-engineering version/configuration hash, experiment ID, aggregate performance metrics, artifact location, training date, and notes. Initial status is `Candidate`; Phase 3.8 validation and one-time protected-test evidence are required before the limited research-candidate status documented below.

The current deterministic mock response identifies itself as a mock contract fixture; its model and dataset strings are not trained-model or dataset-release records and must not be used in papers, benchmark tables, or this registry.

## Phase 3.8 historical baseline

| Model ID | Status | Parent experiment | Dataset / split | Selection evidence | Disposition |
| --- | --- | --- | --- | --- | --- |
| `MDL-linear-svm-1.0.0-EXP-20260717-linear-svm-177d71e9c9` | Historical evaluated baseline | `EXP-20260717-linear-svm-177d71e9c9` | `TL-BFNK-EN-v1.0` / `SPL-TL-BFNK-EN-v1.0` | Validation Macro F1 0.5274; one-time test Macro F1 0.5486; MCC 0.1037 | Historical comparison only; test evidence cannot be reused after tuning |

## Phase 3.9 conditional candidate set

| Model ID | Status | Optimization record | Selection evidence | Disposition |
| --- | --- | --- | --- | --- |
| `MDL-TL-LSVM-TFIDF-v1.1.0-rc.1` | Integrated internal champion, untested after tuning | `OPT-20260718-linear-svm-faafafe15e` | OOF Macro F1 0.5346; validation Macro F1 0.5398; MCC 0.1014 | Internal integration only; deployment prohibited |
| `MDL-TL-MNB-TFIDF-v1.1.0-rc.1` | Primary challenger | `OPT-20260718-multinomial-naive-bayes-60fad40e22` | Validation Macro F1 0.5399; FAKE recall 0.4226 | Retain for a future governed comparison |
| `MDL-TL-LR-TFIDF-v1.1.0-rc.1` | Challenger | `OPT-20260718-logistic-regression-15115d5c12` | OOF Macro F1 0.5394; FAKE recall 0.4365 | Retain for recall/fairness investigation |

The tracked registry is [`ml/metadata/model-registry.json`](../../ml/metadata/model-registry.json). `MDL-TL-LSVM-TFIDF-v1.1.0-rc.1` is now the current **internal integration** package, with deployment status `integrated_not_deployment_approved` and a package-manifest checksum. It remains `production_model=false`: all tuned candidates are untested after tuning, have weak absolute performance, and remain subject to known source/template sensitivity. The r1 artifacts are invalidated and are not model candidates.

## Phase 4.1 explainability evidence

The current-model record now links the Phase 4.1 SHAP/LIME methods, train-only global-reference policy, unavailable confidence state, and [XAI artifact manifest](XAI_ARTIFACT_MANIFEST.json). This is model-behaviour evidence only: it does not alter the classifier, validation results, deployment status, or protected-test restriction. See the [Model Card](MODEL_CARD.md) and [XAI limitations](XAI_LIMITATIONS.md).

## Phase 4.2 transformer challengers

RDL-013 adds independent transformer registry entries without changing the current LinearSVC champion. Each entry is research-only and `production_model=false` by policy; a complete test result is non-selection benchmark evidence, not a promotion trigger.

| Model ID | Source | Registry status | Protected-test state | Disposition |
| --- | --- | --- | --- | --- |
| `MDL-TL-INDICBERT-v1.0.0-p42` | `ai4bharat/indic-bert` | `not_evaluated_access_limited` | None | Gated upstream repository rejected unauthenticated access before data use |
| `MDL-TL-DISTILBERT-v1.0.0-p42` | `distilbert/distilbert-base-uncased` | `not_evaluated_resource_limited` | None | Stopped after >86 CPU-minutes without checkpoint/results |
| `MDL-TL-BERT-BASE-v1.0.0-p42` | `google-bert/bert-base-uncased` | `not_evaluated_resource_limited` | None | Not started after lower-cost CPU limitation |
| `MDL-TL-ROBERTA-v1.0.0-p42` | `FacebookAI/roberta-base` | `not_evaluated_resource_limited` | None | Not started after lower-cost CPU limitation |

See [TRANSFORMER_BENCHMARK.md](TRANSFORMER_BENCHMARK.md), [CLASSICAL_VS_TRANSFORMERS.md](CLASSICAL_VS_TRANSFORMERS.md), and [MODEL_SELECTION_UPDATE.md](MODEL_SELECTION_UPDATE.md) for protocol, result-state, and non-promotion limits.
