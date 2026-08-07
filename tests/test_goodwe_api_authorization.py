from goodwe_connector.goodwe_auth.goodwe_api_authorization import GoodweApiAuth


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

    def post(self, url, payload=None, headers=None, timeout=10):
        self.calls.append({"url": url, "payload": payload, "headers": headers, "timeout": timeout})
        return self.response


def test_goodwe_api_auth_uses_injected_http_transport():
    # Arrange
    transport = FakeHttpTransport(FakeResponse({"api": "https://example.test", "data": {"token": "abc"}}))

    # Act
    auth = GoodweApiAuth("system-1", "account", "password", logging=False, http_client=transport)
    result = auth._authorization()

    # Assert
    assert result is True
    assert auth.base_url == "https://example.test"
    assert auth._credentials == '{"token": "abc"}'
    assert transport.calls
