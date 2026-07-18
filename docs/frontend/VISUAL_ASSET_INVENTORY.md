# Visual Asset Inventory

## Phase 5.3 assets

| Asset | Location | Source / license | Use |
| --- | --- | --- | --- |
| Research analytics flow illustration | `frontend/assets/images/analytics-research-flow.svg` | Original TruthLens Phase 5.3 SVG artwork; project-owned, no third-party attribution required | Dashboard hero illustration |
| Interface icon set | `frontend/src/js/components/icon.js` | Original inline SVG paths maintained in this repository; project-owned | Navigation, monitoring, cards, and actions |
| Research figures | `docs/research/figures/` | Existing project-generated aggregate figures; source and generation details in that folder's README | Documentation only; not copied into dashboard UI |
| RC system architecture diagram | `docs/assets/release-candidate/system-architecture.svg` | Original Phase 5.5 SVG artwork; project-owned, no third-party attribution required | README and deployment documentation |
| RC prediction workflow diagram | `docs/assets/release-candidate/prediction-workflow.svg` | Original Phase 5.5 SVG artwork; project-owned, no third-party attribution required | README and API/deployment documentation |
| RC browser screenshots | `docs/assets/release-candidate/screenshots/` | Original local Phase 5.5 browser captures using synthetic input; project-owned, no third-party attribution required | Release documentation / README evidence |

## External-asset statement

Phase 5.3/5.5 add **no external images, icon packs, fonts, illustrations, scripts, or chart libraries**. The dashboard and release documentation therefore have no third-party image licence or attribution requirement. This avoids unreviewed copyright and loading dependencies while keeping the UI scalable through SVG and CSS.

## Performance and accessibility

- The hero illustration is a small local SVG with explicit intrinsic dimensions.
- Icons are inline SVG and inherit surrounding text colour.
- Charts are generated from lightweight local data and SVG/CSS rather than a charting dependency.
- Every rendered visual has a text label or accessible description; purely decorative visual treatment is not used as evidence.

Any future external asset must be added to this inventory with creator, source URL, licence, attribution wording, local filename, and intended UI use before it is committed.
