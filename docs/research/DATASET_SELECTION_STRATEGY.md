# Dataset Selection Strategy

**Scope:** Phase 3.1 planning specification
**Status:** No candidate evaluated or selected
**Related documents:** [Research methodology](RESEARCH_METHODOLOGY.md), [Dataset registry](DATASET_REGISTRY.md), [Data provenance](DATA_PROVENANCE.md)

## Purpose

This document defines how a future dataset candidate will be reviewed. It does not identify a preferred dataset, authorise acquisition, or create a dataset record.

## Candidate lifecycle

1. Record a candidate as Proposed in the dataset registry with only publicly available descriptive information.
2. Perform independent methodological, legal, ethical, and technical reviews.
3. Record evidence, unresolved risks, and the review outcome in the registry.
4. Mark the candidate Approved only when every mandatory gate passes.
5. Obtain or access data only after approval; create the immutable manifest before any transformation.

Rejected, deferred, and withdrawn candidates remain recorded with the reason so that the selection process is auditable.

## Mandatory approval gates

| Gate | Evidence required | Fail condition |
| --- | --- | --- |
| Indian digital-media relevance | Documented Indian publisher, fact-check, public-information, or sampling relationship. | Relevance cannot be demonstrated. |
| Label provenance | Source-label definitions, verification or annotation method, reviewer/process information, and uncertainty treatment. | Labels are undocumented or are inferred only from a source identity. |
| Legal and licence review | Dataset licence, creator attribution, derivative/redistribution rights, and relevant publisher/platform terms. | Intended research use, retention, or access conflicts with terms. |
| Copyright and privacy review | Full-text rights, personal-data considerations, sensitive-content risks, and retention restrictions. | Content handling would be unlawful, unsafe, or undocumented. |
| Text and metadata suitability | Intended text unit plus enough metadata to audit source, time, language, and provenance. | Text/task alignment or metadata is materially insufficient. |
| Coverage and independence | Class counts, source/publisher diversity, language distribution, time range, topic coverage, and duplicate risk. | Corpus cannot support leakage-controlled evaluation. |
| Reproducibility | Stable source location or acquisition method, release/version information, and ability to record a manifest. | A future researcher could not identify the exact source release. |

A candidate may not compensate for a failed mandatory gate with a high score elsewhere.

## Comparative evaluation criteria

Candidates that pass all gates are compared transparently using the following evidence categories. The review records a narrative judgement and supporting links or snapshots; it does not use a score as a substitute for expert review.

| Criterion | Questions to answer |
| --- | --- |
| Task fit | Does the available text unit support the declared headline, article, claim, excerpt, or approved combination task? |
| Indian context | What makes the sample Indian digital media, and which Indian regions, publishers, languages, or platforms are absent? |
| Label integrity | Are labels item-level? Can raw labels, adjudication, corrections, and ambiguity be preserved? |
| Metadata quality | Are canonical URL, publisher, dates, language, topic, and source-record identifiers available or explicitly missing? |
| Independence | What duplicates, syndicated copies, translated copies, claims, sources, and collection events could create correlated records? |
| Representativeness | Is coverage concentrated in a few sources, topics, time periods, or fact-check formats? |
| Feasibility | Can the data be accessed and stored within project constraints without relying on prohibited scraping or redistribution? |
| Publication value | Can the dataset's limitations and provenance be cited sufficiently for a defensible paper? |

## Review record and approval authority

Each review must state the reviewer, review date, evidence location, candidate release/version, outcome, limitations, and whether acquisition is permitted. Approval requires all mandatory gates to pass and records the exact approved scope. Any licence change, source-release change, or material label/provenance correction returns the candidate to review.

## Exclusion and escalation rules

- Ambiguous, disputed, satire, opinion, partially verified, or unverified labels are held for explicit policy review; they are never silently forced into a binary class.
- A dataset with only publisher-level labels is not used as an item-level truth corpus without an approved justification and limitations statement.
- If full text is protected, retain only the permitted metadata and reproducible access instructions, or reject the candidate.
- If provenance or licence evidence cannot be archived, defer the candidate rather than relying on memory or a changing web page.
