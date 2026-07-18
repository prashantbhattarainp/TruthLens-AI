#!/usr/bin/env python3
"""Run a non-sensitive HTTP smoke test against a locally started TruthLens RC stack."""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class CheckResult:
    endpoint: str
    latency_ms: float
    status_code: int


def request_json(base_url: str, path: str, *, payload: dict[str, Any] | None = None) -> tuple[int, dict[str, Any], float]:
    body = json.dumps(payload).encode('utf-8') if payload is not None else None
    request = Request(
        f'{base_url.rstrip("/")}{path}',
        data=body,
        headers={'Accept': 'application/json', **({'Content-Type': 'application/json'} if body else {})},
        method='POST' if body else 'GET',
    )
    started_at = time.perf_counter()
    try:
        with urlopen(request, timeout=20) as response:  # noqa: S310 - caller controls a local RC URL.
            response_body = json.loads(response.read().decode('utf-8'))
            return response.status, response_body, round((time.perf_counter() - started_at) * 1000, 2)
    except HTTPError as error:
        response_body = json.loads(error.read().decode('utf-8'))
        return error.code, response_body, round((time.perf_counter() - started_at) * 1000, 2)
    except URLError as error:
        raise RuntimeError(f'{path}: backend could not be reached ({error.reason}).') from error


def require_success(path: str, status_code: int, body: dict[str, Any], latency_ms: float) -> CheckResult:
    if status_code != 200 or body.get('success') is not True:
        error = body.get('error', {}).get('code', 'UNKNOWN')
        raise RuntimeError(f'{path}: expected a successful 200 response, got {status_code} ({error}).')
    return CheckResult(endpoint=path, latency_ms=latency_ms, status_code=status_code)


def run_verification(base_url: str) -> list[CheckResult]:
    checks: list[CheckResult] = []
    for path in ('/api/health', '/api/system/health', '/api/model/ready', '/api/model/version', '/api/model/metadata'):
        status_code, body, latency_ms = request_json(base_url, path)
        checks.append(require_success(path, status_code, body, latency_ms))

    status_code, body, latency_ms = request_json(
        base_url,
        '/api/predict',
        payload={
            'headline': 'Release-candidate synthetic validation input',
            'article': (
                'This synthetic release-candidate request exists only to verify the approved local integration path. '
                'It contains no personal data, no external claim, and no evidence that should be retained or interpreted.'
            ),
        },
    )
    checks.append(require_success('/api/predict', status_code, body, latency_ms))

    prediction = body['data']
    if prediction.get('confidence') is not None or prediction.get('confidence_status') != 'unavailable':
        raise RuntimeError('/api/predict: confidence boundary was not preserved.')
    if prediction.get('risk_level') != 'not_assessed':
        raise RuntimeError('/api/predict: risk boundary was not preserved.')
    if prediction.get('model_version') != 'TL-LSVM-TFIDF-v1.1.0-rc.1':
        raise RuntimeError('/api/predict: unexpected model version returned.')
    if prediction.get('explainability', {}).get('metadata', {}).get('status') not in {'available', 'unavailable'}:
        raise RuntimeError('/api/predict: explainability metadata did not use the documented contract.')

    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--backend-url', default='http://127.0.0.1:3000', help='Local Node public API base URL.')
    arguments = parser.parse_args()

    try:
        checks = run_verification(arguments.backend_url)
    except RuntimeError as error:
        print(f'RC verification failed: {error}', file=sys.stderr)
        return 1

    print('TruthLens RC HTTP verification passed.')
    for check in checks:
        print(f'- {check.endpoint}: HTTP {check.status_code} in {check.latency_ms:.2f} ms')
    print('Research boundary preserved: confidence unavailable; risk not assessed; internal candidate only.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
