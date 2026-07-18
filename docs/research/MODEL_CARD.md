# Model Card - TruthLens Linear SVM Conditional Research Champion

## Model details

| Field | Value |
| --- | --- |
| Version | `TL-LSVM-TFIDF-v1.1.0-rc.1` |
| Algorithm | TF-IDF unigram/bigram + LinearSVC |
| Dataset | `TL-BFNK-EN-v1.0`, `DER-20260718-r2` |
| Status | `integrated_not_deployment_approved` |
| Validation Macro F1 / MCC | 0.5398 / 0.1014 |
| Protected test after tuning | Not accessed |

## Intended use

Internal research into a limited English BFNK-derived classification signal, with human review and documented uncertainty. It is not a fact-checking system, factual-verdict tool, calibrated probability model, or general Indian-media reliability assessor.

## Explainability

Each successful prediction exposes bounded local SHAP and LIME margin explanations. Global coefficient and mean-absolute-SHAP reports use only the frozen training partition. Positive values support the Fake-class margin; negative values support the Real-class margin. The explanation methods and limits are documented in [EXPLAINABLE_AI.md](EXPLAINABLE_AI.md) and [XAI_LIMITATIONS.md](XAI_LIMITATIONS.md).

## Responsible AI considerations

The model retains known source/template sensitivity, limited language and cohort coverage, weak absolute performance, uncalibrated output, and licence/content-rights constraints. Explanations make these behaviours inspectable but do not mitigate them. Any calibration, deployment, multilingual expansion, fairness claim, or consequential use requires a new governed decision and evidence package.

## Phase 4.2 benchmark relationship

The LinearSVC remains the current internal research champion and is not retrained or re-tested by Phase 4.2. Transformer candidates are separate research-only challengers governed by [RDL-013](../../research/decision-log/RDL-013-Transformer-Benchmark-and-Champion-Challenger-Boundary.md). IndicBERT is access-limited; DistilBERT exceeded the CPU window before checkpoint selection; BERT base and RoBERTa were not started on this host. No challenger has a promotion or deployment approval, and no benchmark outcome can automatically replace this model. See [DATA_CARD.md](DATA_CARD.md) and [MODEL_SELECTION_UPDATE.md](MODEL_SELECTION_UPDATE.md).

## Phase 4.3 ensemble relationship

Hard/weighted voting achieved validation Macro F1 0.5447 and soft voting 0.5443, but all are validation-only research challengers. The gains are within the existing practical-tie tolerance and introduce false-positive, resource, and explanation trade-offs; the OOF stacker is rejected for a severe FAKE-recall collapse. The current service and this Model Card therefore remain LinearSVC-specific. No ensemble output is calibrated confidence, a factual verdict, or a deployment-approved replacement. See [ENSEMBLE_EVALUATION.md](ENSEMBLE_EVALUATION.md).
