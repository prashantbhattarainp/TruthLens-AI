const MlServiceClient = require('../clients/ml-service-client');
const config = require('../config/environment');
const { logger } = require('../utils/logger');
const {
  modelMetadataSchema,
  modelReadySchema,
  modelVersionSchema,
} = require('../validators/schemas/model-response-schemas');

const mlServiceClient = new MlServiceClient({
  baseUrl: config.mlServiceUrl,
  startupTimeoutMs: config.modelStartupTimeoutMs,
  retryAttempts: config.mlServiceRetryAttempts,
  retryDelayMs: config.mlServiceRetryDelayMs,
  timeoutMs: config.requestTimeoutMs,
});

async function getModelReady({ requestId }) {
  return requestValidatedModelEndpoint({
    endpoint: 'ready',
    requestId,
    schema: modelReadySchema,
  });
}

async function getModelMetadata({ requestId }) {
  return requestValidatedModelEndpoint({
    endpoint: 'metadata',
    requestId,
    schema: modelMetadataSchema,
  });
}

async function getModelVersion({ requestId }) {
  return requestValidatedModelEndpoint({
    endpoint: 'version',
    requestId,
    schema: modelVersionSchema,
  });
}

async function requestValidatedModelEndpoint({ endpoint, requestId, schema }) {
  const methods = {
    metadata: 'getMetadata',
    ready: 'getReady',
    version: 'getVersion',
  };
  const result = await mlServiceClient[methods[endpoint]]({ requestId });
  if (!result.ok) {
    return result;
  }
  const validation = schema.safeParse(result.data);
  if (!validation.success) {
    logger.warn(
      {
        endpoint,
        event: 'ml_model_response_invalid',
        request_id: requestId,
        validation_issues: validation.error.issues.map((issue) => issue.path.join('.')),
      },
      'ML model endpoint returned an invalid response',
    );
    return {
      error: {
        code: 'ML_SERVICE_INVALID_RESPONSE',
        message: 'ML service returned an invalid model response.',
      },
      ok: false,
    };
  }
  return { data: validation.data, ok: true };
}

module.exports = {
  getModelMetadata,
  getModelReady,
  getModelVersion,
};
