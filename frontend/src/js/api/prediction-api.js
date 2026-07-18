import { requestJson } from './api.js';

export async function requestPrediction({ article, headline }) {
  const response = await requestJson('/api/predict', {
    body: {
      article,
      headline,
    },
    method: 'POST',
  });

  return {
    data: response.data,
    requestId: response.request_id,
    timestamp: response.timestamp,
  };
}
