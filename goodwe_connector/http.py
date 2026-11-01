from __future__ import annotations

from typing import Any, Protocol

import requests


class HttpClient(Protocol):
    def post(
        self,
        url: str,
        payload: Any = None,
        headers: Any = None,
        timeout: int = 10,
        *,
        json_body: bool = False,
    ):
        ...


class RequestsHttpClient:
    def post(
        self,
        url: str,
        payload: Any = None,
        headers: Any = None,
        timeout: int = 10,
        *,
        json_body: bool = False,
    ):
        body = {"json": payload} if json_body else {"data": payload}
        return requests.post(url, headers=headers, timeout=timeout, **body)
