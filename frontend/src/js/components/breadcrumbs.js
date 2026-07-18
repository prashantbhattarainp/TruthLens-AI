import { getRouteHref, routes } from '../routing/routes.js';

export function renderBreadcrumbs(route) {
  if (route.id === routes.home.id) {
    return '';
  }

  return `
    <div class="container">
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <ol class="breadcrumb__list">
          <li class="breadcrumb__item"><a href="${getRouteHref('home')}">Home</a></li>
          <li class="breadcrumb__item" aria-current="page">${route.label}</li>
        </ol>
      </nav>
    </div>
  `;
}
