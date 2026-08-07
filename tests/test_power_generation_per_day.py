from datetime import datetime

from goodwe_connector.strategies.power_generation_per_day import PowerGenerationPerDay
from goodwe_connector.goodwe_context import GoodweContext


class FakeGoodweApi:
    def __init__(self):
        self.calls = []

    def get_power_generation_per_day(self, date):
        self.calls.append(("per_day", date))
        return {date.strftime("%Y-%m-%d"): 7.5}


def test_power_generation_per_day_strategy_delegates_to_api():
    # Arrange
    api = FakeGoodweApi()
    strategy = PowerGenerationPerDay(datetime(2024, 1, 2))
    context = GoodweContext(goodwe_api=api, strategy=strategy)

    # Act
    result = context.process()

    # Assert
    assert result == {"2024-01-02": 7.5}
    assert api.calls[0][0] == "per_day"
