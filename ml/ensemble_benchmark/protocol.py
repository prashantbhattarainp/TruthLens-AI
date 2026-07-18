"""Pre-specified Phase 4.3 ensemble protocol and immutable component identities."""

from __future__ import annotations

from dataclasses import asdict, dataclass


DATASET_VERSION = "TL-BFNK-EN-v1.0"
DERIVATIVE_ID = "DER-20260718-r2"
SPLIT_ID = "SPL-TL-BFNK-EN-v1.0"
DATASET_SHA256 = "978931f41ece219a3e3e27d052cfb35dfe557af02a604d6f913d4ad8e6ca59ad"
LABEL_MAPPING = {"REAL": 0, "FAKE": 1}


BASE_MODELS = {
    "linear_svm": {
        "display_name": "LinearSVC TF-IDF",
        "optimization_id": "OPT-20260718-linear-svm-faafafe15e",
        "model_id": "MDL-TL-LSVM-TFIDF-v1.1.0-rc.1",
        "score_type": "uncalibrated_decision_margin",
    },
    "multinomial_naive_bayes": {
        "display_name": "MultinomialNB TF-IDF",
        "optimization_id": "OPT-20260718-multinomial-naive-bayes-60fad40e22",
        "model_id": "MDL-TL-MNB-TFIDF-v1.1.0-rc.1",
        "score_type": "predict_proba_fake_class",
    },
    "logistic_regression": {
        "display_name": "Logistic Regression TF-IDF",
        "optimization_id": "OPT-20260718-logistic-regression-15115d5c12",
        "model_id": "MDL-TL-LR-TFIDF-v1.1.0-rc.1",
        "score_type": "predict_proba_fake_class",
    },
}


@dataclass(frozen=True)
class EnsembleProtocol:
    """Fixed before validation metrics are observed."""

    seed: int = 42
    evaluation_partition: str = "validation only"
    protected_test_policy: str = "no prediction, feature transformation, label use, or ensemble selection"
    preprocessing: str = "frozen Phase 3.9 preprocessing package applied identically to validation text"
    hard_vote_rule: str = "FAKE when at least two of three component labels are FAKE"
    weighted_vote_rule: str = "FAKE when OOF-macro-F1-weighted component labels reach half total weight"
    weighted_vote_weights: str = "normalized Phase 3.9 train-only grouped-OOF Macro F1"
    soft_vote_rule: str = "mean FAKE probability from MultinomialNB and Logistic Regression; threshold 0.5"
    soft_vote_exclusion: str = "LinearSVC excluded because its decision margin is not a calibrated probability"
    stacking_features: str = "train-only OOF: sigmoid-clipped LinearSVC margin, MultinomialNB FAKE probability, Logistic Regression FAKE probability"
    stacking_estimator: str = "LogisticRegression(C=1.0, solver=lbfgs, max_iter=1000, random_state=42)"
    blending_status: str = "excluded; no independent blend-development partition exists without changing the frozen protocol"
    transformer_hybrid_status: str = "excluded; Phase 4.2 produced no transformer prediction artifact"
    champion_policy: str = "no automatic promotion; validation evidence is research-only"


def protocol_dict() -> dict[str, object]:
    return {
        "dataset_version": DATASET_VERSION,
        "derivative_id": DERIVATIVE_ID,
        "dataset_sha256": DATASET_SHA256,
        "split_id": SPLIT_ID,
        "label_mapping": LABEL_MAPPING,
        "components": BASE_MODELS,
        "ensemble": asdict(EnsembleProtocol()),
    }
