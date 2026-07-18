import { getRouteHref } from '../routing/routes.js';

export function renderFooter() {
  const footerContainer = document.querySelector('[data-component="footer"]');

  if (!footerContainer) {
    return;
  }

  footerContainer.innerHTML = `
    <footer class="site-footer">
      <div class="container site-footer__inner">
        <div>
          <div class="site-footer__brand">TruthLens AI</div>
          <p class="site-footer__copy">AI-assisted content analysis with transparent, review-oriented results.</p>
        </div>
        <div>
          <nav class="site-footer__links" aria-label="Footer navigation">
            <a href="${getRouteHref('predict')}">Predict</a>
            <a href="${getRouteHref('dashboard')}">Dashboard</a>
            <a href="${getRouteHref('about')}">About</a>
            <a href="${getRouteHref('contact')}">Contact</a>
          </nav>
          <p class="site-footer__meta">TruthLens AI &middot; v1.0.0</p>
        </div>
      </div>
    </footer>
  `;
}
