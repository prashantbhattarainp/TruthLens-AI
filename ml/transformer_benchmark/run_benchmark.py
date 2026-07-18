"""Run one governed Phase 4.2 transformer candidate.

Usage (from repository root)::

    .\\ml-service\\.venv\\Scripts\\python.exe -m ml.transformer_benchmark.run_benchmark --model indicbert

Each invocation creates a timestamped, ignored evidence bundle. It cannot
alter the existing service model and refuses a test evaluation until validation
checkpoint selection has completed in that invocation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import random
import sys
import time
from datetime import UTC, datetime
from importlib import metadata
from pathlib import Path
from typing import Any

import numpy as np

from .metrics import classification_metrics, error_slice_summary
from .protocol import DATASET_SHA256, MODELS, TrainingProtocol, protocol_dict


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATASET = REPOSITORY_ROOT / "ml/data/derived/TL-BFNK-EN-v1.0/DER-20260718-r2/split-documents.jsonl"
DEFAULT_OUTPUT_ROOT = REPOSITORY_ROOT / "ml/data/transformer-benchmarks"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_frozen_split(path: Path) -> dict[str, list[dict[str, Any]]]:
    actual_hash = _sha256(path)
    if actual_hash != DATASET_SHA256:
        raise ValueError(f"Frozen derivative hash mismatch: expected {DATASET_SHA256}, got {actual_hash}")
    partitions = {"train": [], "validation": [], "test": []}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            partition = row.get("partition")
            if partition not in partitions:
                raise ValueError(f"Unexpected partition {partition!r}")
            label = row.get("label")
            if label not in (0, 1):
                raise ValueError(f"Unexpected binary label {label!r}")
            partitions[partition].append(row)
    expected = {"train": 6813, "validation": 1461, "test": 1458}
    found = {name: len(rows) for name, rows in partitions.items()}
    if found != expected:
        raise ValueError(f"Frozen split cardinality mismatch: expected {expected}, got {found}")
    return partitions


def _set_seed(seed: int, torch: Any) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


def _environment(torch: Any, transformers: Any, device: Any) -> dict[str, Any]:
    packages = ("torch", "transformers", "accelerate", "safetensors", "numpy", "scikit-learn")
    versions: dict[str, str] = {}
    for package in packages:
        try:
            versions[package] = metadata.version(package)
        except metadata.PackageNotFoundError:
            versions[package] = "not_installed"
    return {
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "processor": platform.processor() or "unavailable",
        "package_versions": versions,
        "device": str(device),
        "cuda_available": bool(torch.cuda.is_available()),
        "cuda_device_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "torch_threads": torch.get_num_threads(),
        "transformers_version": transformers.__version__,
    }


class _TokenizedDataset:
    def __init__(self, rows: list[dict[str, Any]], tokenizer: Any, max_length: int) -> None:
        self.rows = rows
        self.encodings = tokenizer(
            [str(row["raw_text"]) for row in rows],
            truncation=True,
            max_length=max_length,
            padding="max_length",
            return_tensors="pt",
        )

    def __len__(self) -> int:
        return len(self.rows)

    def __getitem__(self, index: int) -> dict[str, Any]:
        item = {key: value[index] for key, value in self.encodings.items()}
        item["labels"] = int(self.rows[index]["label"])
        return item


def _evaluate(model: Any, dataloader: Any, device: Any, torch: Any) -> tuple[dict, list[float], list[int]]:
    model.eval()
    labels: list[int] = []
    predictions: list[int] = []
    scores: list[float] = []
    start = time.perf_counter()
    with torch.inference_mode():
        for batch in dataloader:
            labels.extend(batch.pop("labels").tolist())
            inputs = {key: value.to(device) for key, value in batch.items()}
            logits = model(**inputs).logits
            probabilities = torch.softmax(logits, dim=1)[:, 1]
            scores.extend(probabilities.detach().cpu().tolist())
            predictions.extend(torch.argmax(logits, dim=1).detach().cpu().tolist())
    elapsed_seconds = time.perf_counter() - start
    result = classification_metrics(labels, predictions, scores)
    result["inference_seconds"] = elapsed_seconds
    result["inference_examples_per_second"] = len(labels) / elapsed_seconds if elapsed_seconds else None
    return result, scores, predictions


def _write_json(path: Path, content: dict[str, Any]) -> None:
    path.write_text(json.dumps(content, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _checkpoint_hashes(checkpoint: Path) -> dict[str, str]:
    return {
        str(path.relative_to(checkpoint)): _sha256(path)
        for path in sorted(checkpoint.rglob("*"))
        if path.is_file()
    }


def _report_failure(output_dir: Path, args: argparse.Namespace, exception: Exception) -> None:
    _write_json(
        output_dir / "run-manifest.json",
        {
            "schema_version": "1.0.0",
            "status": "not_evaluated",
            "model_key": args.model,
            "model": MODELS[args.model],
            "protocol": protocol_dict(),
            "failure": {"type": type(exception).__name__, "message": str(exception)},
            "governance": {
                "protected_test_access": "none; candidate setup/training did not complete",
                "promotion_decision": "none",
                "reason": "resource, access, or reproducibility prerequisite did not complete",
            },
        },
    )


def run(args: argparse.Namespace) -> Path:
    """Fine-tune a fixed candidate, select on validation, then evaluate test once."""

    protocol = TrainingProtocol()
    run_stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    output_dir = Path(args.output_root) / f"P42-{args.model}-{run_stamp}"
    output_dir.mkdir(parents=True, exist_ok=False)
    try:
        import torch
        import transformers
        from torch.optim import AdamW
        from torch.utils.data import DataLoader
        from transformers import AutoModelForSequenceClassification, AutoTokenizer, get_linear_schedule_with_warmup

        _set_seed(protocol.seed, torch)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        frozen = _read_frozen_split(Path(args.dataset))
        model_info = MODELS[args.model]
        tokenizer = AutoTokenizer.from_pretrained(model_info["model_id"])
        model = AutoModelForSequenceClassification.from_pretrained(
            model_info["model_id"],
            num_labels=2,
            id2label={0: "REAL", 1: "FAKE"},
            label2id={"REAL": 0, "FAKE": 1},
            ignore_mismatched_sizes=True,
        ).to(device)
        resolved_revision = getattr(model.config, "_commit_hash", None)
        datasets = {
            name: _TokenizedDataset(rows, tokenizer, protocol.max_sequence_length)
            for name, rows in frozen.items()
        }
        generator = torch.Generator().manual_seed(protocol.seed)
        train_loader = DataLoader(
            datasets["train"], batch_size=protocol.train_batch_size, shuffle=True, generator=generator
        )
        evaluation_loaders = {
            name: DataLoader(dataset, batch_size=protocol.eval_batch_size, shuffle=False)
            for name, dataset in datasets.items()
            if name != "train"
        }
        optimizer = AdamW(
            model.parameters(),
            lr=protocol.learning_rate,
            betas=(protocol.adam_beta1, protocol.adam_beta2),
            eps=protocol.adam_epsilon,
            weight_decay=protocol.weight_decay,
        )
        total_steps = len(train_loader) * protocol.epochs
        scheduler = get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=round(total_steps * protocol.warmup_ratio),
            num_training_steps=total_steps,
        )
        training_start = time.perf_counter()
        epochs: list[dict[str, Any]] = []
        best_state: dict[str, Any] | None = None
        best_validation_macro_f1 = float("-inf")
        for epoch_index in range(1, protocol.epochs + 1):
            model.train()
            epoch_loss = 0.0
            optimizer.zero_grad(set_to_none=True)
            for step, batch in enumerate(train_loader, start=1):
                labels = batch.pop("labels").to(device)
                inputs = {key: value.to(device) for key, value in batch.items()}
                loss = model(**inputs, labels=labels).loss / protocol.gradient_accumulation_steps
                loss.backward()
                if step % protocol.gradient_accumulation_steps == 0 or step == len(train_loader):
                    torch.nn.utils.clip_grad_norm_(model.parameters(), protocol.max_grad_norm)
                    optimizer.step()
                    scheduler.step()
                    optimizer.zero_grad(set_to_none=True)
                epoch_loss += float(loss.detach().cpu()) * protocol.gradient_accumulation_steps
            validation_metrics, _, _ = _evaluate(model, evaluation_loaders["validation"], device, torch)
            epochs.append(
                {
                    "epoch": epoch_index,
                    "mean_training_loss": epoch_loss / len(train_loader),
                    "validation": validation_metrics,
                }
            )
            if validation_metrics["macro_f1"] > best_validation_macro_f1:
                best_validation_macro_f1 = validation_metrics["macro_f1"]
                best_state = {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}
        if best_state is None:
            raise RuntimeError("No validation checkpoint was selected")
        model.load_state_dict(best_state)
        training_seconds = time.perf_counter() - training_start
        selected_checkpoint = output_dir / "selected-checkpoint"
        model.save_pretrained(selected_checkpoint, safe_serialization=True)
        tokenizer.save_pretrained(selected_checkpoint)
        final_validation, _, _ = _evaluate(model, evaluation_loaders["validation"], device, torch)
        test_metrics, test_scores, test_predictions = _evaluate(model, evaluation_loaders["test"], device, torch)
        test_rows = [
            {
                "document_id": row["document_id"],
                "label": row["label"],
                "prediction": prediction,
                "score_fake": score,
                "raw_text": row["raw_text"],
            }
            for row, prediction, score in zip(frozen["test"], test_predictions, test_scores, strict=True)
        ]
        errors = error_slice_summary(test_rows)
        del test_rows
        _write_json(
            output_dir / "results.json",
            {
                "validation": final_validation,
                "protected_test": test_metrics,
                "epochs": epochs,
                "training_seconds": training_seconds,
                "training_examples_per_second": len(frozen["train"]) / training_seconds if training_seconds else None,
                "error_analysis": errors,
                "sample_score_storage": "none; raw text and per-document scores are not persisted",
            },
        )
        _write_json(
            output_dir / "run-manifest.json",
            {
                "schema_version": "1.0.0",
                "status": "evaluated_research_only",
                "model_key": args.model,
                "model": {**model_info, "resolved_revision": resolved_revision},
                "protocol": protocol_dict(),
                "data": {
                    "path": str(Path(args.dataset).resolve()),
                    "sha256": _sha256(Path(args.dataset)),
                    "partition_counts": {name: len(rows) for name, rows in frozen.items()},
                },
                "environment": _environment(torch, transformers, device),
                "selected_checkpoint": {
                    "path": str(selected_checkpoint.resolve()),
                    "files_sha256": _checkpoint_hashes(selected_checkpoint),
                },
                "governance": {
                    "validation_selection": "The selected checkpoint maximized validation macro_f1 within the fixed one-epoch schedule.",
                    "protected_test_access": "one final non-selection evaluation after selection",
                    "champion_replacement": "prohibited automatically; separate review and safety gates required",
                    "production_deployment": "prohibited by this benchmark",
                },
            },
        )
        return output_dir
    except Exception as exception:
        _report_failure(output_dir, args, exception)
        raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", choices=sorted(MODELS), required=True)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    return parser.parse_args()


if __name__ == "__main__":
    parsed = parse_args()
    try:
        artifact = run(parsed)
    except Exception as failure:
        print(f"Benchmark did not complete: {type(failure).__name__}: {failure}", file=sys.stderr)
        raise SystemExit(1) from failure
    print(f"Benchmark completed: {artifact}")
