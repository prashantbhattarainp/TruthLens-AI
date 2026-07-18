import { requestJson } from './api.js';

function outcomeData(outcome) {
  return outcome.status === 'fulfilled' ? outcome.value.data : null;
}

function outcomeMessage(outcome) {
  return outcome.status === 'fulfilled' ? null : outcome.reason?.code ?? 'Unavailable';
}

export async function getOperationalSnapshot() {
  const [apiHealth, systemHealth] = await Promise.allSettled([
    requestJson('/api/health'),
    requestJson('/api/system/health'),
  ]);
  const api = outcomeData(apiHealth);
  const system = outcomeData(systemHealth);

  return {
    api: { detail: api ? `Version ${api.version}` : outcomeMessage(apiHealth), state: api?.status === 'healthy' ? 'healthy' : 'unavailable' },
    mlService: { detail: system?.ml_service?.model_loaded ? 'Available' : outcomeMessage(systemHealth), state: system?.ml_service?.status === 'healthy' ? 'healthy' : 'unavailable' },
  };
}
