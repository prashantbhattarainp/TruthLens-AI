import test from 'node:test';
import assert from 'node:assert/strict';

import { getRouteFromHash, getRouteHref, routes } from '../src/js/routing/routes.js';

test('resolves each configured hash route', () => {
  for (const route of Object.values(routes)) {
    assert.equal(getRouteFromHash(getRouteHref(route.id)).id, route.id);
  }
});

test('falls back to home for unknown or empty routes', () => {
  assert.equal(getRouteFromHash('').id, 'home');
  assert.equal(getRouteFromHash('#/not-a-route').id, 'home');
});
