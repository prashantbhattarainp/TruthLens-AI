# TruthLens AI Research and Implementation Roadmap

**Updated:** 2026-07-18  
**Current position:** Phase 3 complete at the internal-integration boundary; approval is required before Phase 4. Public deployment remains blocked by RDL-011.

## Completed phases

| Phase                            | Outcome                                                                                                        | Status   |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------- | -------- |
| Phase 1 - Project Foundation     | Independent frontend, backend, and ML-service infrastructure; observability and service-health communication.  | Complete |
| Phase 2 - Application Workflow   | Prediction UI, Node.js API contract, frontend/backend integration, and a deterministic Python ML-service mock. | Complete |
| Phase 3.1 - Research Methodology | Research scope, data governance, baseline protocol, evaluation, explainability, and reproducibility plan.      | Complete |
| Phase 3.2 - Dataset Landscape    | Candidate comparison, scoring, licence assessment, conditional role-separated selection, and registry evidence. | Complete |
| Phase 3.3 - Data Acquisition     | Immutable BharatFakeNewsKosh v1 acquisition, metadata, integrity checks, and read-only validation evidence.     | Complete |
| Phase 3.4 - EDA and Assessment   | Read-only data profile, aggregate statistics, quality assessment, preprocessing recommendations, and vector figures. | Complete |
| Phase 3.5 - Preprocessing Pipeline | Modular spaCy pipeline, frozen configuration contract, validation, logging, and fixture verification; no raw data run. | Complete |
| Phase 3.6 - Feature Engineering | Modular Count and TF-IDF representations, configuration, validation, experiment tracking, and fixture verification; no feature-data run. | Complete |
| Phase 3.7 - Baseline Experiment Framework | Logistic Regression, Multinomial Naive Bayes, Linear SVM, fold-safe feature fitting, metrics, tracking, and synthetic fixture verification; no research model run. | Complete |
| Phase 3.7.5 - Dataset Finalization | Frozen English cohort, source-label mapping, duplicate/leakage rules, split strategy, manifest, versioning, and experiment-readiness contract; no data-bearing output. | Complete |
| Phase 3.8 - Model Evaluation | Governed r2 derivative, grouped baseline CV, validation-led Linear SVM selection, one-time protected test evaluation, statistical/error/feature analysis, and registry evidence; research candidate only. | Complete |
| Phase 3.9 - Hyperparameter Optimization | Training-only grouped-CV GridSearchCV for the three approved baselines, frozen-validation comparison, conditional champion/challenger strategy, and production-candidate definition; no post-tuning test access. | Complete |
| Phase 3.10 - Production Model Integration | Versioned candidate packaging, integrity-checked lazy loading, Python/Node API integration, structured logging, and final Phase 3 documentation; integrated but not deployment-approved. | Complete |

## Phase 3 - Machine Learning and Research

| Milestone                                     | Planned outcome                                                                                              | Prerequisite                          |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------------- |
| 4.1 - Explainability and research reporting | Bounded feature explanations, stability checks, reports, figures, model cards, and paper-ready result package. | Phase 3 approval and a new governed protocol where needed |

## Later platform phases

| Phase                          | Planned focus                                                                                                             |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| Phase 4 - Product analytics    | Persisted prediction history, dashboard analytics, model-comparison page, and user-facing system health.                  |
| Phase 5 - Advanced modelling   | IndicBERT/DistilBERT, multilingual cohorts, alternative feature extractors, calibration, and SHAP/LIME comparisons.       |
| Phase 6 - Production hardening | Authentication, PostgreSQL migration, REST API versioning, deployment, monitoring, security review, and drift governance. |

## Governance gates

No model may be described as research-evaluated until it has a versioned dataset and split, frozen configuration, evaluation report, model metadata, and experiment record. No data acquisition proceeds until the candidate's legal and methodological review is approved.
