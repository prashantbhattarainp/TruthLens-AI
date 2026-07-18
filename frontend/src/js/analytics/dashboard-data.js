export const DASHBOARD_EVIDENCE = Object.freeze({
  dataset: {
    fakeRecords: 3825,
    identifier: 'TL-BFNK-EN-v1.0 / DER-20260718-r2',
    realRecords: 5907,
    validationRecords: 1461,
  },
  model: {
    deploymentStatus: 'Integrated; not deployment approved',
    name: 'LinearSVC with TF-IDF unigram/bigram',
    version: 'TL-LSVM-TFIDF-v1.1.0-rc.1',
  },
  predictionDistribution: {
    fake: 46,
    note: 'Illustrative placeholder only. Prediction history and aggregate retention are not implemented.',
    real: 54,
  },
  research: {
    benchmarkedCandidates: '4 evaluated classical/ensemble candidates',
    explainabilityMethods: 'SHAP + LIME margin explanations',
    publicationStatus: 'Phase 4.6 publication package complete',
    supportedLanguages: 'English evidence only; Hindi/Hinglish not validated',
    trackedRecords: 7,
  },
  xaiFeatures: [
    { feature: 'that', value: 0.0169 },
    { feature: 'Fact', value: 0.0152 },
    { feature: 'Check', value: 0.0143 },
    { feature: 'a', value: 0.0139 },
    { feature: 'being', value: 0.0123 },
    { feature: 'media post', value: 0.0109 },
  ],
});

export const PERFORMANCE_METRICS = Object.freeze({
  accuracy: { label: 'Accuracy', maximum: 0.65, sourceLabel: 'Validation accuracy' },
  fakeRecall: { label: 'FAKE recall', maximum: 0.5, sourceLabel: 'Validation FAKE recall' },
  macroF1: { label: 'Macro F1', maximum: 0.6, sourceLabel: 'Validation Macro F1' },
  rocAuc: { label: 'ROC-AUC', maximum: 0.6, sourceLabel: 'Validation ROC-AUC' },
});

export const PERFORMANCE_SERIES = Object.freeze([
  {
    accuracy: 0.5941,
    fakeRecall: 0.3183,
    label: 'LinearSVC',
    macroF1: 0.5398,
    rocAuc: 0.5576,
  },
  {
    accuracy: 0.5647,
    fakeRecall: 0.4226,
    label: 'MultinomialNB',
    macroF1: 0.5399,
    rocAuc: 0.5652,
  },
  {
    accuracy: 0.5825,
    fakeRecall: 0.3739,
    label: 'Hard vote',
    macroF1: 0.5447,
    rocAuc: 0.5513,
  },
  {
    accuracy: 0.5674,
    fakeRecall: 0.4348,
    label: 'Soft vote',
    macroF1: 0.5443,
    rocAuc: 0.5688,
  },
]);
