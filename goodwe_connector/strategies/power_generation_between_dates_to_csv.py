from goodwe_connector.goodwe_api import GoodweApi
from goodwe_connector.strategy import Strategy
from datetime import datetime

class PowerGenerationBetweenDaysToCsv(Strategy):

    def __init__(self, 
                 start_date:datetime, 
                 end_date:datetime, 
                 file_name:str,
                 show_info:bool = False
                 ) -> None:
        
        self.__start_date = start_date
        self.__end_date = end_date
        self.__file_name = file_name
        self.__show_info = show_info

    def do_algorithm(self, goodwe:GoodweApi) -> dict:
        
        data = goodwe.get_power_generation_between_dates_to_csv(
            start_date=self.__start_date,
            end_date=self.__end_date,
            file_name=self.__file_name,
            show_info=self.__show_info
        )
        
        return data