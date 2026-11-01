import base64
import hashlib
import json

from goodwe_connector.goodwe_auth.goodwe_api_authorization import GoodweApiAuth
from goodwe_connector.goodwe_constants import GOODWE_SEMS_PLUS_LOGIN_URL


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload
        self.elapsed = 0

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload

    def close(self):
        return None


class FakeHttpTransport:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def post(self, url, payload=None, headers=None, timeout=10, *, json_body=False):
        self.calls.append({
            "url": url,
            "payload": payload,
            "headers": headers,
            "timeout": timeout,
            "json_body": json_body,
        })
        return self.response


def test_goodwe_api_auth_uses_injected_http_transport():
    # Arrange
    transport = FakeHttpTransport(
        FakeResponse({
            "code": "0",
            "api": "https://example.test/web/sems",
            "data": {"uid": "user-1", "token": "abc"},
        })
    )

    # Act
    auth = GoodweApiAuth("system-1", "account", "password", logging=False, http_client=transport)
    result = auth._authorization()

    # Assert
    assert result is True
    assert auth.base_url == "https://example.test/web/sems"
    assert auth._credentials == '{"uid":"user-1","token":"abc"}'
    call = transport.calls[0]
    assert call["url"] == GOODWE_SEMS_PLUS_LOGIN_URL
    assert call["json_body"] is True
    expected_password = hashlib.md5(
        b"password", usedforsecurity=False
    ).hexdigest().encode()
    assert call["payload"] == {
        "account": "account",
        "pwd": base64.b64encode(expected_password).decode(),
        "agreement": 1,
        "isChinese": False,
        "isLocal": False,
    }
    assert json.loads(call["headers"]["Token"]) == {
        "uid": "",
        "timestamp": 0,
        "token": "",
        "client": "semsPlusWeb",
        "version": "",
        "language": "en",
    }
    assert call["headers"]["X-Signature"]


def test_goodwe_api_auth_rejects_unsuccessful_sems_plus_response():
    transport = FakeHttpTransport(
        FakeResponse({"code": 100005, "msg": "Email or password error.", "data": None})
    )
    auth = GoodweApiAuth("system-1", "account", "password", http_client=transport)

    assert auth._authorization() is False
