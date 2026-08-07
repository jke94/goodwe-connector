from goodwe_connector.goodwe_context import GoodweContext
from goodwe_connector.strategies.power_station_monitor_detail import PowerStationMonitorDetail


class FakeGoodweApi:
    def __init__(self):
        self.calls = []

    def get_power_station_monitor_detail(self, year, month):
        self.calls.append(("monitor_detail", year, month))
        return {"year": year, "month": month}


def test_power_station_monitor_detail_strategy_delegates_to_api():
    # Arrange
    api = FakeGoodweApi()
    strategy = PowerStationMonitorDetail(2024, 2)
    context = GoodweContext(goodwe_api=api, strategy=strategy)

    # Act
    result = context.process()

    # Assert
    assert result == {"year": 2024, "month": 2}
    assert api.calls[0][0] == "monitor_detail"
