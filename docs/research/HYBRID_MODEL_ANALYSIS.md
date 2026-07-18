# Hybrid Model Analysis - Phase 4.3

## Classical-transformer hybrid status

**Not evaluated.** Phase 4.2 produced no completed transformer checkpoint, prediction artifact, or validation metric: IndicBERT is gated, DistilBERT exceeded the CPU window before checkpoint selection, and BERT/RoBERTa were not started. Combining a classical score with a missing transformer score would be fabricated evidence, so no hybrid metric is reported.

## Classical ensemble findings

The Phase 4.3 classical ensembles show that combining differently biased sparse models can change the recall/false-positive trade-off. Hard voting improves validation Macro F1 from 0.5398 to 0.5447 while decreasing accuracy from 0.5941 to 0.5825. Soft voting has the best ranking metrics, but also increases false positives. The stacker illustrates that an OOF-trained meta-model is not automatically stable: its FAKE recall collapsed to 0.0174 (10/575).

## Explainability and production implications

The existing SHAP/LIME implementation applies to the LinearSVC margin only. A vote can expose component labels and fixed weights, but it does not create a faithful combined SHAP/LIME explanation. A stacker further obscures the relationship between text features and the output. No Phase 4.3 variant is integrated into the API, and no ensemble has calibrated confidence or factual-verdict capability.

## Future prerequisite

A real hybrid study requires a separately governed, completed transformer artifact on suitable compute; a frozen feature-alignment rule; train-only OOF/meta-training evidence; validation-only selection; and a new explanation/operational review. It cannot reuse Phase 4.2's absent results or the current protected-test partition.
