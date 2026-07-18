# Visual Asset Inventory

## Phase 5.3 assets

| Asset | Location | Source / license | Use |
| --- | --- | --- | --- |
| Research analytics flow illustration | `frontend/assets/images/analytics-research-flow.svg` | Original TruthLens Phase 5.3 SVG artwork; project-owned, no third-party attribution required | Dashboard hero illustration |
| Interface icon set | `frontend/src/js/components/icon.js` | Original inline SVG paths maintained in this repository; project-owned | Navigation, monitoring, cards, and actions |
| Research figures | `docs/research/figures/` | Existing project-generated aggregate figures; source and generation details in that folder's README | Documentation only; not copied into dashboard UI |

## External-asset statement

Phase 5.3 adds **no external images, icon packs, fonts, illustrations, scripts, or chart libraries**. The dashboard therefore has no third-party image licence or attribution requirement. This avoids unreviewed copyright and loading dependencies while keeping the UI scalable through SVG and CSS.

## Performance and accessibility

- The hero illustration is a small local SVG with explicit intrinsic dimensions.
- Icons are inline SVG and inherit surrounding text colour.
- Charts are generated from lightweight local data and SVG/CSS rather than a charting dependency.
- Every rendered visual has a text label or accessible description; purely decorative visual treatment is not used as evidence.

Any future external asset must be added to this inventory with creator, source URL, licence, attribution wording, local filename, and intended UI use before it is committed.
