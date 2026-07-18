# BERT Base Evaluation

**Model:** `google-bert/bert-base-uncased`  
**Status:** `not_evaluated_resource_limited`
**Protected test:** Not accessed

BERT base is retained as the full English encoder reference for Phase 4.2. Its training configuration, dataset derivative, labels, split, validation checkpoint rule, metric suite, and protected-test ordering are exactly those in [TRANSFORMER_BENCHMARK.md](TRANSFORMER_BENCHMARK.md).

The host is CPU-only with limited free memory. The smaller public DistilBERT candidate exceeded 86 CPU-minutes without a checkpoint or result artifact, so BERT base was not started on this host. It has no score, timing, checkpoint, error analysis, or protected-test result. It cannot be compared, promoted, or described as underperforming until a complete local evidence bundle exists.
