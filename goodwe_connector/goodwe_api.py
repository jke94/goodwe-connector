import datetime
from goodwe_connector.goodwe_constants import GOODWE_API_URL
from goodwe_connector.goodwe_api_methods import GetPowerStationPowerAndIncomeByDay
from goodwe_connector.goodwe_api_methods import v2CommonCrossLogin
from goodwe_connector.goodwe_logger.goodwe_api_logger import GoodweApiLogger
from requests.exceptions import RequestException
from json import JSONDecodeError
import json
import requests

class GoodweApi:
    """_summary_
    """

    def __init__(self,
                 system_id:str, 
                 account:str, 
                 password:str, 
                 logging=False) -> None:
        """_summary_

        Args:
            system_id (str): _description_
            account (str): _description_
            password (str): _description_
            logging (bool, optional): _description_. Defaults to False.
        """
        
        self.__headers = {
            'User-Agent': 'SEMS Portal/3.1 (iPhone; iOS 13.5.1; Scale/2.00)',
            'Token': '{"version":"v3.1","client":"ios","language":"en"}',
        }
        
        self.__global_url = GOODWE_API_URL
        self.system_id = system_id
        self.account = account
        self.password = password
        self.base_url = self.__global_url
        self.__token = ''
        self.__n_max_request_retry = 5
        
        self.__logger = GoodweApiLogger(isLogging=logging)

    def __login(self, url, payload) -> dict:
        
        try:

            loginPayload = {
                'account': self.account,
                'pwd': self.password,
            }

            authrequest = requests.post(
                self.__global_url + v2CommonCrossLogin, 
                headers=self.__headers, 
                data=loginPayload, 
                timeout=10)
            
            authrequest.raise_for_status()
            
            self.__logger.info(f'Login request elapsed seconds: {authrequest.elapsed}')
            
            data = authrequest.json()
            authrequest.close()

            # Print login json result.
            # print(json.dumps(data, indent=4))

            if('api' not in data):
                self.__logger.warning(f' key: api, does not in {data}')
                return None
            
            self.base_url = data['api']
            self.__token = json.dumps(data['data'])

            headers = {
                'User-Agent': 'SEMS Portal/3.1 (iPhone; iOS 13.5.1; Scale/2.00)',
                'Token': self.__token,
            }

            request = requests.post(
                self.base_url + url, 
                headers=headers, 
                data=payload, 
                timeout=10)
            
            request.raise_for_status()
            
            self.__logger.info(f'Method request elapsed seconds: {request.elapsed}')
            
            data = request.json()
            request.close()

            return data['data']
        
        except JSONDecodeError as json_decoder_error:
            self.__logger.warning(f'{json_decoder_error}')
            return None

        except RequestException as e:
            self.__logger.warning(f'{e}')
            return None

    def get_power_generation_per_day(self, date:datetime) -> float:
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
        
        count_request = 0
        data = {}
        
        while(not data and count_request < self.__n_max_request_retry):
        
            count_request += 1
            method = GetPowerStationPowerAndIncomeByDay
            data = self.__login(method, payload)
        
            if not data:
                self.__logger.warning(f'Request count={count_request}, Method: {method}, missing data.')

        # Parsing data to extract the correct day.
        for day in data:
            if day['d'] == date.strftime('%m/%d/%Y'):
                return day['p']

        return -2