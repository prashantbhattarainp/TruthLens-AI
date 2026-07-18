# RDL-007: Baseline Experiment Framework

**Status:** Accepted for Phase 3.7  
**Date:** 2026-07-18  
**Related documents:** [Experiment Framework](../../docs/research/EXPERIMENT_FRAMEWORK.md), [Baseline Model Report](../../docs/research/BASELINE_MODEL_REPORT.md), [Model Comparison Plan](../../docs/research/MODEL_COMPARISON_PLAN.md), [Reproducibility Guide](../../docs/research/REPRODUCIBILITY_GUIDE.md)

## Context

RDL-001 specifies transparent TF-IDF baseline models and five-fold stratified group cross-validation where groups are available. RDL-004 through RDL-006 retain a blocking data-readiness gate: no approved BFNK derivative, label mapping, split, feature artifact, or model result exists. Phase 3.7 therefore needs testable experimental infrastructure without presenting a synthetic model as research evidence.

## Decisions

1. Implement a closed Phase 3.7 model registry containing only Logistic Regression, Multinomial Naive Bayes, and Linear SVM. The model factory rejects every other model family.
2. Implement a versioned, hashable experiment configuration with hyperparameters, random seed, CV settings, and Macro F1 as the required primary metric. The default is five-fold Stratified K-Fold; Stratified Group K-Fold is available when an approved group definition is supplied.
3. Fit the Phase 3.6 feature extractor independently inside each CV training fold, then transform only that fold's held-out rows. Vocabulary and TF-IDF weights must never be fitted on CV validation, validation-partition, or test-partition text.
4. Generate a collision-resistant experiment ID automatically. Record lineage, including a required approved dataset/derivative SHA-256 hash; preprocessing/feature versions and hashes; configuration/hyperparameters; deterministic settings; timings; accuracy; precision; recall; macro/weighted F1; ROC-AUC where a continuous score exists; confusion matrix; classification report; out-of-fold predictions; timestamps; logs; and checksums.
5. Retain each completed run as a self-contained artifact bundle with canonical `config.json` and `metrics.json`, classification report, numeric and PNG confusion matrix, notes, and an immutable filesystem-discoverable local experiment-registry sidecar. This applies MLflow-style lineage and artifact principles without adding MLflow or a tracking service.
6. Create a candidate model-registry record with model version, dataset version, feature-engineering version/configuration hash, experiment ID, aggregate performance evidence, artifact location, training date, and notes. Candidate is not equivalent to evaluated, approved, deployable, or fact-checking.
7. Restrict Phase 3.7 execution evidence to synthetic fixtures until RDL-004 is resolved. No raw/processed BFNK data access, derivative, split, real model artifact, real comparison, evaluation claim, or model-registry entry is authorised.

## Consequences

- The project can reproduce the complete baseline experiment workflow once governed inputs exist, but has no research baseline result.
- Feature-fold fitting prevents a common CV leakage path that would otherwise inflate lexical-baseline estimates.
- Continuous Linear SVM decision scores may support ROC-AUC ranking, but are not recorded as calibrated confidence.
- Model artifacts are retained as candidate evidence only when a future approved run produces the complete artifact bundle.

## Architecture impact

None. The experimentation package is internal to the existing ML research boundary; it changes no public API, service contract, deployment topology, model-serving behavior, or deterministic mock prediction flow. No ADR is created.
