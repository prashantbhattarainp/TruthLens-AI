# RDL-013 - Transformer Benchmark and Champion-Challenger Boundary

**Date:** 2026-07-18  
**Status:** Accepted  
**Phase:** 4.2

## Decision

Phase 4.2 may run the pre-specified transformer candidates `ai4bharat/indic-bert`, `distilbert/distilbert-base-uncased`, `google-bert/bert-base-uncased`, and `FacebookAI/roberta-base` against the frozen `TL-BFNK-EN-v1.0` derivative `DER-20260718-r2` and split `SPL-TL-BFNK-EN-v1.0`.

Each candidate uses only the frozen `raw_text`, its native tokenizer, the fixed binary mapping `REAL=0` / `FAKE=1`, and the fixed Phase 4.2 training protocol. Transformer-native tokenization is model input handling, not a mutation of the dataset or the classical sparse-feature preprocessing contract. The protocol is fixed before results: seed 42, maximum sequence length 192, batch sizes 8/16, AdamW at 2e-5, linear 10% warm-up/decay, weight decay 0.01, gradient clipping 1.0, float32, no class weighting, and one epoch. The validation Macro F1 selects the checkpoint within that fixed schedule.

After validation checkpoint selection, each completed transformer candidate may receive exactly one protected-test evaluation. That result is descriptive benchmark evidence only: it may not select a champion, tune a configuration, approve deployment, or make a factual-verdict claim. A candidate that cannot load, train, or evaluate records `not_evaluated` with the concrete reason and receives no substitute score.

The existing LinearSVC champion must not re-access the protected test. Its post-tuning comparison evidence remains frozen validation Macro F1 0.5398 and MCC 0.1014. The historical Phase 3.8 test result is explicitly excluded from Phase 4.2 ranking because it predates the Phase 3.9 tuning.

## Champion-challenger policy

The LinearSVC remains the internal, non-deployment-approved champion. Every transformer is a research-only challenger, even if it exceeds the incumbent on a benchmark metric. Promotion requires a separate governed decision with reproduced evidence, a new release package review, data-rights review, calibration and robustness/fairness evidence, human-review controls, and explicit deployment approval. This phase changes neither the public API nor the production architecture, so no ADR is required.

## Consequences

The model registry records one independent entry per transformer, including incomplete and access-limited outcomes. Benchmark artifacts, checkpoints, model downloads, and per-run logs remain local and ignored; their manifests retain resolved revisions, hardware, package versions, timing, metrics, checksums, and error-slice aggregates. No raw article text is written into reports.
