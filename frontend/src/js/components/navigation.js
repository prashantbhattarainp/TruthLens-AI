const navigationItems = [
  { id: 'home', label: 'Home', href: 'index.html' },
  { id: 'detection', label: 'Detection', href: 'detection.html' },
  { id: 'research', label: 'Research', href: 'research.html' },
  { id: 'about', label: 'About', href: 'about.html' },
  { id: 'contact', label: 'Contact', href: 'contact.html' },
];

export function renderNavigation(activePage) {
  const navigationContainer = document.querySelector('[data-component="navigation"]');

  if (!navigationContainer) {
    return;
  }

  const navigationLinks = navigationItems
    .map(({ id, label, href }) => {
      const currentPageAttribute = id === activePage ? ' aria-current="page"' : '';

      return `<li><a class="site-nav__link" href="${href}"${currentPageAttribute}>${label}</a></li>`;
    })
    .join('');

  navigationContainer.innerHTML = `
    <header class="site-header">
      <div class="container site-header__inner">
        <a class="site-brand" href="index.html" aria-label="TruthLens AI home">TruthLens AI</a>
        <nav class="site-nav" aria-label="Primary navigation">
          <button
            class="site-nav__toggle"
            type="button"
            aria-expanded="false"
            aria-controls="primary-navigation"
          >
            Menu
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

  navigationToggle?.addEventListener('click', () => {
    const isExpanded = navigationToggle.getAttribute('aria-expanded') === 'true';
    const nextExpandedValue = String(!isExpanded);

    navigationToggle.setAttribute('aria-expanded', nextExpandedValue);
    navigationList?.setAttribute('data-expanded', nextExpandedValue);
  });
}
