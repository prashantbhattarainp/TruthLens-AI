# Frontend Architecture

## Scope

Phase 5.1 establishes the dependency-free single-page application shell; Phase 5.2 adds the prediction/explainability workflow; Phase 5.3 adds the industrial analytics and research dashboard. None changes backend routes, ML inference, model package loading, XAI generation, persistence, or the frontend -> Node.js -> Python trust boundary.

## Structure

```text
frontend/
  index.html                 static application shell
  public/config.js           optional public API base URL / timeout configuration
  src/css/                   tokens, base, layout, components, page patterns, analytics dashboard styles
  src/js/app.js              route orchestration and shared shell composition
  src/js/routing/            hash-route configuration
  src/js/pages/              route-level render functions, including analytics dashboard composition
  src/js/components/         navigation, footer, breadcrumbs, icons, modal, toast
  src/js/api/                public Node API boundary, prediction and operational-status clients
  src/js/analytics/          frozen dashboard evidence and reusable chart renderers
  src/js/prediction/         validation, state, loading, error/confidence/XAI presentation, result rendering
  src/js/modules/            prediction request lifecycle controller
```

## Routing

The static shell uses hash routes so it can work on simple static hosting without adding server rewrites or changing backend middleware. The route configuration contains `/`, `/predict`, `/dashboard`, `/history`, `/models`, `/research`, `/about`, and `/settings`, rendered as `#/`, `#/predict`, and so on. Home, prediction, research, models, and dashboard have content; history and settings remain explicit future placeholders.

When a server rewrite strategy is approved later, the route configuration can be reused for pathname routes. Phase 5.1 intentionally does not alter Express to serve a frontend fallback.

## API ownership

`src/js/api/api.js` is the only fetch boundary. `prediction-api.js` sends `POST /api/predict` to the Node public API and returns its standard envelope. The browser never calls FastAPI directly. `public/config.js` defaults to the documented local Node endpoint (`http://127.0.0.1:3000`) and exposes only public runtime configuration; deployment may provide `window.TruthLensConfig` before it loads, but it must never contain credentials or model secrets.

Phase 5.2 keeps the request contract to `headline` and `article`. The disabled URL control is a visible scope placeholder and is never included in validation or the payload. The result renderer consumes optional explainability metadata defensively and keeps unavailable confidence unavailable.

Phase 5.3 adds an on-demand analytics client for the existing `GET /api/health`, `GET /api/system/health`, `GET /api/model/ready`, and `GET /api/model/version` endpoints. It does not poll, persist operational data, call the Python service from the browser, add database monitoring, or add a new contract. Frozen chart data is isolated in `src/js/analytics/dashboard-data.js`; illustrative data is labelled rather than treated as observed history.

## Rendering lifecycle

`app.js` derives the active route, renders navigation, page content, and footer, then initializes the prediction interface and analytics controller only when their route markup exists. Route changes reset the page shell, scroll to the top, and move focus to the main content region. Re-rendering does not retain prediction text, history, or operational snapshots.

## Quality controls

Route configuration, pure prediction-presentation helpers, and analytics chart/data helpers have Node built-in tests in `frontend/tests/`. Browser QA validates the dashboard at desktop and mobile widths. CSS files are separated by concern and reusable visual primitives live outside route templates.
