from datetime import datetime

from goodwe_connector.goodwe_context import GoodweContext
from goodwe_connector.strategies.power_generation_between_dates_to_csv import PowerGenerationBetweenDaysToCsv


class FakeGoodweApi:
    def __init__(self):
        self.calls = []

    def get_power_generation_between_dates_to_csv(self, start_date, end_date, file_name, show_info=True):
        self.calls.append(("csv", start_date, end_date, file_name, show_info))
        return {"status": "ok"}


def test_power_generation_between_dates_to_csv_strategy_delegates_to_api_with_show_info_flag():
    # Arrange
    api = FakeGoodweApi()
    strategy = PowerGenerationBetweenDaysToCsv(datetime(2024, 1, 1), datetime(2024, 1, 2), "out.csv", show_info=True)
    context = GoodweContext(goodwe_api=api, strategy=strategy)

    # Act
    result = context.process()

    # Assert
    assert result == {"status": "ok"}
    assert api.calls[0][0] == "csv"
    assert api.calls[0][4] is True
