from datetime import datetime

from goodwe_connector.goodwe_context import GoodweContext
from goodwe_connector.strategies.power_station_generated_every_five_minutes_per_day import PowerStationGeneratedEveryFiveMinutesPerDay


class FakeGoodweApi:
    def __init__(self):
        self.calls = []

    def get_power_station_generated_every_five_minutes_per_day(self, date):
        self.calls.append(("five_minutes", date))
        return {"2024-01-01 00:00:00": 1}


def test_power_station_generated_every_five_minutes_strategy_delegates_to_api():
    # Arrange
    api = FakeGoodweApi()
    strategy = PowerStationGeneratedEveryFiveMinutesPerDay(datetime(2024, 1, 1))
    context = GoodweContext(goodwe_api=api, strategy=strategy)

    # Act
    result = context.process()

    # Assert
    assert result == {"2024-01-01 00:00:00": 1}
    assert api.calls[0][0] == "five_minutes"
