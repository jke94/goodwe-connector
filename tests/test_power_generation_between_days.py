from datetime import datetime

import pytest

from goodwe_connector.goodwe_api import GoodweApi
from goodwe_connector.data_transformers import parse_generation_series
from goodwe_connector.goodwe_context import GoodweContext
from goodwe_connector.strategies.power_generation_between_dates import PowerGenerationBetweenDays


class FakeGoodweApi:
    def __init__(self):
        self.calls = []

    def get_power_generation_between_dates(self, start_date, end_date):
        self.calls.append(("between_dates", start_date, end_date))
        return {"2024-01-01": 5.0, "2024-01-02": 6.0}


def test_power_generation_between_days_strategy_delegates_to_api():
    # Arrange
    api = FakeGoodweApi()
    strategy = PowerGenerationBetweenDays(datetime(2024, 1, 1), datetime(2024, 1, 2))
    context = GoodweContext(goodwe_api=api, strategy=strategy)

    # Act
    result = context.process()

    # Assert
    assert result == {"2024-01-01": 5.0, "2024-01-02": 6.0}
    assert api.calls[0][0] == "between_dates"


def test_parse_generation_series_returns_all_days_in_the_range():
    data = [
        {"d": "01/01/2024", "p": 5.0},
        {"d": "01/02/2024", "p": 6.0},
    ]

    result = parse_generation_series(data, datetime(2024, 1, 1), datetime(2024, 1, 2))

    assert result == {"2024-01-01": 5.0, "2024-01-02": 6.0}


def test_api_batches_daily_generation_requests_for_the_full_range():
    class StubGoodweApi(GoodweApi):
        def __init__(self):
            super().__init__("system-id", "account", "password")
            self.calls = []

        def _GoodweApi__call(self, url, payload):
            self.calls.append((url, payload))
            return [
                {"d": "01/01/2024", "p": 5.0},
                {"d": "01/02/2024", "p": 6.0},
            ]

    api = StubGoodweApi()

    result = api.get_power_generation_between_dates(datetime(2024, 1, 1), datetime(2024, 1, 2))

    assert result == {"2024-01-01": 5.0, "2024-01-02": 6.0}
    assert len(api.calls) == 1
    assert api.calls[0][0] == "/sems-plant/api/stations/statistics"
    assert api.calls[0][1] == {
        "stationId": "system-id",
        "isReport": False,
        "items": ["proSystemTotalStats"],
        "dimension": "day",
        "startTime": "2024-01-01 00:00:00",
        "endTime": "2024-01-02 23:59:59",
    }


def test_api_maps_sems_plus_daily_statistics_to_generation_series():
    class StubGoodweApi(GoodweApi):
        def __init__(self):
            super().__init__("station-1", "account", "password")

        def _GoodweApi__call(self, url, payload):
            return {
                "dataList": [
                    {
                        "item": "proSystemTotalStats",
                        "statisticsList": [
                            {"date": "2024-01-01T00:00:00", "val": 5.0},
                            {"date": "2024-01-02T00:00:00", "val": "6.25"},
                        ],
                    }
                ]
            }

    api = StubGoodweApi()

    result = api.get_power_generation_between_dates(
        datetime(2024, 1, 1), datetime(2024, 1, 2)
    )

    assert result == {"2024-01-01": 5.0, "2024-01-02": 6.25}


def test_daily_generation_does_not_pass_none_to_the_parser():
    class FailedGoodweApi(GoodweApi):
        def __init__(self):
            super().__init__("station-1", "account", "password")

        def _GoodweApi__call(self, url, payload):
            return None

    api = FailedGoodweApi()

    with pytest.raises(RuntimeError, match="SEMS\\+ daily generation request"):
        api.get_power_generation_between_dates(
            datetime(2024, 1, 1), datetime(2024, 1, 1)
        )


def test_daily_generation_uses_sems_plus_login_and_signed_statistics_request():
    class FakeResponse:
        elapsed = 0

        def __init__(self, body):
            self.body = body

        def raise_for_status(self):
            return None

        def json(self):
            return self.body

        def close(self):
            return None

    class FakeHttpClient:
        def __init__(self):
            self.responses = [
                FakeResponse({
                    "code": "0",
                    "api": "https://gateway.example/web/sems",
                    "data": {"uid": "user-1", "token": "token-1"},
                }),
                FakeResponse({
                    "code": "0",
                    "data": {
                        "dataList": [
                            {
                                "item": "proSystemTotalStats",
                                "statisticsList": [
                                    {"date": "2024-01-01T00:00:00", "val": 5.0}
                                ],
                            }
                        ]
                    },
                }),
            ]
            self.calls = []

        def post(self, url, payload=None, headers=None, timeout=10, *, json_body=False):
            self.calls.append({
                "url": url,
                "payload": payload,
                "headers": headers,
                "json_body": json_body,
            })
            return self.responses.pop(0)

    client = FakeHttpClient()
    api = GoodweApi("station-1", "account", "password", http_client=client)

    result = api.get_power_generation_between_dates(
        datetime(2024, 1, 1), datetime(2024, 1, 1)
    )

    assert result == {"2024-01-01": 5.0}
    assert client.calls[0]["json_body"] is True
    assert client.calls[1]["url"] == (
        "https://gateway.example/web/sems/sems-plant/api/stations/statistics"
    )
    assert client.calls[1]["json_body"] is True
    assert client.calls[1]["headers"]["X-Signature"]
