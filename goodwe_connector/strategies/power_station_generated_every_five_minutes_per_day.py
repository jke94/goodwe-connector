from goodwe_connector.goodwe_api import GoodweApi
from goodwe_connector.strategy import Strategy
from datetime import datetime

class PowerStationGeneratedEveryFiveMinutesPerDay(Strategy):
    
    def __init__(self, date:datetime) -> None:
        
        self.__date = date    

    def do_algorithm(self, goodwe:GoodweApi) -> dict:
        
        data = goodwe.get_power_station_generated_every_five_minutes_per_day(self.__date)
        
        return data
    