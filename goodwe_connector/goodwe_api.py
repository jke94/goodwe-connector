from goodwe_connector.goodwe_constants import GOODWE_API_HEADER,GOODWE_API_TOKEN, GOODWE_API_URL
from goodwe_connector.goodwe_logger.goodwe_api_logger import GoodweApiLogger
from requests.exceptions import RequestException
from json import JSONDecodeError
import json
import requests

class GoodweApi:

    def __init__(self, system_id, account, password, logging=False) -> None:
        
        self.__global_url = 'https://semsportal.com/api/'
        self.__headers = {
            'User-Agent': 'SEMS Portal/3.1 (iPhone; iOS 13.5.1; Scale/2.00)',
            'Token': '{"version":"v3.1","client":"ios","language":"en"}',
        }

        self.system_id = system_id
        self.account = account
        self.password = password
        self.base_url = self.__global_url
        self.token = ''
        self.__n_max_request_retry = 5
        
        self.__logger = GoodweApiLogger(logging)

    def __login(self, url, payload) -> dict:
        
        try:

            loginPayload = {
                'account': self.account,
                'pwd': self.password,
            }

            authrequest = requests.post(
                self.__global_url + 'v2/Common/CrossLogin', 
                headers=self.__headers, 
                data=loginPayload, 
                timeout=10)
            
            authrequest.raise_for_status()
            
            self.__logger.info(f'Login request elapsed seconds: {authrequest.elapsed}')
            
            data = authrequest.json()
            authrequest.close()

            # Print login json result.
            # print(json.dumps(data, indent=4))

            self.base_url = data['api']
            self.token = json.dumps(data['data'])

            headers = {
                'User-Agent': 'SEMS Portal/3.1 (iPhone; iOS 13.5.1; Scale/2.00)',
                'Token': self.token,
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

    def get_power_generation_per_day(self, date) -> float:

        payload = {
            'powerstation_id' : self.system_id,
            'date' : date.strftime('%Y-%m-%d')
        }
        
        count_request = 0
        data = {}
        
        while(not data and count_request < self.__n_max_request_retry):
        
            count_request += 1
            method = "v2/PowerStationMonitor/GetPowerStationPowerAndIncomeByDay"
            data = self.__login(method, payload)
        
            if not data:
                self.__logger.warning(f'Request count={count_request}, Method: {method}, missing data.')

        # Parsing data to extract the correct day.
        for day in data:
            if day['d'] == date.strftime('%m/%d/%Y'):
                return day['p']

        return -2