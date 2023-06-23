from datetime import datetime
from datetime import timedelta
from json import JSONDecodeError
from goodwe_connector.goodwe_auth.goodwe_api_authorization import GoodweApiAuth
from goodwe_connector.goodwe_api_controller.v2.power_station import GetPowerStationPowerAndIncomeByDay
from goodwe_connector.goodwe_api_controller.v0.power_station_monitor import GetPowerStationPacByDayForApp
from goodwe_connector.goodwe_api_methods import GetPowerStationMonitorDetail
from goodwe_connector.goodwe_api_methods import GetGetPowerStationStatus
from goodwe_connector.goodwe_api_methods import GetStatPowerStationKPI
from goodwe_connector.goodwe_api_methods import GetQueryPowerStationMonitor
from goodwe_connector.goodwe_api_methods import PowerStation_GetPowerStationTips
from goodwe_connector.goodwe_api_methods import PowerStationGetUserInfoByPowerStation
from goodwe_connector.goodwe_api_methods import StatGetPowerStationAndPowerTotal
from goodwe_connector.goodwe_api_methods import HistoryDataQueryPowerStationByHistory
from goodwe_connector.goodwe_api_methods import HistoryDataQueryPowerStationByHistoryForDaily
from goodwe_connector.goodwe_api_methods import PowerStationV1GetPowerCharts
from goodwe_connector.goodwe_api_methods import PowerStationV1GetEnergeStatisticsCharts
from goodwe_connector.goodwe_api_methods import ReportDataV1GetPowerStationPowerReportDetialByMonth

import requests
from requests.exceptions import RequestException

class GoodweApi(GoodweApiAuth):
    """_summary_
    """

    def __init__(self,
                 system_id:str, 
                 account:str, 
                 password:str, 
                 logging=False) -> None:
        
        self.__n_max_request_retry = 5
        
        super().__init__(system_id, account, password,logging)

    def __call(self, url, payload) -> dict:
        
        try:
            
            if not self._authorization():
                return None
            
            headers = {
                'User-Agent': 'SEMS Portal/3.1 (iPhone; iOS 13.5.1; Scale/2.00)',
                'Token': self._credentials,
            }
            
            request = requests.post(
                self.base_url + url, 
                headers=headers, 
                data=payload, 
                timeout=10)
            
            request.raise_for_status()
            
            self._logger.info(f'Method request elapsed seconds: {request.elapsed}')
            
            data = request.json()
            request.close()
            
            return data['data']
        
        except JSONDecodeError as json_decoder_error:
            self._logger.warning(f'{json_decoder_error}')
            return None

        except RequestException as e:
            self._logger.warning(f'{e}')
            return None

    def get_power_generation_per_day(self, date:datetime) -> dict:
        """_summary_

        Args:
            date (datetime): _description_

        Returns:
            float: _description_
        """
        
        payload = {
            'powerstation_id' : self.system_id,
            'date' : date.strftime('%Y-%m-%d')
        }
        
        generation = {}
        count_request = 0
        data = {}
        
        while(not data and count_request < self.__n_max_request_retry):
        
            count_request += 1
            method = GetPowerStationPowerAndIncomeByDay
            data = self.__call(method, payload)
        
            if not data:
                self._logger.warning(f'Request count={count_request}, Method: {method}, missing data.')

        # Parsing data to extract the correct day.
        for day in data:
            if day['d'] == date.strftime('%m/%d/%Y'):
                
                Key_date = date.strftime('%Y-%m-%d')
                value = day['p']
                
                generation[Key_date] = value
                
                return generation

        return generation
    
    def get_power_generation_between_dates(self, 
                                           start_date:datetime, 
                                           end_date:datetime) -> dict:
        generation = {}
        
        delta = timedelta(days=1)

        while start_date <= end_date:
            
            payload = {
                'powerstation_id' : self.system_id,
                'date' : start_date.strftime('%Y-%m-%d')
            }
            
            count_request = 0
            data = {}
            
            while(not data and count_request < self.__n_max_request_retry):
            
                count_request += 1
                method = GetPowerStationPowerAndIncomeByDay
                data = self.__call(method, payload)
            
                if not data:
                    self._logger.warning(f'Request count={count_request}, Method: {method}, missing data.')

            # Parsing data and extracting day.
            for day in data:
                if day['d'] == start_date.strftime('%m/%d/%Y'):
                    generation[start_date.strftime('%Y-%m-%d')] = day['p']
            
            start_date += delta
            count_request = 0
            data = {}
            
        return generation
    
    def get_power_station_generated_every_five_minutes_per_day(self, date:datetime) -> dict:
        
        day_powers = {} 
        
        day = date.strftime('%Y-%m-%d')
        
        payload = {
            'id' : self.system_id,
            'date' : day
        }
        
        count_request = 0
        data = {}
        
        while(not data and count_request < self.__n_max_request_retry):
        
            count_request += 1
            method = GetPowerStationPacByDayForApp
            data = self.__call(method, payload)
        
            if not data:
                self._logger.warning(f'Request count={count_request}, Method: {method}, missing data.')
                
        if (not data or "pacs" not in data or not data['pacs']):
            
            day_powers['NO_DATA'] = 0
            
            return day_powers
        
        for item in data['pacs']:
                      
            aux_date = date.strptime(item['date'], '%m/%d/%Y %H:%M:%S')
            key_day = aux_date.strftime('%Y-%m-%d %H:%M:%S')
            
            day_powers[key_day] = int(item['pac'])
        
        return day_powers
    
    def get_power_station_monitor_detail(self, year:int, month:int) -> dict:
        
        data_returned = {} 
        
        if year < 0 or month < 1 or month > 12:
            print(f'Error! Month: {month}. Year: {year}')
            return data_returned
                
        print(f'Month : {month} | Year: {year}')
        
        date = datetime(year=year, month=month, day=1)
        date_str = date.strftime("%Y-%m-%d")
        
        payload = {
            # "date": "2023-04-1",
            'date' : date_str,
            "is_report": 2,
            "page_index": 1,
            "page_size": 5
        }
        
        count_request = 0
        data = {}
        
        while(not data and count_request < self.__n_max_request_retry):
        
            count_request += 1
            method = ReportDataV1GetPowerStationPowerReportDetialByMonth
            data = self.__call(method, payload)
        
            if not data:
                self._logger.warning(f'Request count={count_request}, Method: {method}, missing data.')
        
        if (not data):
            
            data_returned['NO_DATA'] = 0
            
            return data_returned
        
        power_stations_info = []
        
        # print(json.dumps(data, indent=2))
        
        for item in data['list']:
            power_stations_info.append({
                'PowerStationId': item['pw_id'],
                'PowerStationOwnerId': item['owner_id'],
                'PowerStationInformation' :  item['pw_name'],
                'PowerStationAddress' :  item['address'],
                'PowerStationKwCapacity' :  item['capacity'],
                'PowerStationMonthPower' :  item['month_power'],
                'PowerStationTotalPower' :  item['total_power'],
                'ContactEmail' :  item['email'],
            })
        
        return power_stations_info