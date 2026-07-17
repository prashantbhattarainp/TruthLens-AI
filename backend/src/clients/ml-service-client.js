const { logger } = require('../utils/logger');

function wait(delayMs) {
  return new Promise((resolve) => {
    setTimeout(resolve, delayMs);
  });
}

class MlServiceClient {
  constructor({ baseUrl, timeoutMs, retryAttempts, retryDelayMs, fetchImplementation = fetch }) {
    this.baseUrl = baseUrl;
    this.timeoutMs = timeoutMs;
    this.retryAttempts = retryAttempts;
    this.retryDelayMs = retryDelayMs;
    this.fetchImplementation = fetchImplementation;
  }

  async getHealth({ requestId } = {}) {
    return this.request({
      method: 'GET',
      path: 'health',
      requestId,
    });
  }

  async predict({ article, headline, requestId } = {}) {
    return this.request({
      body: {
        article,
        headline,
      },
      method: 'POST',
      path: 'predict',
      requestId,
    });
  }

  async request({ body, method, path, requestId }) {
    if (!this.baseUrl) {
      logger.warn(
        {
          event: 'ml_service_request_not_configured',
          request_id: requestId,
        },
        'ML service request skipped because no base URL is configured',
      );

      return this.createResult({
        error: {
          code: 'ML_SERVICE_NOT_CONFIGURED',
          message: 'ML service URL is not configured.',
        },
        ok: false,
        responseTimeMs: 0,
      });
    }

    for (let attempt = 1; attempt <= this.retryAttempts; attempt += 1) {
      const result = await this.executeRequest({
        attempt,
        body,
        method,
        path,
        requestId,
      });

      if (result.ok || !result.retryable || attempt === this.retryAttempts) {
        return this.createResult({
          ...result,
          attempts: attempt,
        });
      }

      logger.warn(
        {
          attempt,
          event: 'ml_service_request_retry_scheduled',
          max_attempts: this.retryAttempts,
          request_id: requestId,
          retry_delay_ms: this.retryDelayMs,
        },
        'ML service request will be retried',
      );

      await wait(this.retryDelayMs);
    }

    return this.createResult({
      error: {
        code: 'ML_SERVICE_UNAVAILABLE',
        message: 'ML service could not be reached.',
      },
      ok: false,
      responseTimeMs: 0,
    });
  }

  async executeRequest({ attempt, body, method, path, requestId }) {
    const endpoint = new URL(path, `${this.baseUrl}/`).toString();
    const controller = new AbortController();
    const startedAt = process.hrtime.bigint();
    let timedOut = false;

    const timeout = setTimeout(() => {
      timedOut = true;
      controller.abort();
    }, this.timeoutMs);

    logger.info(
      {
        attempt,
        endpoint,
        event: 'ml_service_request_started',
        method,
        request_id: requestId,
        timeout_ms: this.timeoutMs,
      },
      'ML service request started',
    );

    try {
      const response = await this.fetchImplementation(endpoint, {
        method,
        headers: {
          accept: 'application/json',
          ...(body === undefined ? {} : { 'content-type': 'application/json' }),
          ...(requestId ? { 'x-request-id': requestId } : {}),
        },
        signal: controller.signal,
        ...(body === undefined ? {} : { body: JSON.stringify(body) }),
      });
      const responseTimeMs = this.getResponseTimeMs(startedAt);

      if (!response.ok) {
        logger.warn(
          {
            attempt,
            endpoint,
            event: 'ml_service_request_failed',
            method,
            request_id: requestId,
            response_time_ms: responseTimeMs,
            status_code: response.status,
          },
          'ML service returned an unsuccessful response',
        );

        return {
          data: null,
          error: {
            code: 'ML_SERVICE_HTTP_ERROR',
            message: 'ML service returned an unsuccessful response.',
          },
          ok: false,
          responseTimeMs,
          retryable: response.status >= 500,
        };
      }

      let data;
      try {
        data = await response.json();
      } catch {
        logger.warn(
          {
            attempt,
            endpoint,
            event: 'ml_service_request_failed',
            method,
            reason: 'invalid_json',
            request_id: requestId,
            response_time_ms: responseTimeMs,
            status_code: response.status,
          },
          'ML service returned invalid JSON',
        );

        return {
          data: null,
          error: {
            code: 'ML_SERVICE_INVALID_RESPONSE',
            message: 'ML service returned an invalid response.',
          },
          ok: false,
          responseTimeMs,
          retryable: false,
        };
      }

      logger.info(
        {
          attempt,
          endpoint,
          event: 'ml_service_request_succeeded',
          method,
          request_id: requestId,
          response_time_ms: responseTimeMs,
          status_code: response.status,
        },
        'ML service request succeeded',
      );

      return {
        data,
        error: null,
        ok: true,
        responseTimeMs,
        retryable: false,
      };
    } catch (error) {
      const responseTimeMs = this.getResponseTimeMs(startedAt);
      const code = timedOut ? 'ML_SERVICE_TIMEOUT' : 'ML_SERVICE_UNAVAILABLE';

      logger.warn(
        {
          attempt,
          endpoint,
          error_name: error.name,
          event: timedOut ? 'ml_service_request_timed_out' : 'ml_service_request_failed',
          method,
          request_id: requestId,
          response_time_ms: responseTimeMs,
        },
        timedOut ? 'ML service request timed out' : 'ML service request failed',
      );

      return {
        data: null,
        error: {
          code,
          message: timedOut ? 'ML service request timed out.' : 'ML service could not be reached.',
        },
        ok: false,
        responseTimeMs,
        retryable: true,
      };
    } finally {
      clearTimeout(timeout);
    }
  }

  createResult({ attempts = 1, data = null, error, ok, responseTimeMs }) {
    return {
      attempts,
      data,
      error,
      ok,
      responseTimeMs,
    };
  }

  getResponseTimeMs(startedAt) {
    return Number((Number(process.hrtime.bigint() - startedAt) / 1_000_000).toFixed(2));
  }
}

module.exports = MlServiceClient;
