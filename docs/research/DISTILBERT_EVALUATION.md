# DistilBERT Evaluation

**Model:** `distilbert/distilbert-base-uncased`  
**Status:** `not_evaluated_resource_limited`
**Protected test:** Not accessed

DistilBERT was the first executable CPU challenger because its architecture is smaller than the full base encoders and it is available without the IndicBERT gated-access requirement. It used only the fixed Phase 4.2 protocol in [TRANSFORMER_BENCHMARK.md](TRANSFORMER_BENCHMARK.md).

The CPU-only run exceeded 86 CPU-minutes without reaching a checkpoint or result artifact and was stopped. Validation checkpoint selection and protected-test evaluation never occurred. Consequently, this document contains no provisional score, inferred confusion matrix, error analysis, timing claim, or ranking conclusion. The ignored `resource-limitation.json` records the host context and stop condition.

A future rerun needs an appropriate GPU or a separately approved, reproducible compute plan. It must use the unchanged protocol or be recorded under a new governed decision. A resource or runtime failure is `not_evaluated`, not a negative model result.
