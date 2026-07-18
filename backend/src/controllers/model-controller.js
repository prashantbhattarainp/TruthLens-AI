const { getModelMetadata, getModelReady, getModelVersion } = require('../services/model-service');
const AppError = require('../utils/app-error');
const { sendSuccess } = require('../utils/api-response');

function statusCodeForModelError(code) {
  if (code === 'ML_SERVICE_TIMEOUT') {
    return 504;
  }
  if (code === 'ML_SERVICE_INVALID_RESPONSE' || code === 'ML_SERVICE_HTTP_ERROR') {
    return 502;
  }
  return 503;
}

function createHandler(serviceFunction) {
  return async (request, response, next) => {
    try {
      const result = await serviceFunction({ requestId: request.requestId });
      if (!result.ok) {
        return next(new AppError({
          statusCode: statusCodeForModelError(result.error.code),
          code: result.error.code,
          message: result.error.message,
        }));
      }
      return sendSuccess(response, { data: result.data, requestId: request.requestId });
    } catch (error) {
      return next(error);
    }
  };
}

module.exports = {
  getModelMetadata: createHandler(getModelMetadata),
  getModelReady: createHandler(getModelReady),
  getModelVersion: createHandler(getModelVersion),
};
