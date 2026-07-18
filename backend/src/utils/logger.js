const pino = require('pino');
const pinoHttp = require('pino-http');

const config = require('../config/environment');

const logger = pino({
  level: config.logLevel,
  base: {
    service: 'truthlens-backend',
    environment: config.environment,
  },
  redact: ['req.headers.authorization', 'req.headers.cookie'],
  timestamp: pino.stdTimeFunctions.isoTime,
});

function createHttpLogger() {
  return pinoHttp({
    logger,
    autoLogging: false,
    genReqId: (request) => request.requestId,
    serializers: {
      req: (request) => ({
        id: request.id,
        method: request.method,
        url: request.url,
      }),
    },
  });
}

function getRequestLogger(request) {
  return request.log ?? logger;
}

module.exports = {
  createHttpLogger,
  getRequestLogger,
  logger,
};
