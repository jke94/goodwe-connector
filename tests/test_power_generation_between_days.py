from datetime import datetime

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
