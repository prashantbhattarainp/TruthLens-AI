# Transformer Benchmark - Phase 4.2

**Scope:** Frozen-data, research-only comparison of the existing LinearSVC candidate with four transformer challengers.  
**Decision authority:** [RDL-013](../../research/decision-log/RDL-013-Transformer-Benchmark-and-Champion-Challenger-Boundary.md).  
**Status:** Complete at a documented resource-limited evidence boundary; no incomplete candidate has a performance claim.

## Frozen inputs and fair-comparison boundary

| Control | Fixed value |
| --- | --- |
| Dataset / derivative | `TL-BFNK-EN-v1.0` / `DER-20260718-r2` |
| Dataset SHA-256 | `978931f41ece219a3e3e27d052cfb35dfe557af02a604d6f913d4ad8e6ca59ad` |
| Split | `SPL-TL-BFNK-EN-v1.0`: train 6,813; validation 1,461; protected test 1,458 |
| Labels | `REAL=0`, `FAKE=1` |
| Input text | Frozen `raw_text`; no label, source, split, or text mutation |
| Classical model | Existing TF-IDF + LinearSVC candidate, validation-only comparison evidence |
| Transformer input | Each model's native tokenizer; this is model input handling, not a new preprocessing derivative |

The tuned LinearSVC may not re-access the protected test. Its Phase 3.8 test metric predates Phase 3.9 tuning and is not used in this benchmark table or any selection decision.

## Pre-specified training protocol

| Setting | Value |
| --- | --- |
| Seed / precision / device policy | 42 / float32 / CUDA if available, otherwise CPU |
| Sequence length | 192 tokens, truncation with model-native tokenizer |
| Batch sizes | train 8; validation/test 16; no gradient accumulation |
| Optimizer | AdamW, LR 2e-5, betas 0.9/0.999, epsilon 1e-8, weight decay 0.01 |
| Schedule | One epoch; linear 10% warm-up then decay; gradient clipping 1.0 |
| Class imbalance | No weighting; the frozen 60.7% / 39.3% class mix is retained |
| Checkpoint rule | Highest validation Macro F1 within the fixed schedule |
| Test rule | One final, non-selection evaluation only after checkpoint selection |

The runner verifies the input SHA-256 and partition counts before it contacts a model repository. Every ignored local evidence bundle records package versions, resolved model revision, hardware, timing, checkpoint hashes, all metrics, and aggregate error slices.

## Candidate evidence state

| Candidate | Upstream identifier | State | Protected test | Reason / next action |
| --- | --- | --- | --- | --- |
| IndicBERT | `ai4bharat/indic-bert` | Not evaluated | Not accessed | Upstream gated-repository access was rejected before data access. A Hugging Face account must accept the model conditions and supply credentials before a new governed run. |
| DistilBERT | `distilbert/distilbert-base-uncased` | Not evaluated | Not accessed | Fixed CPU run exceeded 86 CPU-minutes without a checkpoint/result artifact and was stopped. |
| BERT base | `google-bert/bert-base-uncased` | Not evaluated | Not accessed | Not started: the larger encoder is impractical after the DistilBERT CPU limitation. |
| RoBERTa base | `FacebookAI/roberta-base` | Not evaluated | Not accessed | Not started: the larger encoder is impractical after the DistilBERT CPU limitation. |

No blank cell in this table represents a zero score. A candidate becomes `evaluated_research_only` only when its local run manifest and result bundle are complete. The local `resource-limitation.json` retains the DistilBERT stop evidence; it is not an evaluation artifact.

## Evaluation and error analysis

Completed candidates report accuracy; macro and weighted precision, recall, and F1; FAKE-class precision/recall/F1; ROC-AUC; PR-AUC; MCC; Cohen's kappa; a labelled confusion matrix; wall-clock training time; and validation/test inference throughput. Results preserve full precision in JSON and may be rounded only for human-readable tables.

False positives and false negatives are counted across the fixed, overlapping descriptive cohorts `political`, `health`, `breaking`, `short` (<=150 characters), `long` (>=400 characters), and `ambiguous`. Topic cohorts use documented keywords, never train the model, and do not establish real-world demographic, factual, or fairness labels. Reports exclude raw text and retain only aggregate counts and local document identifiers in ignored evidence artifacts.

## Reproduction

From the repository root, use a short Windows virtual-environment path if the project path exceeds the PyTorch installer filename limit:

```powershell
$env:PYTHONPATH = (Get-Location).Path
& 'C:\tmp\truthlens-p42-venv\Scripts\python.exe' -m ml.transformer_benchmark.run_benchmark --model distilbert
```

Use one model key at a time: `indicbert`, `distilbert`, `bert_base`, or `roberta`. Do not rerun a completed candidate merely to improve a metric; use a new governed decision for any protocol change.
