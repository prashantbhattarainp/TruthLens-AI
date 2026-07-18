# TruthLens AI Project Research Summary

## Motivation

TruthLens AI investigates how a fake-news classification signal for Indian digital-media research can be built and reported transparently. The project deliberately distinguishes a model's learned text pattern from factual truth, confidence, source credibility, and deployment readiness.

## Methodology

The completed work freezes the English BFNK-derived dataset identity, derivative, split, label mapping, model package, and experiment boundaries. The final internal research champion is TF-IDF unigram/bigram plus LinearSVC (`TL-LSVM-TFIDF-v1.1.0-rc.1`), served through an integrity-checked FastAPI package behind the existing frontend -> Node.js -> Python boundary. The model was selected on validation evidence only and is not approved for deployment.

## Phase 4 experiments

- Phase 4.1 added bounded local SHAP/LIME margin explanations and train-only aggregate XAI figures.
- Phase 4.2 pre-specified transformer benchmarks but produced no completed transformer metric because of gated access and CPU limitations.
- Phase 4.3 evaluated classical ensembles. Hard/weighted voting reached Macro F1 0.5447, within the practical tie tolerance of the incumbent's 0.5398.
- Phase 4.4 established Unicode/Hindi/Hinglish processing diagnostics but found no valid Hindi or Hinglish fake-news benchmark.
- Phase 4.5 assessed reliability. Capitalization and neutral expansion changed 29.0% and 27.0% of validation predictions; calibration remains unavailable.

## Findings and conclusion

The LinearSVC is retained for internal research because it is reproducibly packaged, already integrated, and explainable on its exact margin. That decision does not make it a strong or safe real-world detector: Macro F1 is 0.5398, MCC is 0.1014, FAKE recall is 0.3183, it is sensitive to surface changes, and it is uncalibrated. No evaluated alternative clears the combined practical, operational, explanation, and governance requirements for replacement.

The project’s central contribution is therefore a disciplined research package: it records what was measured, what was not measured, and what evidence must exist before stronger multilingual, fairness, generalization, calibration, or deployment claims can be made. See the [publication package](publication/README.md) and [Phase 4 summary](../PHASE4_SUMMARY.md).
