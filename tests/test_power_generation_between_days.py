from datetime import datetime

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
    assert api.calls[0][1]["count"] == 2
