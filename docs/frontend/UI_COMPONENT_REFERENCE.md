# Analytics UI Component Reference

## Phase 5.3 components

| Component | Location | Purpose | State boundary |
| --- | --- | --- | --- |
| Analytics dashboard page | `pages/analytics-dashboard-page.js` | Semantic route composition | Static evidence only; no persistence |
| Dashboard data | `analytics/dashboard-data.js` | Frozen values with provenance | Update only from governed research evidence |
| Chart renderer | `analytics/chart-renderer.js` | Reusable accessible SVG/bar visualizations | No inference or metric calculation |
| Operational API client | `api/system-api.js` | Existing read-only status requests | Public Node API only |
| Dashboard controller | `modules/analytics-dashboard.js` | Chart selection and status refresh | No polling or data storage |
| Monitoring item | Dashboard markup + `analytics.css` | Textual health status | Database remains not instrumented |
| Status pill | `analytics.css` | Text-and-colour service state | Healthy, unavailable, or not instrumented |
| Evidence chart | Chart renderer + `analytics.css` | Frozen / illustrative visual summary | Must label data class |

## Reuse rules

- Keep public fetches inside `src/js/api/`; route templates must not call `fetch`.
- Put reusable data-to-visual functions in `src/js/analytics/`.
- Update interactive control state with native buttons before adding custom ARIA patterns.
- Use the existing token, card, badge, button, toast, and icon primitives before introducing a new visual treatment.
- Do not add prediction history, user profiles, database status, or model-promotion controls until a separate approved contract exists.

The existing [Component Library](COMPONENT_LIBRARY.md) remains the foundation for app-wide components. This reference describes the analytics-specific layer added in Phase 5.3.
