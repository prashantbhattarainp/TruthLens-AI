"""Materialize TL-BFNK-EN-v1.0 without modifying the immutable raw archive."""

from __future__ import annotations

import hashlib
import html
import json
import re
import time
import unicodedata
import zlib
from collections import Counter, defaultdict
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Any
from zipfile import ZipFile

import numpy as np
import pandas as pd


_WHITESPACE = re.compile(r"\s+")
_PRIME = np.uint64(2**61 - 1)


@dataclass(frozen=True)
class FrozenDatasetMaterializer:
    """Apply the frozen cohort, mapping, duplicate, and split protocol exactly once."""

    manifest_path: Path
    output_directory: Path

    def run(self) -> dict[str, str]:
        manifest = _read_json(self.manifest_path)
        parent = manifest["parent_dataset"]
        archive = Path(parent["raw_archive"])
        if _sha256_file(archive) != parent["raw_archive_sha256"]:
            raise ValueError("Raw archive SHA-256 does not match the frozen manifest.")
        if self.output_directory.exists():
            raise FileExistsError(f"Refusing to overwrite governed derivative output: {self.output_directory}")
        self.output_directory.mkdir(parents=True)

        started = time.perf_counter()
        frame = _read_primary_sheet(archive)
        records, excluded = _select_frozen_records(frame, manifest)
        expected = manifest["statistics"]["prospective_phase_3_cohort"]
        counts = Counter(record["label"] for record in records)
        if (len(records), counts[0], counts[1]) != (
            expected["rows"], expected["real_count"], expected["fake_count"]
        ):
            raise ValueError("Cohort counts do not reconcile to the frozen manifest.")

        _assign_duplicate_clusters(records)
        _assign_partitions(records, manifest["split"])
        _validate_partition_integrity(records)

        derivative_path = self.output_directory / "derivative-documents.jsonl"
        split_path = self.output_directory / "split-documents.jsonl"
        exclusions_path = self.output_directory / "exclusions.jsonl"
        _write_jsonl(derivative_path, records)
        _write_jsonl(split_path, records)
        _write_jsonl(exclusions_path, excluded)
        split_summary = _split_summary(records)
        manifest_value: dict[str, Any] = {
            "artifact_type": "governed_dataset_derivative",
            "dataset_version": manifest["dataset_version"],
            "parent_manifest_sha256": _sha256_file(self.manifest_path),
            "raw_archive_sha256": parent["raw_archive_sha256"],
            "duplicate_policy_id": manifest["duplicate_policy"]["id"],
            "split_id": manifest["split"]["id"],
            "source_rows": int(len(frame)),
            "included_rows": len(records),
            "excluded_rows": len(excluded),
            "class_counts": {"REAL": counts[0], "FAKE": counts[1]},
            "split_summary": split_summary,
            "duration_ms": round((time.perf_counter() - started) * 1000),
            "files": {
                derivative_path.name: _sha256_file(derivative_path),
                split_path.name: _sha256_file(split_path),
                exclusions_path.name: _sha256_file(exclusions_path),
            },
        }
        manifest_output = self.output_directory / "derivative-manifest.json"
        manifest_output.write_text(json.dumps(manifest_value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return {
            "documents": str(derivative_path),
            "split_documents": str(split_path),
            "exclusions": str(exclusions_path),
            "manifest": str(manifest_output),
        }


def _read_primary_sheet(archive: Path) -> pd.DataFrame:
    with ZipFile(archive) as container:
        members = container.namelist()
        if len(members) != 1:
            raise ValueError("Frozen source archive must contain exactly one workbook.")
        workbook = container.read(members[0])
    frame = pd.read_excel(BytesIO(workbook), sheet_name="A", engine="openpyxl", dtype=object)
    required = {"id", "Statement", "News Body", "Label", "Language", "Fact_Check_Source", "Publish_Date"}
    if not required <= set(frame.columns):
        raise ValueError("Frozen source worksheet no longer has the required fields.")
    return frame


def _select_frozen_records(frame: pd.DataFrame, manifest: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    english = frame.loc[frame["Language"].eq("English")].copy()
    english["label"] = english["Label"].map(_map_label)
    if english["label"].isna().any():
        raise ValueError("Frozen cohort contains an unmapped label.")
    english["label"] = english["label"].astype(int)
    # Spreadsheet blanks are absent source text, never the literal token
    # "nan" introduced by pandas string conversion.  This preserves the
    # frozen source-text contract without imputing or cleaning content.
    english["raw_text"] = english["Statement"].map(_text_or_empty) + "\n\n" + english["News Body"].map(_text_or_empty)
    english["pair_key"] = english["raw_text"].map(lambda value: _sha256_text(value))
    label_counts = english.groupby("pair_key")["label"].nunique()
    conflict_keys = set(label_counts[label_counts > 1].index)
    excluded: list[dict[str, Any]] = []
    retained = english.loc[~english["pair_key"].isin(conflict_keys)]
    for _, row in english.loc[english["pair_key"].isin(conflict_keys)].iterrows():
        excluded.append({
            "document_id": str(row["id"]),
            "reason": "exact_statement_news_body_pair_has_conflicting_mapped_labels",
            "pair_key": row["pair_key"],
        })
    expected_conflicts = manifest["statistics"]["exact_pair_conflict_exclusion"]
    if (len(conflict_keys), len(excluded)) != (expected_conflicts["clusters"], expected_conflicts["rows"]):
        raise ValueError("Exact conflict exclusion does not reconcile to frozen manifest.")
    records = [{
        "document_id": str(row["id"]),
        "raw_text": row["raw_text"],
        "label": int(row["label"]),
        "raw_label": "True" if int(row["label"]) == 0 else "False",
        "fact_check_source": str(row["Fact_Check_Source"]),
        "publish_date_raw": _string_or_null(row["Publish_Date"]),
        "raw_text_sha256": _sha256_text(row["raw_text"]),
        "exact_pair_key": row["pair_key"],
    } for _, row in retained.iterrows()]
    return records, excluded


def _map_label(value: object) -> int | None:
    if value is True or str(value).strip().lower() in {"true", "1"}:
        return 0
    if value is False or str(value).strip().lower() in {"false", "0"}:
        return 1
    return None


def _text_or_empty(value: object) -> str:
    return "" if pd.isna(value) else str(value)


def _assign_duplicate_clusters(records: list[dict[str, Any]]) -> None:
    """Build deterministic exact/near clusters using the frozen 128-permutation MinHash protocol."""
    parent = list(range(len(records)))

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left: int, right: int) -> None:
        left_root, right_root = find(left), find(right)
        if left_root != right_root:
            parent[max(left_root, right_root)] = min(left_root, right_root)

    exact: dict[str, int] = {}
    for index, record in enumerate(records):
        previous = exact.setdefault(record["exact_pair_key"], index)
        union(index, previous)

    seeds = np.random.default_rng(42).integers(1, int(_PRIME), size=(2, 128), dtype=np.uint64)
    buckets: dict[tuple[int, tuple[int, ...]], list[int]] = defaultdict(list)
    canonical: list[str] = []
    signatures: list[np.ndarray] = []
    for index, record in enumerate(records):
        text = _canonical_duplicate_text(record["raw_text"])
        signature = _minhash_signature(text, seeds)
        candidates: set[int] = set()
        for band in range(32):
            key = (band, tuple(int(value) for value in signature[band * 4:(band + 1) * 4]))
            candidates.update(buckets[key])
        for candidate in candidates:
            if _shingle_jaccard(text, canonical[candidate]) >= 0.90:
                union(index, candidate)
        for band in range(32):
            key = (band, tuple(int(value) for value in signature[band * 4:(band + 1) * 4]))
            buckets[key].append(index)
        canonical.append(text)
        signatures.append(signature)
    members: dict[int, list[str]] = defaultdict(list)
    for index, record in enumerate(records):
        members[find(index)].append(record["document_id"])
    for index, record in enumerate(records):
        cluster_members = sorted(members[find(index)])
        record["duplicate_cluster_id"] = "DUP-" + _sha256_text("\n".join(cluster_members))[:16]


def _minhash_signature(text: str, seeds: np.ndarray) -> np.ndarray:
    shingles = _shingles(text)
    values = np.fromiter((zlib.crc32(value.encode("utf-8")) for value in shingles), dtype=np.uint64)
    if not len(values):
        values = np.array([0], dtype=np.uint64)
    # Vectorized universal hashing: deterministic 128-permutation MinHash with seed 42.
    permutations = (values[:, None] * seeds[0] + seeds[1]) % _PRIME
    return permutations.min(axis=0)


def _canonical_duplicate_text(text: str) -> str:
    return _WHITESPACE.sub(" ", html.unescape(unicodedata.normalize("NFKC", text)).casefold()).strip()


def _shingles(text: str) -> set[str]:
    if len(text) < 5:
        return {text}
    return {text[index:index + 5] for index in range(len(text) - 4)}


def _shingle_jaccard(left: str, right: str) -> float:
    left_set, right_set = _shingles(left), _shingles(right)
    return len(left_set & right_set) / len(left_set | right_set)


def _assign_partitions(records: list[dict[str, Any]], split: dict[str, Any]) -> None:
    ratios = split["ratios"]
    names = ("train", "validation", "test")
    group_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        group_rows[record["duplicate_cluster_id"]].append(record)
    assignments: dict[str, str] = {}
    strata: dict[tuple[tuple[int, int], ...], list[tuple[str, list[dict[str, Any]]]]] = defaultdict(list)
    for group_id, rows in group_rows.items():
        # A group is atomic.  Stratifying its complete class composition also
        # distributes singleton, same-label duplicate, and mixed-label
        # duplicate groups across all partitions, rather than leaving the
        # training cohort with only singleton groups.
        signature = tuple(sorted(Counter(row["label"] for row in rows).items()))
        strata[signature].append((group_id, rows))

    for groups in strata.values():
        target_rows = {name: sum(len(rows) for _, rows in groups) * ratios[name] for name in names}
        allocated_rows = Counter()
        ordered = sorted(groups, key=lambda item: _sha256_text(f"{split['random_seed']}:{item[0]}"))
        for group_id, rows in ordered:
            # Largest remaining quota is a deterministic proportional
            # allocation.  Groups inside a stratum have the same composition.
            partition = max(
                names,
                key=lambda name: (target_rows[name] - allocated_rows[name], -names.index(name)),
            )
            assignments[group_id] = partition
            allocated_rows[partition] += len(rows)
    for record in records:
        record["partition"] = assignments[record["duplicate_cluster_id"]]


def _validate_partition_integrity(records: list[dict[str, Any]]) -> None:
    seen: dict[str, str] = {}
    for record in records:
        group, partition = record["duplicate_cluster_id"], record["partition"]
        if group in seen and seen[group] != partition:
            raise ValueError("Duplicate cluster crosses partitions.")
        seen[group] = partition
    if set(record["partition"] for record in records) != {"train", "validation", "test"}:
        raise ValueError("All frozen partitions must be nonempty.")


def _split_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for partition in ("train", "validation", "test"):
        rows = [record for record in records if record["partition"] == partition]
        labels = Counter(record["label"] for record in rows)
        result[partition] = {
            "rows": len(rows),
            "real_count": labels[0],
            "fake_count": labels[1],
            "duplicate_cluster_count": len({record["duplicate_cluster_id"] for record in rows}),
            "source_counts": dict(sorted(Counter(record["fact_check_source"] for record in rows).items())),
        }
    return result


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _string_or_null(value: object) -> str | None:
    return None if pd.isna(value) else str(value)
