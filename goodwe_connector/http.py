from __future__ import annotations

from typing import Any, Protocol

import requests


class HttpClient(Protocol):
    def post(self, url: str, payload: Any = None, headers: Any = None, timeout: int = 10):
        ...


class RequestsHttpClient:
    def post(self, url: str, payload: Any = None, headers: Any = None, timeout: int = 10):
        return requests.post(url, data=payload, headers=headers, timeout=timeout)
