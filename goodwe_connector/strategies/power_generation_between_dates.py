from goodwe_connector.goodwe_api import GoodweApi
from goodwe_connector.strategy import Strategy
from datetime import datetime

class PowerGenerationBetweenDays(Strategy):

    def __init__(self, start_date:datetime, end_date:datetime) -> None:
        
        self.__start_date = start_date
        self.__end_date = end_date

    def do_algorithm(self, goodwe:GoodweApi) -> dict:
        
        data = goodwe.get_power_generation_between_dates(
            start_date=self.__start_date,
            end_date=self.__end_date
        )
        
        return data