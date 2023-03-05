from json import JSONDecodeError
import json
import requests
from requests.exceptions import RequestException
from goodwe_connector.goodwe_constants import GOODWE_API_URL
from goodwe_connector.goodwe_api_methods import v2CommonCrossLogin
from goodwe_connector.goodwe_logger.goodwe_api_logger import GoodweApiLogger

class GoodweApiAuth:

    def __init__(self,
                 system_id:str, 
                 account:str, 
                 password:str, 
                 logging=False) -> None:
        
        self.__headers = {
            'User-Agent': 'SEMS Portal/3.1 (iPhone; iOS 13.5.1; Scale/2.00)',
            'Token': '{"version":"v3.1","client":"ios","language":"en"}',
        }
        
        self.__global_url = GOODWE_API_URL
        self.system_id = system_id
        self.account = account
        self.password = password
        self.base_url = self.__global_url
        self._credentials = ''
        
        self._logger = GoodweApiLogger(isLogging=logging)
        
    def _authorization(self) -> bool:
        
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
            
            self._logger.info(f'Login request elapsed seconds: {authrequest.elapsed}')
            
            data = authrequest.json()
            authrequest.close()

            # Print login json result.
            # print(json.dumps(data, indent=4))

            if('api' not in data):
                self._logger.warning(f' key: api, does not in {data}')
                return False
            
            self.base_url = data['api']
            self._credentials = json.dumps(data['data'])
            
            return True
        
        except RequestException as e:
            self._logger.warning(f'{e}')
            return False
        
        except JSONDecodeError as json_decoder_error:
            self._logger.warning(f'{json_decoder_error}')
            return False