# Experiment Registry

**Scope:** Reproducible experiment-record design
**Status:** Empty by design — no model or evaluation experiment has been run
**Related documents:** [Research methodology](RESEARCH_METHODOLOGY.md), [Model registry](MODEL_REGISTRY.md)

## Purpose

The experiment registry makes experiments comparable, repeatable, and resistant to selective reporting. It records proposed, successful, failed, and invalidated runs; it does not rank experiments across different datasets or split conditions as though they were identical.

## Required experiment record

| Field | Required evidence |
| --- | --- |
| Experiment ID and status | Immutable ID and proposed, running, completed, failed, invalidated, or archived status. |
| Research objective | Research question/hypothesis and the decision the run is allowed to inform. |
| Dataset and split | Immutable dataset, derivative, label-mapping, and split IDs with checksums. |
| Cohort definition | Language, source, time, topic, text-unit, inclusion/exclusion, and task-scope rules. |
| Code and environment | Repository revision, dependency lock/version evidence, operating environment, hardware notes where material. |
| Randomness control | Seed(s), deterministic settings, and known nondeterministic components. |
| Preprocessing and features | Versioned configuration, enabled stages, vectorizer settings, fitted-artifact references. |
| Model configuration | Algorithm, hyperparameters, class weighting/resampling policy, threshold, and calibration configuration. |
| Validation protocol | Group rule, cross-validation design, model-selection rule, and test-set access statement. |
| Outputs | Metrics, confusion matrix, calibration/ranking outputs where valid, timing, uncertainty estimate, cohort slices, and error-analysis artefacts. |
| Interpretation | Limitations, leakage-audit outcome, deviations, and whether the hypothesis was supported. |
| Artefact integrity | Log, report, plot, model, and metadata locations plus SHA-256 checksums. |
| Run outcome | Completion/failure reason, reviewer, creation time, and parent experiment where applicable. |

## Comparability rule

Experiments are directly comparable only if the dataset derivative, label-mapping version, split, task definition, and metric definitions match. A different corpus, split, label policy, feature protocol, or evaluation condition is a separate comparison cohort and must be labelled as such.

## Lifecycle rules

- A proposed experiment records its question and design before execution.
- A failed run remains registered with safe diagnostic information and never disappears from the research record.
- An invalidated run remains historical and states which data, code, or protocol issue invalidated it.
- A completed run may be linked to a model candidate only after its artefacts and report are verified.
- A test result is appended to the frozen run record; it is not repeatedly overwritten during tuning.

## Current entries

Phase 3.8 contains three comparable r2 experiments. They share `TL-BFNK-EN-v1.0`, derivative `DER-20260718-r2`, split `SPL-TL-BFNK-EN-v1.0`, seed 42, conservative preprocessing (`52ce…3976f`), and TF-IDF (`fdec…4938`).

| Experiment ID | Model | CV Macro F1 | Registry status |
| --- | --- | ---: | --- |
| `EXP-20260717-logistic-regression-e7612c6153` | Logistic Regression | 0.4976 | Completed comparison candidate |
| `EXP-20260717-multinomial-naive-bayes-7869d12afd` | Multinomial NB | 0.4251 | Completed comparison candidate |
| `EXP-20260717-linear-svm-177d71e9c9` | Linear SVM | 0.5323 | Completed; selected on validation Macro F1 |

The r1 derivative/experiments are preserved but invalidated because a missing-cell conversion defect introduced literal `nan` text tokens. They are excluded from all results and registries. Deterministic mock API responses and synthetic fixtures remain excluded.

## Feature-extraction run records

The Phase 3.6 framework creates one `feature-experiment.json` only for a future approved feature-fitting run. Its `experiment_id` must use the registry's immutable experiment-ID convention and it must record dataset version, split ID, fit partition, feature method, full feature configuration and SHA-256 hash, source-manifest hash, timestamps, duration, notes, and validation outcome. The associated matrix, ordered vocabulary, record-order IDs, fitted extractor, JSONL events, and checksummed manifest remain one reproducible feature-artifact bundle.

A feature-only record does not claim a model result. It becomes comparable to another feature run only when the parent derivative, preprocessing configuration, split, fit partition, and feature protocol match. Vocabulary- and IDF-learning methods must be fitted on the training partition only.

## Baseline-model experiment records

The Phase 3.7 framework generates an experiment ID and captures dataset/split lineage (including a required approved dataset/derivative SHA-256 hash), preprocessing and feature versions/configuration hashes, model/version/hyperparameters, random seed, CV policy, timing, complete metrics, out-of-fold predictions, candidate registry record, lifecycle logs, and checksums. A self-contained artifact bundle includes canonical configuration and metrics summaries, classification report, numeric and PNG confusion matrix, notes, and a discoverable `experiment-registry-entry.json` sidecar. `LocalExperimentRegistry` discovers these immutable sidecars below `ml/data/experiments/`; it is deliberately filesystem-based rather than a mutable tracking service. It fits the feature extractor within each CV training fold to prevent vocabulary/IDF leakage. These records become registry entries only after an approved data-bearing run; a synthetic fixture run is excluded.
