import { icon } from '../components/icon.js';
import { getRouteHref } from '../routing/routes.js';

const researchCards = [
  ['Explained model behaviour', 'SHAP and LIME describe the signed LinearSVC margin. They do not establish truth, causality, or confidence.', 'spark'],
  ['Transformer benchmark boundary', 'No transformer candidate produced a completed local metric; unavailable results are not substituted with estimates.', 'layers'],
  ['Multilingual boundary', 'Unicode input can be processed, but there is no validated Hindi or Hinglish fake-news performance claim.', 'message'],
  ['Reliability evidence', 'Capitalization and added-context stressors changed validation predictions materially; the model remains uncalibrated.', 'activity'],
];

export function renderResearchPage() {
  return `
    <header class="page-header"><div class="container page-header__content"><p class="eyebrow">Research evidence</p><h1>Findings with their limits attached.</h1><p>TruthLens keeps evaluation, explanation, multilingual, and reliability boundaries visible so the interface does not overclaim.</p></div></header>
    <section class="page-section"><div class="container">
      <div class="grid grid--two">
        ${researchCards.map(([title, copy, iconName]) => `<article class="card"><div class="card__icon">${icon(iconName)}</div><h2 class="card__title">${title}</h2><p class="card__copy">${copy}</p></article>`).join('')}
      </div>
      <div class="alert alert--warning section-offset"><span>${icon('shield')}</span><div><h2 class="alert__title">Current research status</h2><p class="alert__copy">The LinearSVC is an internal research champion with validation Macro F1 0.5398 and MCC 0.1014. It is not deployment-approved, and confidence remains unavailable.</p></div></div>
    </div></section>
    <section class="page-section page-section--surface"><div class="container"><div class="cta-panel"><div><p class="eyebrow">Prediction workspace</p><h2>Explore the API response responsibly.</h2><p>The prediction page makes the public backend contract and its bounded result states visible.</p></div><a class="button button--primary" href="${getRouteHref('predict')}">Open prediction workspace ${icon('arrowRight')}</a></div></div></section>
  `;
}
