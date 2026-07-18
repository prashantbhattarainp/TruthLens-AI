const path = require('node:path');

const dotenv = require('dotenv');

dotenv.config({
  path: path.resolve(__dirname, '../../.env'),
  quiet: true,
});

const supportedLogLevels = new Set(['fatal', 'error', 'warn', 'info', 'debug', 'trace', 'silent']);

function requireEnvironment(name) {
  const value = process.env[name]?.trim();

  if (!value) {
    throw new Error(`${name} must be configured in the environment.`);
  }

  return value;
}

function parseInteger(name, value, minimum) {
  const parsedValue = Number.parseInt(value, 10);

  if (!Number.isInteger(parsedValue) || parsedValue < minimum) {
    throw new Error(`${name} must be an integer greater than or equal to ${minimum}.`);
  }

  return parsedValue;
}

function parsePort(value) {
  const port = parseInteger('PORT', value, 1);

  if (port > 65535) {
    throw new Error('PORT must be less than or equal to 65535.');
  }

  return port;
}

function parseServiceUrl(value) {
  try {
    return new URL(value).toString().replace(/\/$/, '');
  } catch {
    throw new Error('ML_SERVICE_URL must be a valid URL.');
  }
}

function parseAllowedOrigins(value) {
  const origins = value
    .split(',')
    .map((origin) => origin.trim())
    .filter(Boolean);

  if (origins.length === 0) {
    throw new Error('CORS_ALLOWED_ORIGINS must include at least one origin.');
  }

  const normalizedOrigins = origins.map((origin) => {
    try {
      return new URL(origin).origin;
    } catch {
      throw new Error('CORS_ALLOWED_ORIGINS must contain valid origins.');
    }
  });

  return Object.freeze([...new Set(normalizedOrigins)]);
}

function parseLogLevel(value) {
  const logLevel = value.toLowerCase();

  if (!supportedLogLevels.has(logLevel)) {
    throw new Error('LOG_LEVEL must be a supported Pino log level.');
  }

  return logLevel;
}

module.exports = Object.freeze({
  environment: requireEnvironment('NODE_ENV'),
  corsAllowedOrigins: parseAllowedOrigins(requireEnvironment('CORS_ALLOWED_ORIGINS')),
  host: requireEnvironment('HOST'),
  port: parsePort(requireEnvironment('PORT')),
  mlServiceUrl: parseServiceUrl(requireEnvironment('ML_SERVICE_URL')),
  requestTimeoutMs: parseInteger('REQUEST_TIMEOUT_MS', requireEnvironment('REQUEST_TIMEOUT_MS'), 1),
  modelStartupTimeoutMs: parseInteger(
    'MODEL_STARTUP_TIMEOUT_MS',
    requireEnvironment('MODEL_STARTUP_TIMEOUT_MS'),
    1,
  ),
  mlServiceRetryAttempts: parseInteger(
    'ML_SERVICE_RETRY_ATTEMPTS',
    requireEnvironment('ML_SERVICE_RETRY_ATTEMPTS'),
    1,
  ),
  mlServiceRetryDelayMs: parseInteger(
    'ML_SERVICE_RETRY_DELAY_MS',
    requireEnvironment('ML_SERVICE_RETRY_DELAY_MS'),
    0,
  ),
  requestBodyLimit: requireEnvironment('REQUEST_BODY_LIMIT'),
  shutdownTimeoutMs: parseInteger(
    'SHUTDOWN_TIMEOUT_MS',
    requireEnvironment('SHUTDOWN_TIMEOUT_MS'),
    1,
  ),
  logLevel: parseLogLevel(requireEnvironment('LOG_LEVEL')),
  serviceName: requireEnvironment('BACKEND_SERVICE_NAME'),
  version: requireEnvironment('SERVICE_VERSION'),
});
