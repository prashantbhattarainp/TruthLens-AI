# Dataset Landscape Analysis and Selection Report

**Project:** TruthLens AI  
**Milestone:** Phase 3.2 - Dataset Landscape Analysis and Final Dataset Selection  
**Date:** 2026-07-17  
**Status:** Complete as a research-planning milestone. Dataset acquisition remains prohibited pending gate approval.

## Executive summary

Seven publicly described candidates were assessed against the Phase 3.1 protocol. The landscape contains useful Indian resources, but public availability is repeatedly confused with permission to use or redistribute news content. Only BharatFakeNewsKosh declares a licence compatible with a non-commercial research review; even it requires release-specific source-rights, translation, schema, and label audits.

The selected strategy is therefore conditional and role-separated: BharatFakeNewsKosh as the provisional primary source, FactDrill as a separate Indian-context source, and the COVID-19 Fake News Dataset as a frozen external evaluation source. This is a research decision, not permission to acquire data or a claim that any selected source is already fit for training.

## Method

Candidate discovery was limited to publicly described, text-bearing fake-news or fact-check resources with a credible original paper, institutional repository, DOI record, author repository, or named public dataset page. The review captured source, access route, reported scale/languages/labels, text availability, licence evidence, Indian relevance, adoption signals, strengths, and weaknesses. It then applied the weighted framework in [Dataset Scoring](DATASET_SCORING.md) and the mandatory gates in [Dataset Selection Strategy](DATASET_SELECTION_STRATEGY.md).

No candidate was downloaded, opened as a data file, preprocessed, deduplicated, split, or modelled. Counts and fields below are reported claims that must be verified from an approved immutable release in Phase 3.3.

## Findings

The complete side-by-side evidence is maintained in [Dataset Comparison Matrix](DATASET_COMPARISON_MATRIX.md). The key result is that a single dataset cannot credibly answer the entire research question:

- A primary Indian English-first corpus is needed for controlled baseline development.
- A separate Indian fact-check/social-context corpus is needed to probe content-unit, language, and source shift without contaminating training.
- A separate non-Indian corpus is needed to test whether apparent performance is confined to the primary source.

The strategy and its constraints are formalised in [Final Dataset Selection](FINAL_DATASET_SELECTION.md). The rights assessment is in [Dataset Licences](DATASET_LICENSES.md).

## Principal research decisions

1. Select BFNK only as a **provisional source**, and restrict the main study to a future audited native-English derivative. Translation-derived English must not be silently mixed into the primary reported result.
2. Keep FactDrill separate from primary training. Its contextual richness is valuable, but task-unit and licence differences make pooled data invalid.
3. Use the COVID-19 corpus once as a frozen external test only. It measures a domain shift, not India-wide performance.
4. Reject IFND and FakeNewsNet for the initial study; defer FakeNewsIndia and the Zenodo multilingual record. These decisions are documented so later work can revisit them with new evidence rather than repeat discovery.
5. Treat every selection as reversible before acquisition. A failed licence, rights, provenance, label, or coverage gate cancels the corresponding role without lowering the standard.

## Outcome

The selection report, comparison matrix, scoring record, licence assessment, registry updates, RDL, and engineering-journal entry provide a complete Phase 3.2 research record. The architecture is unchanged and the mock application remains untouched. The next permissible action is governance approval for Phase 3.3, not downloading data.
