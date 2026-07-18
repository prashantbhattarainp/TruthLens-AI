import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

const shell = await readFile(new URL('../index.html', import.meta.url), 'utf8');

test('application shell has baseline accessibility landmarks', () => {
  assert.match(shell, /<html lang="en">/);
  assert.match(shell, /class="skip-link" href="#main-content"/);
  assert.match(shell, /<main class="main-content" id="main-content" tabindex="-1" data-app-root><\/main>/);
  assert.match(shell, /aria-live="polite" aria-relevant="additions" data-toast-region/);
});

test('application shell loads the tokenized CSS and module entrypoint', () => {
  for (const stylesheet of ['tokens.css', 'base.css', 'layout.css', 'components.css', 'pages.css', 'analytics.css']) {
    assert.match(shell, new RegExp(`src/css/${stylesheet.replace('.', '\\.')}`));
  }
  assert.match(shell, /type="module" src="src\/js\/app\.js"/);
});
