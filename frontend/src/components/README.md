# Frontend Component Contracts

The static frontend uses small, focused components to keep the initial vanilla JavaScript implementation extensible.

- `js/components/navigation.js` renders the primary navigation and its accessible mobile-menu control.
- `js/components/footer.js` renders the shared footer.
- Reusable visual component patterns are defined by CSS classes: `hero`, `feature-card`, `section-heading`, `architecture-flow`, and `cta-panel`.
- `js/modules/detection-interface.js` is a focused controller for the backend prediction request lifecycle.
- `js/api/api.js` is the only frontend fetch boundary. `js/api/prediction-api.js` exposes the prediction-specific request function.
- `js/prediction/validation.js`, `character-counter.js`, `ui.js`, `loading.js`, `result-card.js`, and `state.js` separate validation, local UI behaviour, loading, response rendering, and request state.
- `public/config.js` supplies the runtime API base URL and timeout without placing those values in UI components.

All pages load `js/app.js`, which composes these components according to the page identifier in the document body.
