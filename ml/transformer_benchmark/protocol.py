"""The pre-specified Phase 4.2 transformer benchmark protocol.

This module deliberately contains no model-selection logic. The validation
partition chooses a checkpoint within a fixed schedule; the test partition is
evaluated once after that selection and never determines promotion.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass


DATASET_VERSION = "TL-BFNK-EN-v1.0"
DERIVATIVE_ID = "DER-20260718-r2"
SPLIT_ID = "SPL-TL-BFNK-EN-v1.0"
DATASET_SHA256 = "978931f41ece219a3e3e27d052cfb35dfe557af02a604d6f913d4ad8e6ca59ad"
LABEL_MAPPING = {"REAL": 0, "FAKE": 1}


@dataclass(frozen=True)
class TrainingProtocol:
    """Fixed before any candidate result is inspected."""

    seed: int = 42
    max_sequence_length: int = 192
    train_batch_size: int = 8
    eval_batch_size: int = 16
    gradient_accumulation_steps: int = 1
    epochs: int = 1
    learning_rate: float = 2e-5
    adam_beta1: float = 0.9
    adam_beta2: float = 0.999
    adam_epsilon: float = 1e-8
    weight_decay: float = 0.01
    warmup_ratio: float = 0.1
    max_grad_norm: float = 1.0
    class_imbalance_treatment: str = "none; observed 60.7/39.3 class mix retained"
    scheduler: str = "linear_warmup_then_decay"
    precision: str = "float32"
    device_policy: str = "cuda when available, otherwise cpu"
    checkpoint_selection: str = "highest validation macro_f1 after each fixed epoch"
    protected_test_policy: str = "one final non-selection evaluation after checkpoint selection"


MODELS = {
    "indicbert": {
        "model_id": "ai4bharat/indic-bert",
        "display_name": "IndicBERT",
        "architecture": "ALBERT multilingual (12 Indic languages including English)",
        "license": "MIT",
    },
    "distilbert": {
        "model_id": "distilbert/distilbert-base-uncased",
        "display_name": "DistilBERT base uncased",
        "architecture": "Distilled English BERT encoder",
        "license": "Apache-2.0",
    },
    "bert_base": {
        "model_id": "google-bert/bert-base-uncased",
        "display_name": "BERT base uncased",
        "architecture": "English BERT base encoder",
        "license": "Apache-2.0",
    },
    "roberta": {
        "model_id": "FacebookAI/roberta-base",
        "display_name": "RoBERTa base",
        "architecture": "English RoBERTa base encoder",
        "license": "MIT",
    },
}


def protocol_dict() -> dict[str, object]:
    """Return JSON-safe immutable protocol evidence."""

    return {
        "dataset_version": DATASET_VERSION,
        "derivative_id": DERIVATIVE_ID,
        "dataset_sha256": DATASET_SHA256,
        "split_id": SPLIT_ID,
        "label_mapping": LABEL_MAPPING,
        "input_policy": (
            "raw_text from the frozen derivative; transformer-native tokenizer; "
            "no label, split, source, or text normalization mutation"
        ),
        "training": asdict(TrainingProtocol()),
    }
