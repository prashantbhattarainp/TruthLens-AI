import { icon } from '../components/icon.js';
import { getRouteHref } from '../routing/routes.js';

const pageContent = {
  about: ['About TruthLens AI', 'TruthLens AI is an AI-assisted fake-news detection system designed to support thoughtful content review.', 'Results are guidance, not a substitute for independent fact-checking or professional advice.'],
  contact: ['Contact', 'Have feedback, found an issue, or want to contribute?', 'Open an issue in the project repository with steps to reproduce and any relevant, non-sensitive details.'],
  settings: ['Settings', 'Choose how you use this device.', 'Preferences and user accounts are not stored in v1.0.0.'],
};

export function renderPlaceholderPage(route) {
  const [title, description, boundary] = pageContent[route.id] ?? pageContent.about;

  return `
    <header class="page-header"><div class="container page-header__content"><p class="eyebrow">TruthLens AI</p><h1>${title}</h1><p>${description}</p></div></header>
    <section class="page-section"><div class="container"><div class="empty-state"><div class="card__icon">${icon('layers')}</div><h2>Designed with clear boundaries</h2><p>${boundary}</p><a class="button button--secondary" href="${getRouteHref('dashboard')}">Open dashboard</a></div></div></section>
  `;
}
