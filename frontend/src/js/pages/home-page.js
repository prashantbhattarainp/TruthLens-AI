import { icon } from '../components/icon.js';
import { getRouteHref } from '../routing/routes.js';

const featureCards = [
  {
    iconName: 'shield',
    title: 'Bounded research signal',
    copy: 'A transparent classification workflow with documented scope, limitations, and human-review expectations.',
  },
  {
    iconName: 'spark',
    tone: 'accent',
    title: 'Inspectable output',
    copy: 'Prediction responses can include bounded SHAP and LIME features that describe the model margin.',
  },
  {
    iconName: 'layers',
    tone: 'success',
    title: 'Governed evidence',
    copy: 'Model lineage, evaluation limits, multilingual boundaries, and reliability findings are recorded together.',
  },
];

function featureCard({ copy, iconName, title, tone = '' }) {
  const toneClass = tone ? ` card__icon--${tone}` : '';

  return `
    <article class="card">
      <div class="card__icon${toneClass}">${icon(iconName)}</div>
      <h3 class="card__title">${title}</h3>
      <p class="card__copy">${copy}</p>
    </article>
  `;
}

export function renderHomePage() {
  return `
    <section class="hero">
      <div class="container hero__grid">
        <div class="hero__copy">
          <p class="eyebrow">Research workspace</p>
          <h1>See the signal. Keep the uncertainty.</h1>
          <p class="hero__lede">TruthLens AI is an explainable fake-news classification research platform for investigating text patterns in Indian digital-media contexts.</p>
          <div class="button-group">
            <a class="button button--primary" href="${getRouteHref('predict')}">Start a research prediction ${icon('arrowRight')}</a>
            <a class="button button--secondary" href="${getRouteHref('research')}">Explore research evidence</a>
          </div>
          <p class="hero__fine-print">The current model is an internal research candidate. It is not a fact checker, a confidence score, or a production-approved decision system.</p>
        </div>
        <aside class="hero-panel" aria-label="Current research model status">
          <div class="hero-panel__header">
            <div>
              <p class="eyebrow">Current model</p>
              <h2 class="hero-panel__title">LinearSVC research champion</h2>
              <p class="hero-panel__description">TF-IDF unigram/bigram · English-derived evidence</p>
            </div>
            <span class="badge badge--research">Research only</span>
          </div>
          <div class="hero-metrics">
            <div class="hero-metric"><span>Validation Macro F1</span><strong>0.5398</strong></div>
            <div class="hero-metric"><span>Validation MCC</span><strong>0.1014</strong></div>
            <div class="hero-metric"><span>Confidence</span><strong>Unavailable</strong></div>
            <div class="hero-metric"><span>Deployment</span><strong>Not approved</strong></div>
          </div>
          <p class="hero-panel__note">Phase 4 found sensitivity to capitalization and appended context. Read the result as a bounded research signal, with human review.</p>
        </aside>
      </div>
    </section>

    <section class="page-section page-section--surface">
      <div class="container">
        <div class="section-heading">
          <p class="section-heading__eyebrow">Platform foundation</p>
          <h2>Designed for evidence-aware research</h2>
          <p class="section-heading__copy">A focused interface makes the model’s output, explanation boundary, and research safeguards visible without overstating what the system knows.</p>
        </div>
        <div class="grid grid--three">
          ${featureCards.map(featureCard).join('')}
        </div>
      </div>
    </section>

    <section class="page-section">
      <div class="container">
        <div class="section-heading">
          <p class="section-heading__eyebrow">Architecture</p>
          <h2>A deliberate three-layer trust boundary</h2>
          <p class="section-heading__copy">The browser only talks to the validated public API. The backend and ML service retain the existing integrity, lineage, and explainability controls.</p>
        </div>
        <div class="architecture-flow" aria-label="TruthLens system architecture">
          <article class="architecture-flow__node"><small>01 · Browser</small><h3>Research interface</h3><p>Accessible forms, clear result states, and no direct ML-service access.</p></article>
          <div class="architecture-flow__connector" aria-hidden="true">→</div>
          <article class="architecture-flow__node"><small>02 · Public API</small><h3>Node.js backend</h3><p>Validation, envelopes, retries, request IDs, and safe error handling.</p></article>
          <div class="architecture-flow__connector" aria-hidden="true">→</div>
          <article class="architecture-flow__node"><small>03 · ML service</small><h3>FastAPI + XAI</h3><p>Integrity-checked prediction plus optional SHAP/LIME margin explanation.</p></article>
          <div class="architecture-flow__connector" aria-hidden="true">→</div>
          <article class="architecture-flow__node"><small>04 · Evidence</small><h3>Frozen package</h3><p>Versioned candidate, research registry, cards, and reliability documentation.</p></article>
        </div>
      </div>
    </section>

    <section class="page-section page-section--compact">
      <div class="container">
        <div class="cta-panel">
          <div>
            <p class="eyebrow">Ready when you are</p>
            <h2>Run a transparent research prediction.</h2>
            <p>The prediction workspace keeps confidence unavailable, labels the decision score correctly, and returns model-behaviour evidence rather than a factual verdict.</p>
          </div>
          <a class="button button--primary" href="${getRouteHref('predict')}">Open prediction workspace ${icon('arrowRight')}</a>
        </div>
      </div>
    </section>
  `;
}
