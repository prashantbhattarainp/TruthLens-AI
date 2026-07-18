# Performance Optimization

## Phase 5.4 changes

The static frontend remains dependency-free: it uses browser-native ES modules, local CSS, original inline SVG icons, and one local SVG illustration. No framework runtime, chart package, image CDN, tracker, polling loop, or new backend endpoint was added.

| Concern | Implemented approach |
| --- | --- |
| Route code | Page renderers are loaded only for the active hash route through dynamic ES-module imports. The shell, navigation, breadcrumbs, and routing remain small initial code. |
| Loading feedback | A lightweight CSS skeleton appears while a route module resolves. The animation respects `prefers-reduced-motion`. |
| DOM work | Route rendering replaces the page region once, and only the prediction or analytics controller for the active route is initialized. |
| Assets | The dashboard uses a local SVG with intrinsic dimensions and meaningful text alternative. Icons are inline SVG; no external icon or chart library is requested. |
| Operational reads | Status checks remain user-triggered and use the existing endpoints only. API reads use bounded abort timeouts and `cache: no-store`, avoiding stale health/model-state presentation. |
| CSS | Tokens, base rules, layout, shared components, page styles, and analytics styles are separated by concern. Responsive grids use intrinsic `minmax(0, ...)` sizing to avoid accidental overflow. |

## Measurement and release guidance

The repository's static preview is useful for functional QA, not for production performance scores. Measure the deployed, compressed build with representative network and device profiles. Record at least:

- initial route transfer size and loaded module requests;
- LCP, INP, CLS, and accessibility findings from a production-like environment;
- cache headers for immutable versioned static assets;
- API timeout/error rate separately from page-load metrics.

The only dashboard illustration is above the fold, so it is intentionally not lazy-loaded. If future pages add below-the-fold raster media, provide dimensions, modern responsive formats, and lazy loading after checking the visual/assistive impact.

## Deployment recommendations

1. Serve versioned static assets with Brotli or gzip compression and long immutable cache lifetimes; keep `index.html` short-lived so new route manifests can be discovered.
2. Add a deployment-owned Content Security Policy and HTTPS. Do not embed secrets in `public/config.js`.
3. Preserve the API timeout boundary and no-store policy for operational reads. Do not turn the dashboard into a polling or retention system without an approved architecture change.
4. Establish real-user monitoring only after privacy, retention, and governance requirements are approved; it is deliberately outside this frontend milestone.
