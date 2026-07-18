import { requestJson } from './api.js';

function outcomeData(outcome) {
  return outcome.status === 'fulfilled' ? outcome.value.data : null;
}

function outcomeMessage(outcome) {
  if (outcome.status === 'fulfilled') {
    return null;
  }

  return outcome.reason?.code ?? 'Unavailable';
}

export async function getOperationalSnapshot() {
  const [apiHealth, systemHealth, modelReady, modelVersion] = await Promise.allSettled([
    requestJson('/api/health'),
    requestJson('/api/system/health'),
    requestJson('/api/model/ready'),
    requestJson('/api/model/version'),
  ]);
  const api = outcomeData(apiHealth);
  const system = outcomeData(systemHealth);
  const ready = outcomeData(modelReady);
  const version = outcomeData(modelVersion);

  return {
    api: {
      detail: api ? `Version ${api.version}` : outcomeMessage(apiHealth),
      state: api?.status === 'healthy' ? 'healthy' : 'unavailable',
    },
    model: {
      deploymentStatus: version?.deployment_status ?? null,
      detail: ready?.model_version ?? outcomeMessage(modelReady),
      state: ready?.status === 'ready' ? 'healthy' : 'unavailable',
      version: version?.model_version ?? ready?.model_version ?? null,
    },
    mlService: {
      detail: system?.ml_service?.model_loaded ? 'Healthy; model loaded' : outcomeMessage(systemHealth),
      state: system?.ml_service?.status === 'healthy' ? 'healthy' : 'unavailable',
    },
  };
}
