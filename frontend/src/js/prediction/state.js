export const PREDICTION_STATUS = Object.freeze({
  COMPLETE: 'complete',
  ERROR: 'error',
  IDLE: 'idle',
  LOADING: 'loading',
});

export function createPredictionState() {
  return {
    response: null,
    status: PREDICTION_STATUS.IDLE,
    touchedFields: new Set(),
  };
}

export function setPredictionResponse(state, response) {
  state.response = response;
}

export function setPredictionStatus(state, status) {
  state.status = status;
}

export function resetPredictionState(state) {
  state.response = null;
  state.status = PREDICTION_STATUS.IDLE;
  state.touchedFields.clear();
}
