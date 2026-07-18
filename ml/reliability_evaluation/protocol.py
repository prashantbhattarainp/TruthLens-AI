"""Immutable Phase 4.5 reliability-assessment protocol."""

from __future__ import annotations

from dataclasses import asdict, dataclass


DATASET_VERSION = "TL-BFNK-EN-v1.0"
DERIVATIVE_ID = "DER-20260718-r2"
SPLIT_ID = "SPL-TL-BFNK-EN-v1.0"
DATASET_SHA256 = "978931f41ece219a3e3e27d052cfb35dfe557af02a604d6f913d4ad8e6ca59ad"
CHAMPION_MODEL_ID = "MDL-TL-LSVM-TFIDF-v1.1.0-rc.1"


@dataclass(frozen=True)
class ReliabilityProtocol:
    """Pre-specified controls for descriptive Phase 4.5 research evidence."""

    evaluation_partition: str = "validation only"
    protected_test_policy: str = "no prediction, feature transformation, label use, or selection"
    model_policy: str = "immutable packaged LinearSVC; no retraining, calibration fit, threshold change, promotion, or service integration"
    preprocessing_policy: str = "reuse the packaged frozen preprocessing for baseline and every perturbed input"
    perturbation_policy: str = "deterministic text stressors; label preservation is assumed only for mechanical transformations and never used for selection"
    calibration_policy: str = (
        "diagnostic sigmoid of uncalibrated decision margin only; no fitted calibrator, probability, confidence, or API output"
    )
    fairness_policy: str = "descriptive source/topic/language/length slices only; no demographic or causal fairness claim"
    xai_policy: str = "linear contribution overlap is an analysis proxy; SHAP/LIME remain post-prediction and are not classifier components"
    transformer_policy: str = "comparison unavailable; Phase 4.2 produced no completed transformer checkpoint or prediction artifact"
    artifact_policy: str = "ignored aggregate artifacts and tracked aggregate figures only; no raw text, document identifiers, predictions, or scores"


def protocol_dict() -> dict[str, object]:
    """Return serialisable protocol evidence for a local run manifest."""

    return {
        "dataset_version": DATASET_VERSION,
        "derivative_id": DERIVATIVE_ID,
        "dataset_sha256": DATASET_SHA256,
        "split_id": SPLIT_ID,
        "champion_model_id": CHAMPION_MODEL_ID,
        "reliability_assessment": asdict(ReliabilityProtocol()),
    }
