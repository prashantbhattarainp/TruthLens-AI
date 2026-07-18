# Explainable AI Framework

## Scope

Phase 4.1 makes the existing `TL-LSVM-TFIDF-v1.1.0-rc.1` classifier inspectable. It does not retrain, calibrate, replace, or deploy the model. The framework emits local SHAP and LIME explanations with each successful prediction and provides governed global feature analysis for research reporting.

## Research contribution

The framework connects a user-facing classification signal to transparent feature-level behaviour. It supports reproducible inspection of what moves the classifier's Fake-class margin, documents uncertainty honestly, and gives future multilingual or neural models a common explanation-service boundary. This improves transparency and human-centered review, but does not make the system a fact checker.

## Components

| Component | Purpose |
| --- | --- |
| `ShapTextExplainer` | Additive local contributions for the sparse LinearSVC margin. |
| `LimeTextMarginExplainer` | Deterministic, perturbation-based local margin surrogate. |
| `ExplanationService` | Reuses one successful prediction context and returns bounded metadata. |
| Feature importance utilities | Aggregate train-only coefficient and mean-absolute-SHAP rankings. |
| Visualization utilities | Produce publication-oriented figures without raw documents. |

See [the methodology](EXPLANATION_METHODOLOGY.md), [evaluation report](XAI_EVALUATION_REPORT.md), and [limitations](XAI_LIMITATIONS.md).
