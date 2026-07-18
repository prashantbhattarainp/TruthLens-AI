export const VALIDATION_LIMITS = Object.freeze({
  headlineMaxLength: 300,
  articleMinLength: 100,
  articleMaxLength: 15000,
});

function getTrimmedValue(inputElement) {
  return inputElement.value.trim();
}

export function trimFormValues({ headlineInput, articleInput }) {
  headlineInput.value = getTrimmedValue(headlineInput);
  articleInput.value = getTrimmedValue(articleInput);
}

export function validatePredictionForm({ headlineInput, articleInput }) {
  const headline = getTrimmedValue(headlineInput);
  const article = getTrimmedValue(articleInput);
  const errors = {};

  if (!headline) {
    errors.headline = 'Enter a news headline.';
  } else if (headline.length > VALIDATION_LIMITS.headlineMaxLength) {
    errors.headline = `Keep the headline within ${VALIDATION_LIMITS.headlineMaxLength} characters.`;
  }

  if (!article) {
    errors.article = 'Enter the news article text.';
  } else if (article.length < VALIDATION_LIMITS.articleMinLength) {
    errors.article = `Use at least ${VALIDATION_LIMITS.articleMinLength} article characters.`;
  } else if (article.length > VALIDATION_LIMITS.articleMaxLength) {
    errors.article = `Keep the article within ${VALIDATION_LIMITS.articleMaxLength.toLocaleString()} characters.`;
  }

  return {
    errors,
    isValid: Object.keys(errors).length === 0,
  };
}
