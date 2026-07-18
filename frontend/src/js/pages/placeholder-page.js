import { icon } from '../components/icon.js';

const pageContent = {
  about: ['About TruthLens AI', 'A research platform built to make the limits, lineage, and interpretation of model outputs visible.', 'This route is ready for the future project and team narrative.'],
  dashboard: ['Research dashboard', 'A future workspace for governed aggregate monitoring and research review.', 'No history, metrics stream, or monitoring claim is implemented in Phase 5.1.'],
  history: ['Prediction history', 'A future view for authorized, privacy-governed research records.', 'Prediction retention and user history are not implemented in Phase 5.1.'],
  settings: ['Workspace settings', 'A future area for user preferences and environment-aware controls.', 'No user-account or settings persistence is implemented in Phase 5.1.'],
};

export function renderPlaceholderPage(route) {
  const [title, description, boundary] = pageContent[route.id] ?? pageContent.about;

  return `
    <header class="page-header"><div class="container page-header__content"><p class="eyebrow">Future route</p><h1>${title}</h1><p>${description}</p></div></header>
    <section class="page-section"><div class="container"><div class="empty-state"><div class="card__icon">${icon('layers')}</div><h2>Foundation route ready</h2><p>${boundary}</p><span class="badge badge--muted">Planned for a later Phase 5 milestone</span></div></div></section>
  `;
}
