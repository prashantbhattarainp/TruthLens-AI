# EJ-021 - Transformer Benchmark

**Date:** 2026-07-18  
**Milestone:** Phase 4.2

## Completed work

- Added a standalone, research-only transformer benchmark harness under `ml/transformer_benchmark/`; it does not modify the FastAPI inference service or current LinearSVC package.
- Bound every run to the frozen derivative hash `978931f41ece219a3e3e27d052cfb35dfe557af02a604d6f913d4ad8e6ca59ad` and verifies the original 6,813 / 1,461 / 1,458 partition counts before model loading.
- Fixed the seed, token budget, optimizer, scheduler, batch sizes, epoch count, checkpoint-selection rule, metric suite, timing capture, hardware capture, checkpoint hashes, and protected-test ordering in code.
- Added validation and protected-test metrics: accuracy, macro/weighted precision/recall/F1, ROC-AUC, PR-AUC, MCC, Cohen's kappa, and a labelled confusion matrix.
- Added bounded false-positive/false-negative aggregate slices for political, health, breaking, short, long, and ambiguous-keyword cohorts. They are overlapping descriptive heuristics and never affect training or selection.
- Added a local-artifact boundary for transformer checkpoints and benchmark results, plus unit coverage for protocol binding, metrics, and raw-text exclusion.

## Runtime observations

The available host reported 12 logical CPUs, 15.6 GiB RAM (4.2 GiB available at measurement), 271.6 GiB free disk, and no CUDA-visible GPU. The project path exceeded the Windows filename limit during a PyTorch installation, so the benchmark runtime was installed in a short temporary virtual environment. The repository retains the declared dependencies; each run manifest records the exact resolved runtime versions. This operational workaround does not alter versioned source, data, or model artifacts.

`ai4bharat/indic-bert` is a gated upstream repository. Its attempted run correctly stopped before tokenization, training, validation, or protected-test access and wrote an ignored `not_evaluated` manifest. The remaining candidates are run serially on CPU to avoid memory contention; no result is reported until its complete artifact is present.

## Governance outcome

RDL-013 authorizes a bounded comparative study but not promotion. The current LinearSVC champion remains unchanged and may not re-access the protected test. A transformer metric, if produced, is research evidence only and cannot automatically replace the incumbent or support deployment, fact-checking, calibrated-confidence, or broad Indian-media claims.
