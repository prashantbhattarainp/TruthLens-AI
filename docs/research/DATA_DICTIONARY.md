# Unified Data Dictionary

**Scope:** Implementation-neutral canonical schema design
**Status:** Draft planning specification; no table, file, or database schema is created
**Related documents:** [Data provenance](DATA_PROVENANCE.md), [Label mapping](LABEL_MAPPING.md)

## Purpose and design principles

The unified schema supports candidate evaluation, data audits, reproducible derivatives, and leakage-safe experimentation across approved sources. It preserves raw source meaning separately from research annotations and model-ready fields. All values must retain their origin and missingness state; absent metadata is not invented.

The fields below define a target data contract for a future data-governance milestone. They do not prescribe storage technology or authorise implementation.

## Core identity and provenance fields

| Field | Type | Requirement | Definition and validation rule |
| --- | --- | --- | --- |
| record_id | string | Required | Immutable internal row identifier, unique within a dataset release. |
| dataset_id | string | Required | Immutable dataset-release identifier from the provenance protocol. |
| source_record_id | string | Required when supplied | Source-system row/item ID; never treated as a model feature. |
| source_dataset_name | string | Required | Creator-provided source dataset name. |
| source_release | string | Required | Exact source version, date, or immutable snapshot reference. |
| acquisition_id | string | Required | Links to a permitted acquisition event. |
| raw_content_hash | string | Required where content is retained | SHA-256 digest of the permitted raw text representation. |
| parent_record_id | string | Optional | Original record from which a derivative was created; must resolve within its parent dataset. |
| provenance_status | enum | Required | Documented, partial, or unresolved; unresolved records cannot enter an approved experiment. |

## Content and contextual fields

| Field | Type | Requirement | Definition and validation rule |
| --- | --- | --- | --- |
| headline_raw | string | Conditional | Permitted original headline; required if the task includes headlines. |
| article_raw | string | Conditional | Permitted original article/body text; required if the selected task requires article text. |
| text_unit | enum | Required | headline, article, claim, excerpt, or another approved unit; task fit must be explicit. |
| canonical_url | URI/string | Optional | Canonical content identity after documented canonicalisation; never a model feature. |
| source_url | URI/string | Optional | Original permitted URL; stored only where terms permit. |
| publisher_or_source | string | Optional | Publisher, fact-check organisation, platform, or documented source; never a default model feature. |
| publication_at | ISO 8601 date/time | Optional | Original publication time with timezone or precision stated. |
| collected_at | ISO 8601 date/time | Required | Data-collection or source-release time. |
| language | BCP 47 tag/string | Required where detectable | Source-provided or documented detection result; method and confidence recorded if inferred. |
| script | string | Optional | Script or script mix when relevant to multilingual analysis. |
| topic | string | Optional | Source-provided or documented annotation; unknown remains unknown. |
| region | string | Optional | Documented geographic context; do not infer from publisher identity alone. |

## Label and review fields

| Field | Type | Requirement | Definition and validation rule |
| --- | --- | --- | --- |
| raw_label | string | Required | Verbatim source label before any mapping. |
| label_definition_ref | string | Required | Citation or snapshot of the source-label definition. |
| binary_label | enum/integer | Conditional | FAKE = 1 or REAL = 0 only after the mapping is approved; otherwise null/pending. |
| label_status | enum | Required | mapped, pending_review, excluded, or unresolved. |
| label_provenance | string | Required | Fact-check, annotation, correction, verification, or other documented source process. |
| label_reviewed_at | ISO 8601 date/time | Optional | Review timestamp; required for any manual decision. |
| label_review_rule | string | Conditional | Versioned mapping or manual-review rule used. |
| uncertainty_reason | string | Conditional | Required when the record is not cleanly mapped or is excluded. |

## Integrity and split-control fields

| Field | Type | Requirement | Definition and validation rule |
| --- | --- | --- | --- |
| duplicate_cluster_id | string | Required after audit | Exact/near-duplicate cluster identifier; singleton clusters are allowed. |
| duplicate_method_version | string | Required after audit | Documented method/configuration that generated the cluster. |
| group_id | string | Required before splitting | Leakage-control group based on approved URL/source/family/cluster rules. |
| split_id | string | Required after splitting | Immutable split-manifest identifier. |
| partition | enum | Required after splitting | train, validation, test, or excluded; must agree with split manifest. |
| inclusion_status | enum | Required | included, excluded, or review_required. |
| exclusion_reason | string | Conditional | Required for any non-included record. |

## Missing-value policy and quality rules

Required fields cannot be blank after permitted normalisation. Optional metadata remains null or explicitly unknown; it is never guessed from text or another field. A record is excluded from a specific task only when the required text unit, provenance, or approved mapped label is missing. The exclusion is recorded and does not delete the raw-source record from the manifest.

Before a version is used in an experiment, validation must confirm:

1. unique record IDs and resolvable dataset/provenance IDs;
2. permitted text exists for the declared task and no task field is silently substituted;
3. raw labels and label-definition references are present;
4. binary labels are in the approved mapping and no pending/unresolved label enters training or evaluation;
5. timestamps, language, URLs, and source fields preserve their stated precision or missingness;
6. duplicate cluster and group assignments exist and do not cross the frozen partitions; and
7. record, class, inclusion, and exclusion counts reconcile to the manifest.
