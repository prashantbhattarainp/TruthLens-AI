# Label Mapping Policy

**Scope:** Binary-target planning policy
**Status:** Operational convention approved; `LMAP-BFNK-v1.0` is frozen for `TL-BFNK-EN-v1.0`
**Related decision record:** [RDL-001](../../research/decision-log/RDL-001-Research-Methodology-and-Reproducibility.md)

## Purpose

This policy prevents incompatible source labels from being silently collapsed into a binary target. It separates the source's original label from TruthLens AI's approved research target and makes the positive class explicit in every report.

## Binary target convention

| Canonical label | Numeric value | Role | Meaning |
| --- | --- | --- | --- |
| FAKE | 1 | Positive class | Content/claim that the approved source-label policy maps to the misinformation target. |
| REAL | 0 | Negative class | Content/claim that the approved source-label policy maps to the verified/non-misinformation target. |

FAKE is the positive class for binary metrics, threshold reporting, confusion-matrix labelling, and calibration records. The user-facing API's title-case labels remain a presentation concern and must not replace the canonical research labels in an experiment record.

## Frozen BharatFakeNewsKosh v1 mapping

`LMAP-BFNK-v1.0` applies only to the immutable DSR-001 archive identified by `TL-BFNK-EN-v1.0`. The source Kaggle data card and source publication define the labels as legitimate/true and fraudulent/false. The acquired archive contains only raw `True` and `False` values, which map as follows:

| Raw value | Canonical outcome | Inclusion |
| --- | --- | --- |
| `True` | REAL = 0 | Included when the cohort and duplicate rules pass. |
| `False` | FAKE = 1 | Included when the cohort and duplicate rules pass. |
| `Partially True`, ambiguous, missing, or changed value | No binary outcome | Excluded; requires a new source-specific mapping/version decision. |

The mapping is anchored to the archive hash and does not silently reconcile the landing-page count discrepancy. See [Dataset Governance](DATASET_GOVERNANCE.md) and [Dataset Manifest](DATASET_MANIFEST.md) for the release-specific evidence and boundaries.

## Mapping prerequisites

No source label is mapped until the candidate's dataset card documents:

- the original label values and their creator-defined meanings;
- the fact-checking, verification, annotation, or correction process that produced them;
- the unit to which the label applies, such as a claim, headline, article, or source;
- the treatment of revisions, disputed assessments, and missing labels; and
- any known source-level, temporal, topical, or language bias.

The mapping table must preserve raw labels exactly and cite the source definition. One source-release/version receives one versioned mapping rule; a changed label definition creates a new mapping version.

## Mandatory treatment of non-binary or ambiguous labels

| Source condition | Required treatment in the initial binary study |
| --- | --- |
| Clearly documented misinformation/false/fabricated equivalent | Eligible for reviewed mapping to FAKE. |
| Clearly documented verified/true/correct equivalent | Eligible for reviewed mapping to REAL. |
| Partly false, mixed, misleading, missing context, or unverified | Hold for policy review; exclude unless a pre-approved rule establishes semantic equivalence. |
| Satire, parody, opinion, commentary, or non-claim content | Exclude from the initial target unless a separate study defines a justified treatment. |
| Disputed, corrected, or changed verdict | Preserve history; use the approved versioned verdict or exclude with reason. |
| Source-level label with no item-level evidence | Do not map as an item-level truth label by default. |
| Missing or undocumented label | Mark unresolved and exclude from training and evaluation. |

## Mapping approval and audit record

For every raw label, the future mapping register must contain the dataset/source release, raw label, canonical outcome, rationale, evidence citation, reviewer, review date, mapping-policy version, and inclusion/exclusion decision. Manual exceptions require a written rule and cannot be based on model output.

The mapping is frozen before any split is generated. Changing it creates a new data derivative and invalidates direct comparison with experiments that used the prior mapping.

## Reporting requirements

Every experiment and model report states the positive class as FAKE, gives support for both classes, and reports excluded/unresolved counts. Results must never use the label names to imply that TruthLens AI independently fact-checked an item.
