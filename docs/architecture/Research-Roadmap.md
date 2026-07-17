# TruthLens AI Research and Implementation Roadmap

**Updated:** 2026-07-17  
**Current position:** Phase 3 - Milestone 3.1 complete (documentation only)

## Completed phases

| Phase                            | Outcome                                                                                                        | Status   |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------- | -------- |
| Phase 1 - Project Foundation     | Independent frontend, backend, and ML-service infrastructure; observability and service-health communication.  | Complete |
| Phase 2 - Application Workflow   | Prediction UI, Node.js API contract, frontend/backend integration, and a deterministic Python ML-service mock. | Complete |
| Phase 3.1 - Research Methodology | Research scope, data governance, baseline protocol, evaluation, explainability, and reproducibility plan.      | Complete |

## Phase 3 - Machine Learning and Research

| Milestone                                     | Planned outcome                                                                                              | Prerequisite                          |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------------- |
| 3.2 - Dataset governance package              | Candidate register, dataset-card template, licence-review checklist, and acquisition approval gate.          | RDL-001                               |
| 3.3 - Approved data acquisition and manifests | Permission-aware data acquisition, immutable dataset manifests, checksums, and source/label audit.           | Approved candidate and licence review |
| 3.4 - Data quality and split protocol         | Audit reports, duplicate/near-duplicate handling, grouped/temporal split manifest, and leakage checks.       | Versioned approved dataset            |
| 3.5 - Configurable preprocessing              | Tested spaCy-based preprocessing module with versioned configuration.                                        | Locked development split              |
| 3.6 - Features and transparent baselines      | Pluggable TF-IDF features and versioned Naive Bayes, Logistic Regression, and Linear SVM baseline artefacts. | 3.5                                   |
| 3.7 - Evaluation and experiment tracking      | Reproducible metrics reports, experiment records, comparisons, and error-analysis outputs.                   | 3.6                                   |
| 3.8 - Explainability research                 | Bounded baseline feature explanations, stability checks, and documented limitations.                         | 3.7                                   |
| 3.9 - Research reporting                      | Artifact-driven notebooks, figures, model cards, and paper-ready result package.                             | 3.7 and 3.8                           |

## Later platform phases

| Phase                          | Planned focus                                                                                                             |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| Phase 4 - Product analytics    | Persisted prediction history, dashboard analytics, model-comparison page, and user-facing system health.                  |
| Phase 5 - Advanced modelling   | IndicBERT/DistilBERT, multilingual cohorts, alternative feature extractors, calibration, and SHAP/LIME comparisons.       |
| Phase 6 - Production hardening | Authentication, PostgreSQL migration, REST API versioning, deployment, monitoring, security review, and drift governance. |

## Governance gates

No model may be described as research-evaluated until it has a versioned dataset and split, frozen configuration, evaluation report, model metadata, and experiment record. No data acquisition proceeds until the candidate's legal and methodological review is approved.
