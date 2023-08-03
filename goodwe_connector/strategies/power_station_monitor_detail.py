from goodwe_connector.goodwe_api import GoodweApi
from goodwe_connector.strategy import Strategy

class PowerStationMonitorDetail(Strategy):

    def __init__(self, 
                 year:int, 
                 month:int
                 ) -> None:
        
        self.__year = year
        self.__month = month

    def do_algorithm(self, goodweapi:GoodweApi) -> dict:
                
        data = goodweapi.get_power_station_monitor_detail(
            year=self.__year, 
            month=self.__month)
        
        return data