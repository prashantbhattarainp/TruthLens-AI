# Model Card - TruthLens Linear SVM Conditional Research Champion

## Model details

| Field | Value |
| --- | --- |
| Version | `TL-LSVM-TFIDF-v1.1.0-rc.1` |
| Algorithm | TF-IDF unigram/bigram + LinearSVC |
| Dataset | `TL-BFNK-EN-v1.0`, `DER-20260718-r2` |
| Status | `integrated_not_deployment_approved` |
| Production model | No (`production_model=false`) |
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

## Phase 4.4 multilingual relationship

Phase 4.4 adds a separate research preprocessing/audit layer, not multilingual model support. The frozen English LinearSVC accepted audited Unicode text but has no validated Hindi or Hinglish fake-news performance claim. The English-labelled derivative contains only 9 Devanagari-bearing and 2 conservative Hinglish-heuristic validation records; their descriptive slice metrics are not valid language benchmarks. IndicBERT remains access-limited without a checkpoint or metric. No model, preprocessing package, XAI output, API field, or deployment status changed. See [MULTILINGUAL_EVALUATION.md](MULTILINGUAL_EVALUATION.md) and [RDL-015](../../research/decision-log/RDL-015-Multilingual-Evaluation-and-Data-Boundary.md).

## Phase 4.5 robustness, calibration, and responsible use

The integrity-checked champion was evaluated on frozen validation-only deterministic stressors. It is not robustly invariant: capitalization changes flip 29.0% of labels, neutral appended context flips 27.0%, and stop-word deletion flips 11.6%. The inference-only ablation diagnostics also show lower Macro F1 without frozen preprocessing (0.5127) or bigram influence (0.5024). These findings do not change the package or qualify as retrained-component effects.

The LinearSVC remains uncalibrated. A non-fitted sigmoid-margin diagnostic produced ECE/Brier proxies of 0.0620/0.2395; they are neither probabilities nor confidence, and `confidence` remains unavailable. Source/topic/length/time/language-appearance slices are descriptive only; publisher-level generalization, demographic fairness, and Hindi/Hinglish performance are not established. The model remains unsuitable for automated factual verdicts, reliability/risk scoring, or deployment without new governed data, calibration, robustness, fairness, rights, monitoring, and human-review evidence. See [RELIABILITY_ASSESSMENT.md](RELIABILITY_ASSESSMENT.md) and [RDL-016](../../research/decision-log/RDL-016-Robustness-Reliability-and-Fairness-Boundary.md).

## Phase 4.6 final selection and deployment guidance

Phase 4 finalization retains this model as the **final internal research champion**, not as a production model. Hard/weighted voting reached Macro F1 0.5447 and soft voting 0.5443 on the same frozen validation set, but their gains are inside the 0.005 practical-tie tolerance and add false-positive, operational, and explanation trade-offs. Transformer candidates have no completed metrics; multilingual evidence remains compatibility-only. The retained LinearSVC is the most integrated and explainable documented option, not a validated best model for real-world fake-news detection.

Use only for bounded internal research with human review and explicit uncertainty. Do not expose its margin as confidence, use it to make a factual verdict, prioritize people/content by risk, or describe it as Hindi/Hinglish-capable. Any deployment consideration requires a new governed data/model release, post-tuning evaluation plan, fitted calibration evidence, robustness and fairness remediation/evaluation, data-rights review, monitoring, incident response, and meaningful human-review controls. See the [publication package](publication/README.md).
