import { icon } from '../components/icon.js';

export function renderModelsPage() {
  return `
    <header class="page-header"><div class="container page-header__content"><p class="eyebrow">Model registry view</p><h1>Current model state, without promotion theatre.</h1><p>The model view surfaces the research champion and challenger boundaries. It does not imply production readiness.</p></div></header>
    <section class="page-section"><div class="container">
      <div class="grid grid--three">
        <article class="card card--elevated"><div class="card__icon">${icon('check')}</div><p class="placeholder-card__label">Current champion</p><h2 class="card__title">LinearSVC</h2><p class="card__copy">TF-IDF unigram/bigram package integrated for internal research only.</p><p><span class="badge badge--research">Not deployment approved</span></p></article>
        <article class="card"><div class="card__icon card__icon--accent">${icon('layers')}</div><p class="placeholder-card__label">Best ensemble</p><h2 class="card__title">Hard / weighted vote</h2><p class="card__copy">Macro F1 0.5447 on validation, inside the practical-tie tolerance and not integrated.</p><p><span class="badge badge--warning">Research challenger</span></p></article>
        <article class="card"><div class="card__icon card__icon--success">${icon('activity')}</div><p class="placeholder-card__label">Transformer state</p><h2 class="card__title">No completed result</h2><p class="card__copy">Access and CPU constraints prevented completed transformer evaluation in Phase 4.</p><p><span class="badge badge--muted">Unevaluated</span></p></article>
      </div>
      <div class="table-wrap section-offset"><table class="table"><caption class="sr-only">Current model research state</caption><thead><tr><th scope="col">Model</th><th scope="col">Evidence</th><th scope="col">Confidence</th><th scope="col">Deployment</th></tr></thead><tbody><tr><th scope="row">TL-LSVM-TFIDF-v1.1.0-rc.1</th><td>Validation-only; Macro F1 0.5398</td><td>Unavailable</td><td>Not approved</td></tr><tr><th scope="row">Classical ensembles</th><td>Validation-only challenger comparison</td><td>No calibrated evidence</td><td>Not approved</td></tr><tr><th scope="row">Transformers</th><td>No completed artifact / metric</td><td>Not available</td><td>Not eligible</td></tr></tbody></table></div>
    </div></section>
  `;
}
