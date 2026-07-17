function createTimestamp() {
  return new Date().toISOString();
}

function sendSuccess(response, { data, requestId, statusCode = 200 }) {
  return response.status(statusCode).json({
    success: true,
    data,
    timestamp: createTimestamp(),
    request_id: requestId,
  });
}

function sendError(response, { statusCode, code, message, requestId }) {
  return response.status(statusCode).json({
    success: false,
    error: {
      code,
      message,
    },
    timestamp: createTimestamp(),
    request_id: requestId,
  });
}

module.exports = {
  sendError,
  sendSuccess,
};
