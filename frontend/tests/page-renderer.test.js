import test from 'node:test';
import assert from 'node:assert/strict';

import { renderPage, renderPageSkeleton } from '../src/js/pages/page-renderer.js';
import { routes } from '../src/js/routing/routes.js';

test('renders an announced skeleton and a recoverable unknown-route page', async () => {
  const root = { innerHTML: '' };

  renderPageSkeleton(root, routes.predict);
  assert.match(root.innerHTML, /Loading Predict/);
  assert.match(root.innerHTML, /page-skeleton/);

  await renderPage(root, routes.notFound);
  assert.match(root.innerHTML, /That page is not available/);
  assert.match(root.innerHTML, /Return home/);
});
