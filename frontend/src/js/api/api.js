const DEFAULT_TIMEOUT_MS = 8000;

export class ApiError extends Error {
  constructor({ code, message, requestId = null, status = null }) {
    super(message);
    this.name = 'ApiError';
    this.code = code;
    this.requestId = requestId;
    this.status = status;
  }
}

function getRuntimeConfiguration() {
  const runtimeConfig = window.TruthLensConfig ?? {};
  const configuredBaseUrl = runtimeConfig.apiBaseUrl?.trim();
  const apiBaseUrl = (configuredBaseUrl || window.location.origin).replace(/\/$/, '');
  const configuredTimeout = Number(runtimeConfig.apiTimeoutMs);

  return {
    apiBaseUrl,
    timeoutMs:
      Number.isFinite(configuredTimeout) && configuredTimeout > 0
        ? configuredTimeout
        : DEFAULT_TIMEOUT_MS,
  };
}

async function parseResponseBody(response) {
  try {
    return await response.json();
  } catch {
    throw new ApiError({
      code: 'INVALID_RESPONSE',
      message: 'The backend returned an unreadable response.',
      status: response.status,
    });
  }
}

export async function requestJson(path, { body, method = 'GET', timeoutMs } = {}) {
  const runtimeConfiguration = getRuntimeConfiguration();
  const controller = new AbortController();
  const requestTimeoutMs = timeoutMs ?? runtimeConfiguration.timeoutMs;
  let didTimeout = false;
  const timeoutHandle = window.setTimeout(() => {
    didTimeout = true;
    controller.abort();
  }, requestTimeoutMs);

  try {
    const response = await fetch(`${runtimeConfiguration.apiBaseUrl}${path}`, {
      body: body === undefined ? undefined : JSON.stringify(body),
      headers: {
        Accept: 'application/json',
        ...(body === undefined ? {} : { 'Content-Type': 'application/json' }),
      },
      method,
      signal: controller.signal,
    });
    const responseBody = await parseResponseBody(response);

    if (!response.ok || responseBody.success !== true) {
      throw new ApiError({
        code: responseBody.error?.code ?? 'BACKEND_ERROR',
        message: responseBody.error?.message ?? 'The backend could not complete the request.',
        requestId: responseBody.request_id ?? null,
        status: response.status,
      });
    }

    return responseBody;
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }

    if (didTimeout || error.name === 'AbortError') {
      throw new ApiError({
        code: 'REQUEST_TIMEOUT',
        message: 'The backend took too long to respond.',
      });
    }

    throw new ApiError({
      code: 'NETWORK_ERROR',
      message: 'The backend could not be reached.',
    });
  } finally {
    window.clearTimeout(timeoutHandle);
  }
}
