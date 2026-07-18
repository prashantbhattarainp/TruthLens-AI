# Reproducibility Guide

**Scope:** Phase 3.7 baseline experimentation framework  
**Status:** Implementation guidance; no research experiment has been executed.

## Required lineage before a real run

A data-bearing experiment requires an approved dataset derivative, dataset/derivative SHA-256 checksum, label-mapping version, duplicate/group rule, frozen split manifest, preprocessing record/configuration hash, feature configuration hash, source-manifest checksum, and a declared training partition. RDL-008 now freezes these rules for `TL-BFNK-EN-v1.0`; the derivative and split manifest have deliberately not yet been materialized.

## Freeze and record

- Use one immutable experiment configuration from `ml/config/experiments/` and one immutable feature configuration from `ml/config/features/`.
- Record the canonical SHA-256 hashes, model version, all hyperparameters, framework version, Python/dependency environment, code revision, operating environment, and source-manifest hash.
- Set and record the configured random seed before creating folds. The framework seeds Python and NumPy, seeds shuffled CV, and derives a deterministic model seed per fold.
- Fit the vectorizer inside each CV training fold only. Persist each fold's vectorizer/model pair and never refit it on held-out validation/test rows.
- Retain failed or invalidated records; do not overwrite an existing experiment directory or reuse its ID.

## Runtime evidence

The local implementation verification environment used scikit-learn `1.9.0`, SciPy `1.18.0`, joblib `1.5.3`, Pillow `11.3.0`, and the existing project virtual environment. A real run must record its actual installed versions rather than inheriting these values by assumption.

## Re-run contract

From the repository root, ensure `ml/src` is on the Python module path (or install the package equivalently), then supply an approved labelled preprocessed training partition and canonical output root:

```text
python -m experiments.cli --experiment-config <model-config.json> --feature-config <feature-config.json> --training-jsonl <approved-training-partition.jsonl> --source-manifest <approved-manifest.json> --dataset-version <version> --dataset-hash <approved-sha256> --split-id <SPL-id> --preprocessing-version <version> --preprocessing-configuration-sha256 <hash> --notes <rationale> --output-root ml/data/experiments/<dataset-version>
```

The CLI creates a new unique experiment directory. It rejects raw input paths and output roots outside `ml/data/experiments/`. The resulting `manifest.json` must verify the checksums of every retained record, fold model/feature extractor, combined configuration, metrics, reports, prediction file, notes, local-registry sidecar, and log.

## Interpretation boundary

Reproducing a metric verifies a bounded implementation result only. It does not validate source labels, establish factual truth, prove fairness, permit deployment, or extend the result beyond the approved corpus, language, source, time, and text-unit scope.
