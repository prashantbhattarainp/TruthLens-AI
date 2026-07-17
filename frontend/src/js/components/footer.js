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
          <p class="site-footer__text">
            Research-oriented, explainable fake news detection for Indian digital media.
          </p>
        </div>
        <div>
          <nav class="site-footer__links" aria-label="Footer navigation">
            <a href="research.html">Research</a>
            <a href="about.html">About</a>
            <a href="contact.html">Contact</a>
          </nav>
          <p class="site-footer__meta">Platform foundation · Phase 2</p>
        </div>
      </div>
    </footer>
  `;
}
