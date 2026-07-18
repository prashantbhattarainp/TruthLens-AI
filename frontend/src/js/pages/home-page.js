import { icon } from '../components/icon.js';
import { getRouteHref } from '../routing/routes.js';

const featureCards = [
  { iconName: 'shield', title: 'Privacy-aware input', copy: 'Submit only the content you want assessed. The interface does not provide a prediction history or user profiles.' },
  { iconName: 'spark', tone: 'accent', title: 'Explainable results', copy: 'See the words and phrases that most influenced an automated classification outcome.' },
  { iconName: 'layers', tone: 'success', title: 'Human review first', copy: 'Use the result as one signal alongside trusted reporting, primary sources, and your own judgement.' },
];

function featureCard({ copy, iconName, title, tone = '' }) {
  const toneClass = tone ? ` card__icon--${tone}` : '';
  return `<article class="card"><div class="card__icon${toneClass}">${icon(iconName)}</div><h3 class="card__title">${title}</h3><p class="card__copy">${copy}</p></article>`;
}

export function renderHomePage() {
  return `
    <section class="hero">
      <div class="container hero__grid">
        <div class="hero__copy">
          <p class="eyebrow">AI-assisted content analysis</p>
          <h1>Check the signal. Verify the story.</h1>
          <p class="hero__lede">TruthLens AI helps you review news-style text with an automated fake-news classification signal and clear explanatory context.</p>
          <div class="button-group">
            <a class="button button--primary" href="${getRouteHref('predict')}">Analyze content ${icon('arrowRight')}</a>
            <a class="button button--secondary" href="${getRouteHref('about')}">How TruthLens helps</a>
          </div>
          <p class="hero__fine-print">TruthLens provides automated guidance, not a factual verdict. Independently verify important claims before sharing or acting on them.</p>
        </div>
        <aside class="hero-panel" aria-label="TruthLens product overview">
          <div class="hero-panel__header">
            <div>
              <p class="eyebrow">Product workflow</p>
              <h2 class="hero-panel__title">Clear input. Clear next step.</h2>
              <p class="hero-panel__description">Content review, transparent signals, and service health in one focused interface.</p>
            </div>
            <span class="badge badge--success">Ready to review</span>
          </div>
          <div class="hero-metrics">
            <div class="hero-metric"><span>Step 1</span><strong>Submit text</strong></div>
            <div class="hero-metric"><span>Step 2</span><strong>Review signal</strong></div>
            <div class="hero-metric"><span>Step 3</span><strong>Inspect factors</strong></div>
            <div class="hero-metric"><span>Step 4</span><strong>Verify sources</strong></div>
          </div>
          <p class="hero-panel__note">For consequential decisions, consult credible sources and qualified professionals. Do not rely on a single automated result.</p>
        </aside>
      </div>
    </section>

    <section class="page-section page-section--surface">
      <div class="container">
        <div class="section-heading">
          <p class="section-heading__eyebrow">Built for thoughtful review</p>
          <h2>One product flow, with context.</h2>
          <p class="section-heading__copy">A focused interface makes an automated outcome and its contributing signals easier to understand without overstating what the system knows.</p>
        </div>
        <div class="grid grid--three">${featureCards.map(featureCard).join('')}</div>
      </div>
    </section>

    <section class="page-section">
      <div class="container">
        <div class="section-heading">
          <p class="section-heading__eyebrow">Architecture</p>
          <h2>A simple, dependable service boundary</h2>
          <p class="section-heading__copy">The browser talks only to the validated public API. The backend coordinates requests with a dedicated ML service and returns a safe, consistent response.</p>
        </div>
        <div class="architecture-flow" aria-label="TruthLens system architecture">
          <article class="architecture-flow__node"><small>01 · Browser</small><h3>Product interface</h3><p>Accessible forms, clear result states, and no direct ML-service access.</p></article>
          <div class="architecture-flow__connector" aria-hidden="true">→</div>
          <article class="architecture-flow__node"><small>02 · Public API</small><h3>Node.js backend</h3><p>Validation, response envelopes, retries, request IDs, and safe error handling.</p></article>
          <div class="architecture-flow__connector" aria-hidden="true">→</div>
          <article class="architecture-flow__node"><small>03 · ML service</small><h3>FastAPI analysis</h3><p>Automated classification with optional contributing-word details.</p></article>
          <div class="architecture-flow__connector" aria-hidden="true">→</div>
          <article class="architecture-flow__node"><small>04 · Response</small><h3>Review guidance</h3><p>Outcome, explanation, processing details, and a reminder to independently verify important content.</p></article>
        </div>
      </div>
    </section>

    <section class="page-section page-section--compact">
      <div class="container"><div class="cta-panel"><div><p class="eyebrow">Ready when you are</p><h2>Review a story with more context.</h2><p>The prediction workspace returns an automated classification and its contributing signals, never a factual guarantee.</p></div><a class="button button--primary" href="${getRouteHref('predict')}">Open prediction ${icon('arrowRight')}</a></div></div>
    </section>
  `;
}
