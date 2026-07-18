import { icon } from '../components/icon.js';

export function renderPredictPage() {
  return `
    <header class="page-header">
      <div class="container page-header__content">
        <p class="eyebrow">Research prediction</p>
        <h1>Inspect a bounded classification signal.</h1>
        <p>Submit a headline and article to the existing validated backend. The result is not a factual verdict and its decision score is not calibrated confidence.</p>
      </div>
    </header>

    <section class="page-section">
      <div class="container prediction-layout">
        <section class="form-card card--elevated" aria-labelledby="prediction-form-title">
          <div class="form-card__header">
            <div>
              <h2 id="prediction-form-title">Article input</h2>
              <p>Required fields are validated in the browser and again by the backend.</p>
            </div>
            <span class="badge badge--research">Research only</span>
          </div>
          <form data-detection-form novalidate>
            <div class="form-field">
              <label for="headline">Headline</label>
              <p class="form-field__hint" id="headline-hint">A concise headline for the text you want to inspect.</p>
              <input class="input" id="headline" name="headline" type="text" maxlength="300" aria-describedby="headline-hint headline-error headline-counter" required />
              <div class="form-field__meta"><span id="headline-counter" data-headline-counter>0 / 300</span><span>Required</span></div>
              <p class="field-error" id="headline-error" data-headline-error aria-live="polite"></p>
            </div>
            <div class="form-field">
              <label for="article">Article text</label>
              <p class="form-field__hint" id="article-hint">Use at least 100 characters. Do not submit sensitive or unnecessary personal information.</p>
              <textarea class="textarea" id="article" name="article" maxlength="15000" aria-describedby="article-hint article-error article-counter" required></textarea>
              <div class="form-field__meta"><span id="article-counter" data-article-counter>0 / 15,000</span><span>Minimum 100</span></div>
              <p class="field-error" id="article-error" data-article-error aria-live="polite"></p>
            </div>
            <div class="form-field form-field--optional">
              <label for="article-url">Article URL <span class="form-field__optional">Optional — unavailable</span></label>
              <p class="form-field__hint" id="article-url-hint">URL analysis is not part of the current public API, so this field is not submitted.</p>
              <input class="input" id="article-url" type="url" placeholder="URL analysis will be available in a later phase" aria-describedby="article-url-hint" disabled />
            </div>
            <p class="validation-message" data-validation-message aria-live="polite">Add a headline and at least 100 article characters to enable prediction.</p>
            <div class="form-actions">
              <button class="button button--primary" type="submit" data-predict-button disabled>${icon('spark')} Run prediction</button>
              <button class="button button--secondary" type="reset" data-reset-button>Clear input</button>
            </div>
          </form>
        </section>

        <aside class="prediction-sidebar">
          <section class="result-card" data-result-card tabindex="-1" aria-labelledby="result-title" aria-busy="false">
            <p class="result-card__status" aria-live="polite"><span class="status-dot" data-result-status-dot></span><span data-result-status>Waiting for input</span></p>
            <div data-result-initial>
              <div class="result-card__initial">
                <span class="badge badge--muted">No prediction yet</span>
                <h2 id="result-title">Your result will appear here</h2>
                <p>TruthLens will display the research label, processing information, and bounded explanation metadata returned by the backend.</p>
              </div>
            </div>
            <div class="loading-panel" data-loading-panel hidden>
              <span class="loading-panel__spinner" aria-hidden="true"></span>
              <div><h2 data-loading-title>Preparing request</h2><p data-loading-description>Contacting the TruthLens backend.</p></div>
            </div>
            <div class="result-card__error" data-result-error hidden>
              <h2 id="result-error-title" data-result-error-title>Prediction unavailable</h2>
              <p data-result-error-message></p>
            </div>
            <div data-result-content hidden>
              <div class="result-card__header">
                <div><h2 id="result-title-complete" data-result-heading>Prediction</h2><p>Classification result from the configured research candidate.</p></div>
                <div class="result-card__badges"><span class="result-label" data-result-prediction></span><span class="badge badge--muted" data-confidence-badge>Unavailable</span></div>
              </div>
              <div class="result-summary">
                <div class="metric"><span>Confidence</span><strong data-result-confidence>Unavailable</strong></div>
                <div class="metric"><span>Risk level</span><strong data-result-risk>Not assessed</strong></div>
                <div class="metric"><span>Decision margin</span><strong data-decision-score>—</strong></div>
                <div class="metric"><span>Processing</span><strong data-result-time>—</strong></div>
              </div>
              <section class="result-card__section">
                <div class="section-label-row"><h3>Confidence status</h3><span data-confidence-label>Not calibrated</span></div>
                <div class="confidence-progress" data-confidence-progress data-status="unavailable" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" aria-valuetext="Not calibrated; decision score is not a probability."><span data-confidence-progress-fill></span></div>
                <p class="research-callout">The decision margin is not a probability or reliability score. Confidence is intentionally unavailable.</p>
              </section>
              <section class="result-card__section">
                <div class="section-label-row"><h3>Explanation</h3><span>Model behaviour only</span></div>
                <p data-explanation-summary></p>
                <ul class="explanation-list" data-explanation-list></ul>
                <div class="keyword-list" data-keyword-list></div>
              </section>
              <section class="result-card__section" aria-labelledby="explainability-title">
                <div class="section-label-row"><h3 id="explainability-title">Explainability details</h3><span data-explainability-status>Unavailable</span></div>
                <p class="research-callout" data-explainability-disclaimer>Explanation metadata will be shown when the backend provides it.</p>
                <div class="xai-dashboard">
                  <article class="xai-panel">
                    <div class="xai-panel__header"><h4>Top contributing words</h4><span>Margin features</span></div>
                    <p class="xai-panel__description">Features are ranked by their influence on this LinearSVC decision margin.</p>
                    <ul class="contribution-list" data-top-feature-list></ul>
                  </article>
                  <article class="xai-panel">
                    <div class="xai-panel__header"><h4>SHAP summary</h4><span data-shap-status>Unavailable</span></div>
                    <p class="xai-metadata" data-shap-details>Awaiting explanation metadata.</p>
                    <div class="xai-contribution-groups">
                      <section><h5>Supports Fake-class margin</h5><ul class="contribution-list" data-shap-positive-list></ul></section>
                      <section><h5>Supports Real-class margin</h5><ul class="contribution-list" data-shap-negative-list></ul></section>
                    </div>
                  </article>
                  <article class="xai-panel">
                    <div class="xai-panel__header"><h4>LIME equivalent</h4><span data-lime-status>Unavailable</span></div>
                    <p class="xai-metadata" data-lime-details>Awaiting explanation metadata.</p>
                    <div class="xai-contribution-groups">
                      <section><h5>Supports Fake-class margin</h5><ul class="contribution-list" data-lime-positive-list></ul></section>
                      <section><h5>Supports Real-class margin</h5><ul class="contribution-list" data-lime-negative-list></ul></section>
                    </div>
                  </article>
                </div>
              </section>
              <section class="result-card__section">
                <div class="section-label-row"><h3>Model trace</h3><span>Governed metadata</span></div>
                <dl class="model-details">
                  <dt>Model</dt><dd data-model-name>—</dd>
                  <dt>Version</dt><dd data-model-version>—</dd>
                  <dt>Dataset</dt><dd data-dataset-version>—</dd>
                  <dt>Response</dt><dd data-response-timestamp>—</dd>
                  <dt>Request ID</dt><dd data-request-id>—</dd>
                </dl>
              </section>
            </div>
          </section>

          <section class="info-card" aria-labelledby="prediction-boundary-title">
            <p class="eyebrow">Interpretation boundary</p>
            <h2 id="prediction-boundary-title">Use with human review</h2>
            <p class="prose-muted">This UI does not validate Hindi/Hinglish quality, factual truth, source credibility, or a production risk score. Review the research documentation before relying on an output.</p>
          </section>
        </aside>
      </div>
    </section>
  `;
}
