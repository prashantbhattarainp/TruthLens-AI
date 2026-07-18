export const routes = Object.freeze({
  about: { id: 'about', label: 'About', path: '/about', title: 'About | TruthLens AI' },
  contact: { id: 'contact', label: 'Contact', path: '/contact', title: 'Contact | TruthLens AI' },
  dashboard: { id: 'dashboard', label: 'Dashboard', path: '/dashboard', title: 'Dashboard | TruthLens AI' },
  home: { id: 'home', label: 'Home', path: '/', title: 'TruthLens AI | AI-assisted content analysis' },
  notFound: { id: 'notFound', label: 'Page not found', path: '/not-found', title: 'Page not found | TruthLens AI' },
  predict: { id: 'predict', label: 'Predict', path: '/predict', title: 'Predict | TruthLens AI' },
  settings: { id: 'settings', label: 'Settings', path: '/settings', title: 'Settings | TruthLens AI' },
});

const routeByPath = new Map(Object.values(routes).map((route) => [route.path, route]));

export function getRouteFromHash(hash = '') {
  const path = hash.replace(/^#/, '').replace(/\/+$/, '') || '/';

  return routeByPath.get(path) ?? (path === '/' ? routes.home : routes.notFound);
}

export function getRouteHref(routeId) {
  const route = routes[routeId] ?? routes.home;

  return `#${route.path}`;
}

export function setRoute(routeId) {
  window.location.hash = getRouteHref(routeId);
}
