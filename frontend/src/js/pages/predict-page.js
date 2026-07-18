import { icon } from '../components/icon.js';

export function renderPredictPage() {
  return `
    <header class="page-header"><div class="container page-header__content"><p class="eyebrow">Content review</p><h1>Analyze a headline and article.</h1><p>TruthLens returns an automated classification signal and explanation details to support review. It does not determine factual truth.</p></div></header>
    <section class="page-section"><div class="container prediction-layout">
      <section class="form-card card--elevated" aria-labelledby="prediction-form-title">
        <div class="form-card__header"><div><h2 id="prediction-form-title">Article input</h2><p>Required fields are validated in the browser and again by the backend.</p></div><div class="form-card__badges"><span class="badge badge--muted">Independent review advised</span><span class="status-badge status-badge--pending" data-backend-status aria-live="polite">Not checked</span></div></div>
        <form data-detection-form novalidate>
          <div class="form-field"><label for="headline">Headline</label><p class="form-field__hint" id="headline-hint">A concise headline for the text you want to inspect.</p><input class="input" id="headline" name="headline" type="text" maxlength="300" aria-describedby="headline-hint headline-error headline-counter" required /><div class="form-field__meta"><span id="headline-counter" data-headline-counter>0 / 300</span><span>Required</span></div><p class="field-error" id="headline-error" data-headline-error aria-live="polite"></p></div>
          <div class="form-field"><label for="article">Article text</label><p class="form-field__hint" id="article-hint">Use at least 100 characters. Do not submit sensitive or unnecessary personal information.</p><textarea class="textarea" id="article" name="article" maxlength="15000" aria-describedby="article-hint article-error article-counter" required></textarea><div class="form-field__meta"><span id="article-counter" data-article-counter>0 / 15,000</span><span>Minimum 100</span></div><p class="field-error" id="article-error" data-article-error aria-live="polite"></p></div>
          <div class="form-field form-field--optional"><label for="article-url">Article URL <span class="form-field__optional">Optional — unavailable</span></label><p class="form-field__hint" id="article-url-hint">URL analysis is not part of the current public API, so this field is not submitted.</p><input class="input" id="article-url" type="url" placeholder="URL analysis will be available in a future update" aria-describedby="article-url-hint" disabled /></div>
          <p class="validation-message" data-validation-message aria-live="polite">Add a headline and at least 100 article characters to enable prediction.</p>
          <div class="form-actions"><button class="button button--primary" type="submit" data-predict-button disabled>${icon('spark')} Analyze content</button><button class="button button--secondary" type="reset" data-reset-button>Clear input</button></div>
        </form>
      </section>

      <aside class="prediction-sidebar">
        <section class="result-card" data-result-card tabindex="-1" aria-labelledby="result-title" aria-busy="false">
          <p class="result-card__status" aria-live="polite"><span class="status-dot" data-result-status-dot></span><span data-result-status>Waiting for input</span></p>
          <div data-result-initial><div class="result-card__initial"><span class="badge badge--muted">No analysis yet</span><h2 id="result-title">Your result will appear here</h2><p>TruthLens will display the classification outcome, processing information, and explanation details returned by the backend.</p></div></div>
          <div class="loading-panel" data-loading-panel hidden><span class="loading-panel__spinner" aria-hidden="true"></span><div><h2 data-loading-title>Preparing request</h2><p data-loading-description>Contacting the TruthLens backend.</p></div></div>
          <div class="result-card__error" data-result-error hidden><h2 id="result-error-title" data-result-error-title>Prediction unavailable</h2><p data-result-error-message></p></div>
          <div data-result-content hidden>
            <div class="result-card__header"><div><h2 id="result-title-complete" data-result-heading>Analysis result</h2><p>Automated classification guidance for your review.</p></div><div class="result-card__badges"><span class="result-label" data-result-prediction></span></div></div>
            <div class="result-summary"><div class="metric"><span>Classification</span><strong data-result-classification>—</strong></div><div class="metric"><span>Processing</span><strong data-result-time>—</strong></div></div>
            <section class="result-card__section"><div class="section-label-row"><h3>What this means</h3><span>Review guidance</span></div><p data-explanation-summary></p><ul class="explanation-list" data-explanation-list></ul><div class="keyword-list" data-keyword-list></div></section>
            <section class="result-card__section" aria-labelledby="explainability-title"><div class="section-label-row"><h3 id="explainability-title">Explainability</h3><span data-explainability-status>Unavailable</span></div><p class="guidance-callout" data-explainability-disclaimer>Explanation details will be shown when the backend provides them.</p><div class="xai-dashboard">
              <article class="xai-panel"><div class="xai-panel__header"><h4>Top contributing words</h4><span>Classification signals</span></div><p class="xai-panel__description">Features are ranked by their influence on this automated classification.</p><ul class="contribution-list" data-top-feature-list></ul></article>
              <article class="xai-panel"><div class="xai-panel__header"><h4>SHAP summary</h4><span data-shap-status>Unavailable</span></div><p class="xai-metadata" data-shap-details>Awaiting explanation details.</p><div class="xai-contribution-groups"><section><h5>Supports Fake classification</h5><ul class="contribution-list" data-shap-positive-list></ul></section><section><h5>Supports Real classification</h5><ul class="contribution-list" data-shap-negative-list></ul></section></div></article>
              <article class="xai-panel"><div class="xai-panel__header"><h4>LIME summary</h4><span data-lime-status>Unavailable</span></div><p class="xai-metadata" data-lime-details>Awaiting explanation details.</p><div class="xai-contribution-groups"><section><h5>Supports Fake classification</h5><ul class="contribution-list" data-lime-positive-list></ul></section><section><h5>Supports Real classification</h5><ul class="contribution-list" data-lime-negative-list></ul></section></div></article>
            </div></section>
          </div>
        </section>
        <section class="info-card" aria-labelledby="prediction-boundary-title"><p class="eyebrow">Use responsibly</p><h2 id="prediction-boundary-title">Verify before you act</h2><p class="prose-muted">TruthLens does not verify factual truth, source credibility, or legal and medical claims. Use reliable sources and qualified advice for important decisions.</p></section>
      </aside>
    </div></section>
  `;
}
