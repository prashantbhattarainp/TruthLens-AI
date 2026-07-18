import { icon } from '../components/icon.js';
import { getRouteHref } from '../routing/routes.js';

export function renderNotFoundPage() {
  return `
    <header class="page-header"><div class="container page-header__content"><p class="eyebrow">Page not found</p><h1>That page is not available.</h1><p>The address may be incomplete, or the page may have moved.</p></div></header>
    <section class="page-section"><div class="container"><div class="empty-state"><div class="card__icon">${icon('message')}</div><h2>Find your way back</h2><p>Use the primary navigation, return home, or open the prediction flow.</p><div class="button-group"><a class="button button--primary" href="${getRouteHref('home')}">Return home</a><a class="button button--secondary" href="${getRouteHref('predict')}">Open prediction ${icon('arrowRight')}</a></div></div></div></section>
  `;
}
