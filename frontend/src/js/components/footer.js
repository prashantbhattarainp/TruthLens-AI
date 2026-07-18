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
          <p class="site-footer__copy">Research-oriented, explainable classification for Indian digital-media research.</p>
        </div>
        <div>
          <nav class="site-footer__links" aria-label="Footer navigation">
            <a href="${getRouteHref('predict')}">Predict</a>
            <a href="${getRouteHref('research')}">Research</a>
            <a href="${getRouteHref('models')}">Models</a>
            <a href="${getRouteHref('about')}">About</a>
          </nav>
          <p class="site-footer__meta">Prediction dashboard - Phase 5.2 - Research use only</p>
        </div>
      </div>
    </footer>
  `;
}
