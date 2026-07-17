# RDL-001: Research Methodology and Reproducibility Baseline

**Status:** Accepted for Phase 3 planning  
**Date:** 2026-07-17  
**Related document:** [Research Methodology](../Research-Methodology.md)

## Context

TruthLens AI is intended to support a publishable study of explainable fake-news detection for Indian digital media. The project needed a research protocol before dataset acquisition or ML implementation so that results are comparable, legally governed, and reproducible.

## Decisions

1. The primary research scope is Indian digital media. Generic international corpora may be auxiliary or external benchmarks only and must be reported as such.
2. Dataset selection is gated by documented provenance, label policy, Indian-media relevance, licensing, copyright, privacy, and source/language/time coverage.
3. Each dataset release, processed derivative, and split receives immutable identifiers, manifests, checksums, and parent relationships.
4. The initial study will be English-first and binary only after the label policy is approved. Multilingual support is a separately measured future expansion.
5. The default development split is 70/15/15, stratified where feasible and grouped to prevent source, temporal, and duplicate leakage. The exact split is frozen after data audit.
6. TF-IDF with Multinomial Naive Bayes, Logistic Regression, and Linear SVM is the transparent baseline benchmark. Feature extraction remains modular for later contextual embeddings.
7. Macro F1 is the primary selection metric. Per-class metrics, calibration, ranking metrics where valid, time costs, confusion matrices, and cohort slices are required supporting evidence.
8. Initial explanations describe model-influential text features, not factual proof. Future LIME/SHAP analyses must be evaluated for stability and limitations.
9. Every experiment stores immutable data/split references, configuration, seed, code/environment details, metrics, logs, reports, and artefact hashes. Failed runs are retained.

## Consequences

- Dataset acquisition cannot begin until candidate governance review is complete.
- Reported model performance will be narrower but more defensible because leakage and scope controls are mandatory.
- The ML service must later produce versioned artefacts and metadata instead of transient model files.
- Research notebooks may analyse saved outputs but cannot become the sole implementation of the experimental pipeline.

## Alternatives considered

| Alternative                                                              | Reason not selected                                                                                |
| ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| Start model training with an easily available generic fake-news dataset. | Would not establish relevance to Indian digital media or satisfy the required governance protocol. |
| Use a random row-level split only.                                       | Fails to control duplicate, source, and temporal leakage common in news corpora.                   |
| Optimise accuracy alone.                                                 | Can hide minority-class failure and does not support a robust imbalance analysis.                  |
| Treat explanation keywords as fact-check evidence.                       | Misstates what a text classifier can establish and creates misleading user expectations.           |

## Architecture impact

None. This decision defines research governance and future implementation requirements only. The existing frontend, Node.js backend, and Python ML-service service boundary is unchanged; no ADR is created.
