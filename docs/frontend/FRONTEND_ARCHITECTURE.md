# Frontend Architecture

## Scope

Phase 5.1 creates a dependency-free single-page application shell. It does not change backend routes, ML inference, model package loading, XAI generation, or the frontend -> Node.js -> Python trust boundary.

## Structure

```text
frontend/
  index.html                 static application shell
  public/config.js           optional public API base URL / timeout configuration
  src/css/                   tokens, base, layout, components, page patterns
  src/js/app.js              route orchestration and shared shell composition
  src/js/routing/            hash-route configuration
  src/js/pages/              route-level render functions
  src/js/components/         navigation, footer, breadcrumbs, icons, modal, toast
  src/js/api/                public Node API boundary
  src/js/prediction/         validation, state, loading, result rendering
  src/js/modules/            prediction request lifecycle controller
```

## Routing

The static shell uses hash routes so it can work on simple static hosting without adding server rewrites or changing backend middleware. The route configuration contains `/`, `/predict`, `/dashboard`, `/history`, `/models`, `/research`, `/about`, and `/settings`, rendered as `#/`, `#/predict`, and so on. Home, prediction, research, and models have Phase 5.1 content; dashboard, history, and settings are explicit future placeholders.

When a server rewrite strategy is approved later, the route configuration can be reused for pathname routes. Phase 5.1 intentionally does not alter Express to serve a frontend fallback.

## API ownership

`src/js/api/api.js` is the only fetch boundary. `prediction-api.js` sends `POST /api/predict` to the Node public API and returns its standard envelope. The browser never calls FastAPI directly. `public/config.js` defaults to the documented local Node endpoint (`http://127.0.0.1:3000`) and exposes only public runtime configuration; deployment may provide `window.TruthLensConfig` before it loads, but it must never contain credentials or model secrets.

## Rendering lifecycle

`app.js` derives the active route, renders navigation, page content, and footer, then initializes the prediction interface only if the page contains its form. Route changes reset the page shell, scroll to the top, and move focus to the main content region. Re-rendering does not retain prediction text or history.

## Quality controls

Route configuration has Node built-in tests in `frontend/tests/`. Browser QA validates the rendered shell at desktop and mobile widths. CSS files are separated by concern and all reusable visual primitives live outside route templates.
