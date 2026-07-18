# Research Documentation

This directory is the tracked source of truth for the current TruthLens research package. Governed raw data, fitted model packages, checkpoints, and local run artifacts remain outside Git by design. The final Phase 4 publication consolidation is in [publication](publication/README.md).

## Core records

| Document | Purpose |
| --- | --- |
| [Project research summary](PROJECT_RESEARCH_SUMMARY.md) | Motivation, methodology, experiments, findings, and conclusion |
| [Experiment Registry](EXPERIMENT_REGISTRY.md) | Phase 4 experiment status and data-access restrictions |
| [Model Registry](MODEL_REGISTRY.md) | Candidate lifecycle and final internal champion state |
| [Model Card](MODEL_CARD.md) | Intended use, limitations, ethics, performance, and deployment guidance |
| [Data Card](DATA_CARD.md) | Frozen derivative identity, handling, and limitations |
| [Phase 4 publication package](publication/README.md) | Final tables, figures, reproducibility, validity, and handoff checklist |
| [Figures index](publication/FINAL_FIGURES_INDEX.md) | Captions and evidence limits for tracked figures |

## Phase 4.1: Explainable AI

- [Explainable AI framework](EXPLAINABLE_AI.md)
- [Explanation methodology](EXPLANATION_METHODOLOGY.md)
- [Explanation strategy](EXPLANATION_STRATEGY.md)
- [Feature importance](FEATURE_IMPORTANCE.md)
- [SHAP analysis](SHAP_ANALYSIS.md)
- [LIME analysis](LIME_ANALYSIS.md)
- [XAI evaluation report](XAI_EVALUATION_REPORT.md)
- [XAI limitations](XAI_LIMITATIONS.md)
- [XAI artifact manifest](XAI_ARTIFACT_MANIFEST.json)

## Phase 4.2: Transformer benchmark

- [Transformer benchmark](TRANSFORMER_BENCHMARK.md)
- [Classical versus transformers](CLASSICAL_VS_TRANSFORMERS.md)
- [Resource comparison](RESOURCE_COMPARISON.md)
- [IndicBERT evaluation](INDICBERT_EVALUATION.md), [DistilBERT evaluation](DISTILBERT_EVALUATION.md), [BERT base evaluation](BERT_BASE_EVALUATION.md), and [RoBERTa evaluation](ROBERTA_EVALUATION.md)
- [Model selection update](MODEL_SELECTION_UPDATE.md)

## Phase 4.3: Ensembles and hybrids

- [Ensemble evaluation](ENSEMBLE_EVALUATION.md)
- [Ensemble comparison](ENSEMBLE_COMPARISON.md)
- [Hybrid model analysis](HYBRID_MODEL_ANALYSIS.md)
- [Production deployment impact](PRODUCTION_DEPLOYMENT_IMPACT.md)

## Phase 4.4: Multilingual assessment

- [Multilingual evaluation](MULTILINGUAL_EVALUATION.md)
- [Hindi dataset analysis](HINDI_DATASET_ANALYSIS.md)
- [Hinglish analysis](HINGLISH_ANALYSIS.md)
- [Language comparison](LANGUAGE_COMPARISON.md)
- [Multilingual error analysis](MULTILINGUAL_ERROR_ANALYSIS.md)
- [Multilingual research findings](MULTILINGUAL_RESEARCH_FINDINGS.md)

## Phase 4.5: Reliability assessment

- [Robustness evaluation](ROBUSTNESS_EVALUATION.md)
- [Calibration analysis](CALIBRATION_ANALYSIS.md)
- [Bias and fairness analysis](BIAS_AND_FAIRNESS.md)
- [Generalization study](GENERALIZATION_STUDY.md)
- [Error analysis report](ERROR_ANALYSIS_REPORT.md)
- [Ablation study](ABLATION_STUDY.md)
- [Model limitations](MODEL_LIMITATIONS.md)
- [Reliability assessment](RELIABILITY_ASSESSMENT.md)
- [Phase 4.5 artifact manifest](PHASE_4_5_ARTIFACT_MANIFEST.json)

## Governance and historical availability

The [Research Decision Log](../../research/decision-log/README.md), [Engineering Journal](../engineering-journal/README.md), [ADRs](../adr/README.md), and [Phase 3 summary](../PHASE3_SUMMARY.md) provide the tracked governance context.

Earlier primary Phase 1-3 research Markdown files named in older indexes are not present in this checkout. Their unavailable links have not been recreated or inferred in Phase 4.6; the tracked files above, registries, cards, manifests, and decision records are the reliable basis for the final package.
