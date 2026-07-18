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
