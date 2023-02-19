from goodwe_connector.goodwe_constants import GOODWE_API_HEADER,GOODWE_API_TOKEN, GOODWE_API_URL
import json
import logging
import requests
from requests.exceptions import RequestException

class GoodweApi:

    def __init__(self, system_id, account, password) -> None:
        
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

        logging.basicConfig(
            filename='goodwe-connector.log', 
            encoding='utf-8', 
            level=logging.DEBUG)

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
            data = authrequest.json()
            authrequest.close()

            print(json.dumps(data, indent=4))

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
            data = request.json()
            request.close()

            return data['data']

        except RequestException as e:
            logging.warning(f'{e}')
            return {}
        
    def dummy_function(self, method, date):

        payload = {
            'powerstation_id' : self.system_id,
            'count' : 1,
            'date' : date.strftime('%Y-%m-%d')
        }

        data = self.__login(method, payload)

        if not data:
            logging.warning(f'Method: {method}, missing data.')
            return 0

        eday_kwh = 0
        for day in data:
            if day['d'] == date.strftime('%m/%d/%Y'):
                eday_kwh = day['p']

        return eday_kwh