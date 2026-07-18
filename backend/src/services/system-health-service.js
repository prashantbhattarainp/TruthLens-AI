const MlServiceClient = require('../clients/ml-service-client');
const config = require('../config/environment');

const mlServiceClient = new MlServiceClient({
  baseUrl: config.mlServiceUrl,
  startupTimeoutMs: config.modelStartupTimeoutMs,
  retryAttempts: config.mlServiceRetryAttempts,
  retryDelayMs: config.mlServiceRetryDelayMs,
  timeoutMs: config.requestTimeoutMs,
});

function getBackendHealth() {
  return {
    status: 'healthy',
    version: config.version,
  };
}

function isValidMlHealthResponse(mlHealth) {
  return (
    typeof mlHealth.data?.status === 'string' && typeof mlHealth.data?.model_loaded === 'boolean'
  );
}

async function getSystemHealth({ requestId }) {
  const backend = getBackendHealth();
  const mlHealth = await mlServiceClient.getHealth({
    requestId,
  });

  if (!mlHealth.ok) {
    return {
      ok: false,
      backend,
      error: mlHealth.error,
    };
  }

  if (!isValidMlHealthResponse(mlHealth)) {
    return {
      ok: false,
      backend,
      error: {
        code: 'ML_SERVICE_INVALID_RESPONSE',
        message: 'ML service returned an invalid health response.',
      },
    };
  }

  return {
    ok: true,
    backend,
    mlService: {
      status: mlHealth.data.status,
      model_loaded: mlHealth.data.model_loaded,
    },
  };
}

module.exports = {
  getSystemHealth,
};
