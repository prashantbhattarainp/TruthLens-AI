import { icon } from './icon.js';
import { getRouteHref, routes } from '../routing/routes.js';

const navigationItems = ['home', 'predict', 'dashboard', 'models', 'research', 'about'];

export function renderNavigation(activeRouteId) {
  const navigationContainer = document.querySelector('[data-component="navigation"]');

  if (!navigationContainer) {
    return;
  }

  const navigationLinks = navigationItems
    .map((routeId) => {
      const route = routes[routeId];
      const currentPageAttribute = route.id === activeRouteId ? ' aria-current="page"' : '';

      return `<li><a class="site-nav__link" href="${getRouteHref(route.id)}"${currentPageAttribute}>${route.label}</a></li>`;
    })
    .join('');

  navigationContainer.innerHTML = `
    <header class="site-header">
      <div class="container site-header__inner">
        <a class="site-brand" href="${getRouteHref('home')}" aria-label="TruthLens AI home">
          <span class="brand-mark">${icon('spark')}</span>
          <span>TruthLens AI</span>
        </a>
        <nav class="site-nav" aria-label="Primary navigation">
          <button
            class="site-nav__toggle"
            type="button"
            aria-label="Open navigation menu"
            aria-expanded="false"
            aria-controls="primary-navigation"
          >
            ${icon('menu')}
            <span>Menu</span>
          </button>
          <ul class="site-nav__list" id="primary-navigation" data-expanded="false">
            ${navigationLinks}
          </ul>
        </nav>
      </div>
    </header>
  `;

  const navigationToggle = navigationContainer.querySelector('.site-nav__toggle');
  const navigationList = navigationContainer.querySelector('.site-nav__list');

  const setExpanded = (expanded) => {
    navigationToggle?.setAttribute('aria-expanded', String(expanded));
    navigationToggle?.setAttribute('aria-label', expanded ? 'Close navigation menu' : 'Open navigation menu');
    navigationList?.setAttribute('data-expanded', String(expanded));
    document.body.dataset.menuOpen = String(expanded);
  };

  navigationToggle?.addEventListener('click', () => {
    setExpanded(navigationToggle.getAttribute('aria-expanded') !== 'true');
  });
  navigationList?.addEventListener('click', (event) => {
    if (event.target.closest('a')) {
      setExpanded(false);
    }
  });
  navigationContainer.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      setExpanded(false);
      navigationToggle?.focus();
    }
  });
}
