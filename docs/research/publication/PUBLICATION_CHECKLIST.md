# Publication Checklist

## Package integrity

| Check | Status | Evidence |
| --- | --- | --- |
| Final results and comparison tables present | Complete | `FINAL_RESULTS_TABLES.md`, `FINAL_COMPARISON_TABLES.md` |
| Figure index covers tracked Phase 4 assets | Complete | `FINAL_FIGURES_INDEX.md`; 13 aggregate 300-DPI PNGs |
| Experiment, model, data, and decision records aligned | Complete | Registries, cards, RDL-017, EJ-025 |
| No new model, dataset, API, or architecture introduced | Complete | Phase 4.6 boundary record |
| Registry status and champion identity are consistent | Complete | `ml/metadata/model-registry.json` |
| Required publication paths and figure hashes verify | Complete when `verify_phase_4_publication.py` exits 0 | Reproducibility guide |
| Markdown internal links verify | Complete when `verify_phase_4_publication.py` exits 0 | Reproducibility guide |

## Reporting safeguards

| Requirement | Status | Required wording |
| --- | --- | --- |
| Model status | Mandatory | Internal research champion; not deployment-approved |
| Test evidence | Mandatory | No post-tuning protected-test result for the champion or ensembles |
| Confidence | Mandatory | LinearSVC margin is uncalibrated; confidence unavailable |
| Multilingual evidence | Mandatory | Input compatibility only; no Hindi/Hinglish classifier claim |
| Transformer evidence | Mandatory | No completed transformer result exists |
| Fairness/generalization | Mandatory | Descriptive slices only; no demographic fairness or external-generalization claim |
| Perturbation evidence | Mandatory | Deterministic inherited-label stress diagnostics, not real-world robustness proof |

## External-submission gates

The documentation package is ready for transparent internal research handoff. External publication still needs author/reviewer sign-off, data and model rights review, venue formatting, citation review, and a decision on how to handle the unavailable historical Phase 1-3 primary Markdown files. Deployment is separately blocked by the research, calibration, robustness, multilingual, fairness, monitoring, and human-review gates in the Model Card.
