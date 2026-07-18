"""Verify the tracked Phase 4.6 publication package without reading governed data."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PUBLICATION = ROOT / "docs" / "research" / "publication"
REQUIRED_FILES = (
    "FINAL_RESULTS_TABLES.md",
    "FINAL_COMPARISON_TABLES.md",
    "FINAL_FIGURES_INDEX.md",
    "FINAL_EXPERIMENT_SUMMARY.md",
    "RESEARCH_CONTRIBUTIONS.md",
    "THREATS_TO_VALIDITY.md",
    "REPRODUCIBILITY_GUIDE.md",
    "FUTURE_WORK.md",
    "PUBLICATION_CHECKLIST.md",
    "README.md",
)
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


def check(condition: bool, message: str, failures: list[str]) -> None:
    if condition:
        print(f"PASS: {message}")
    else:
        failures.append(message)
        print(f"FAIL: {message}")


def local_markdown_links() -> list[tuple[Path, str]]:
    missing: list[tuple[Path, str]] = []
    excluded_parts = {".git", ".venv", "node_modules"}
    for source in ROOT.rglob("*.md"):
        if any(part in excluded_parts for part in source.parts):
            continue
        for raw_target in MARKDOWN_LINK.findall(source.read_text(encoding="utf-8")):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if not target or target.startswith(("#", "mailto:")) or "://" in target:
                continue
            target = target.split("#", 1)[0]
            if target and not (source.parent / target).resolve().exists():
                missing.append((source.relative_to(ROOT), target))
    return missing


def main() -> int:
    failures: list[str] = []
    for filename in REQUIRED_FILES:
        check((PUBLICATION / filename).is_file(), f"publication file {filename}", failures)

    check((ROOT / "docs" / "research" / "PROJECT_RESEARCH_SUMMARY.md").is_file(), "project research summary", failures)
    check((ROOT / "docs" / "PHASE4_SUMMARY.md").is_file(), "Phase 4 summary", failures)
    check(
        (ROOT / "research" / "decision-log" / "RDL-017-Research-Finalization-and-Publication-Boundary.md").is_file(),
        "RDL-017 finalization record",
        failures,
    )
    check(
        (ROOT / "docs" / "engineering-journal" / "EJ-025-Research-Finalization-and-Publication-Package.md").is_file(),
        "EJ-025 finalization journal",
        failures,
    )

    registry = json.loads((ROOT / "ml" / "metadata" / "model-registry.json").read_text(encoding="utf-8"))
    current_model = registry.get("current_model", {})
    finalization = registry.get("phase_4_finalization", {})
    check(registry.get("schema_version") == "1.4.0", "registry schema version 1.4.0", failures)
    check(
        registry.get("status") == "phase_4_complete_publication_package_validation_only",
        "registry Phase 4 completion status",
        failures,
    )
    check(current_model.get("model_id") == "MDL-TL-LSVM-TFIDF-v1.1.0-rc.1", "champion model identity", failures)
    check(current_model.get("production_model") is False, "champion remains non-production", failures)
    check(
        finalization.get("experiment_id") == "P46-research-finalization-20260718",
        "publication finalization experiment identity",
        failures,
    )

    figure_manifest = json.loads(
        (ROOT / "docs" / "research" / "PHASE_4_5_ARTIFACT_MANIFEST.json").read_text(encoding="utf-8")
    )
    for figure in figure_manifest["figures"]:
        figure_path = ROOT / figure["path"]
        digest = hashlib.sha256(figure_path.read_bytes()).hexdigest() if figure_path.is_file() else ""
        check(digest == figure["sha256"], f"figure hash {figure['path']}", failures)

    missing_links = local_markdown_links()
    check(not missing_links, "all tracked Markdown links resolve", failures)
    for source, target in missing_links:
        print(f"  missing: {source.as_posix()} -> {target}")

    if failures:
        print(f"\n{len(failures)} verification failure(s).")
        return 1
    print("\nPhase 4 publication verification passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
