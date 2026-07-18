import { renderExplanationDashboard } from './explanation-panel.js';

function getResultElements(resultCard) {
  return {
    error: resultCard.querySelector('[data-result-error]'),
    errorMessage: resultCard.querySelector('[data-result-error-message]'),
    errorTitle: resultCard.querySelector('[data-result-error-title]'),
    explanationList: resultCard.querySelector('[data-explanation-list]'),
    explanationSummary: resultCard.querySelector('[data-explanation-summary]'),
    initial: resultCard.querySelector('[data-result-initial]'),
    keywordList: resultCard.querySelector('[data-keyword-list]'),
    loadingDescription: resultCard.querySelector('[data-loading-description]'),
    loadingPanel: resultCard.querySelector('[data-loading-panel]'),
    loadingTitle: resultCard.querySelector('[data-loading-title]'),
    resultClassification: resultCard.querySelector('[data-result-classification]'),
    resultContent: resultCard.querySelector('[data-result-content]'),
    resultHeading: resultCard.querySelector('[data-result-heading]'),
    resultPrediction: resultCard.querySelector('[data-result-prediction]'),
    resultStatus: resultCard.querySelector('[data-result-status]'),
    resultStatusDot: resultCard.querySelector('[data-result-status-dot]'),
    resultTime: resultCard.querySelector('[data-result-time]'),
  };
}

function renderList(listElement, items, className, itemElementName = 'li') {
  listElement.replaceChildren(...items.map((item) => {
    const listItem = document.createElement(itemElementName);
    listItem.className = className;
    listItem.textContent = item;
    return listItem;
  }));
}

function setResultStatus(elements, message, state = 'pending') {
  elements.resultStatus.textContent = message;
  elements.resultStatusDot?.classList.toggle('status-dot--success', state === 'success');
}

function hideAllResultStates(elements) {
  elements.error.hidden = true;
  elements.initial.hidden = true;
  elements.loadingPanel.hidden = true;
  elements.resultContent.hidden = true;
}

export function showInitialResult(resultCard) {
  const elements = getResultElements(resultCard);
  hideAllResultStates(elements);
  elements.initial.hidden = false;
  resultCard.setAttribute('aria-busy', 'false');
  resultCard.setAttribute('aria-labelledby', 'result-title');
  resultCard.removeAttribute('aria-label');
  setResultStatus(elements, 'Waiting for input');
}

export function showLoadingState(resultCard, loadingState) {
  const elements = getResultElements(resultCard);
  hideAllResultStates(elements);
  elements.loadingPanel.hidden = false;
  elements.loadingTitle.textContent = loadingState.title;
  elements.loadingDescription.textContent = loadingState.description;
  resultCard.setAttribute('aria-busy', 'true');
  resultCard.setAttribute('aria-label', loadingState.title);
  resultCard.removeAttribute('aria-labelledby');
  setResultStatus(elements, 'Request in progress');
}

export function showPredictionResult(resultCard, response) {
  const elements = getResultElements(resultCard);
  const { data } = response;
  hideAllResultStates(elements);
  elements.resultContent.hidden = false;
  elements.resultHeading.textContent = `Analysis: ${data.prediction}`;
  elements.resultPrediction.textContent = data.prediction;
  elements.resultClassification.textContent = data.prediction;
  elements.resultTime.textContent = `${data.processing_time_ms} ms`;
  setResultStatus(elements, 'Response received from backend', 'success');
  elements.explanationSummary.textContent = data.explanation?.summary ?? 'Explanation details were unavailable.';
  renderList(elements.explanationList, data.explanation?.reasons ?? [], 'explanation-list__item');
  renderList(elements.keywordList, data.keywords ?? [], 'keyword-list__item', 'span');
  renderExplanationDashboard(resultCard, data.explainability);
  resultCard.setAttribute('aria-busy', 'false');
  resultCard.setAttribute('aria-labelledby', 'result-title-complete');
  resultCard.removeAttribute('aria-label');
  resultCard.focus();
}

export function showErrorState(resultCard, { message, title }) {
  const elements = getResultElements(resultCard);
  hideAllResultStates(elements);
  elements.error.hidden = false;
  elements.errorTitle.textContent = title;
  elements.errorMessage.textContent = message;
  resultCard.setAttribute('aria-busy', 'false');
  resultCard.setAttribute('aria-labelledby', 'result-error-title');
  resultCard.removeAttribute('aria-label');
  setResultStatus(elements, 'Prediction unavailable');
  resultCard.focus();
}
