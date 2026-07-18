"""Fixed Phase 4.4 multilingual-assessment protocol.

The protocol permits descriptive validation slices from the existing English
derivative and a synthetic language-processing probe.  Neither is sufficient
to establish Hindi or Hinglish fake-news classification performance.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass


DATASET_VERSION = "TL-BFNK-EN-v1.0"
DERIVATIVE_ID = "DER-20260718-r2"
SPLIT_ID = "SPL-TL-BFNK-EN-v1.0"
DATASET_SHA256 = "978931f41ece219a3e3e27d052cfb35dfe557af02a604d6f913d4ad8e6ca59ad"
CHAMPION_MODEL_ID = "MDL-TL-LSVM-TFIDF-v1.1.0-rc.1"


@dataclass(frozen=True)
class MultilingualProtocol:
    """Controls that prevent this research audit from becoming model selection."""

    evaluation_partition: str = "validation only"
    protected_test_policy: str = "no prediction, feature transformation, label use, or selection"
    source_derivative_policy: str = (
        "reuse only as an exploratory language-appearance slice; it remains an English BFNK-derived dataset"
    )
    language_detection: str = "conservative Unicode-script plus Roman-Hindi marker heuristic"
    synthetic_probe_policy: str = (
        "manually authored, language-labelled preprocessing fixture; no REAL/FAKE labels, training, or model metric"
    )
    champion_policy: str = "no retraining, calibration, threshold change, promotion, service integration, or deployment claim"
    transformer_policy: str = "IndicBERT remains not evaluated because the Phase 4.2 upstream access limitation is unchanged"
    artifact_policy: str = "local ignored aggregates only; no raw text, per-document predictions, or scores"


def protocol_dict() -> dict[str, object]:
    """Return the serialisable protocol recorded by each local run manifest."""

    return {
        "dataset_version": DATASET_VERSION,
        "derivative_id": DERIVATIVE_ID,
        "dataset_sha256": DATASET_SHA256,
        "split_id": SPLIT_ID,
        "champion_model_id": CHAMPION_MODEL_ID,
        "multilingual_assessment": asdict(MultilingualProtocol()),
    }
