# DistilBERT Evaluation

**Model:** `distilbert/distilbert-base-uncased`  
**Status:** `benchmark_run_in_progress`  
**Protected test:** Not yet accessed

DistilBERT is the first executable CPU challenger because its architecture is smaller than the full base encoders and it is available without the IndicBERT gated-access requirement. It is trained only with the fixed Phase 4.2 protocol in [TRANSFORMER_BENCHMARK.md](TRANSFORMER_BENCHMARK.md).

No validation or protected-test metric is reported until the run has selected its fixed-schedule validation checkpoint, saved the ignored checkpoint and manifest, and completed exactly one non-selection test evaluation. Consequently, this document contains no provisional scores, inferred confusion matrix, or ranking claim.

When complete, the report must link the timestamped ignored artifact, resolved model revision, package/hardware manifest, validation/test metric suite, training and inference timing, and false-positive/false-negative aggregate slices. A resource or runtime failure will be recorded as `not_evaluated`, not as a negative model result.
