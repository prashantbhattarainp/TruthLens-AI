export function getPredictionElements(form) {
  const resultCard = document.querySelector('[data-result-card]');

  return {
    articleError: form.querySelector('[data-article-error]'),
    articleInput: form.querySelector('#article'),
    articleCounter: form.querySelector('[data-article-counter]'),
    backendStatus: document.querySelector('[data-backend-status]'),
    form,
    headlineError: form.querySelector('[data-headline-error]'),
    headlineInput: form.querySelector('#headline'),
    headlineCounter: form.querySelector('[data-headline-counter]'),
    predictButton: form.querySelector('[data-predict-button]'),
    resetButton: form.querySelector('[data-reset-button]'),
    resultCard,
    validationMessage: form.querySelector('[data-validation-message]'),
  };
}

function setFieldValidation(inputElement, errorElement, errorMessage, shouldShowError) {
  const visibleErrorMessage = shouldShowError ? (errorMessage ?? '') : '';

  inputElement.setAttribute('aria-invalid', String(Boolean(visibleErrorMessage)));
  errorElement.textContent = visibleErrorMessage;
}

export function renderValidation(elements, validation, touchedFields) {
  setFieldValidation(
    elements.headlineInput,
    elements.headlineError,
    validation.errors.headline,
    touchedFields.has('headline'),
  );
  setFieldValidation(
    elements.articleInput,
    elements.articleError,
    validation.errors.article,
    touchedFields.has('article'),
  );

  elements.predictButton.disabled = !validation.isValid;
  elements.validationMessage.dataset.state = validation.isValid ? 'valid' : 'invalid';
  elements.validationMessage.textContent = validation.isValid
    ? 'Inputs are ready. Submit them to the TruthLens backend for prediction.'
    : 'Add a headline and at least 100 article characters to enable prediction.';
}

export function setFormBusy(elements, isBusy) {
  elements.headlineInput.disabled = isBusy;
  elements.articleInput.disabled = isBusy;
  elements.predictButton.disabled = isBusy;
  elements.resetButton.disabled = isBusy;
  elements.form.setAttribute('aria-busy', String(isBusy));

  if (isBusy) {
    elements.validationMessage.dataset.state = 'loading';
    elements.validationMessage.textContent =
      'Contacting the TruthLens backend. The form is locked.';
  }
}

export function showRequestError(elements, { message }) {
  elements.validationMessage.dataset.state = 'error';
  elements.validationMessage.textContent = message;
}

export function setBackendStatus(elements, { message, state }) {
  if (!elements.backendStatus) {
    return;
  }

  elements.backendStatus.className = `status-badge status-badge--${state}`;
  elements.backendStatus.textContent = message;
}

export function focusFirstInvalidField(elements, validation) {
  if (validation.errors.headline) {
    elements.headlineInput.focus();
    return;
  }

  if (validation.errors.article) {
    elements.articleInput.focus();
  }
}
