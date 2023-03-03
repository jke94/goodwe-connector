from numpy import void
from goodwe_connector.goodwe_api import GoodweApi
import datetime
import configparser
import os.path
import json

json_credentials_config_file = 'goodwe_config.json'

def read_json_config(confg_file_name) -> dict:
    
    if(not os.path.exists(confg_file_name)):
        print(f'Error! File: {confg_file_name}, does not exits! The file needs store the secrets for the connection.')
        return None

    # Read secrets configuration file
    file = open(confg_file_name)
    config = configparser.ConfigParser()
    config.read_dict(json.load(file))
    file.close()
    
    return config

def __get_power_generation_per_day(goodweapi:GoodweApi) -> void:
        
    day = datetime.datetime(2023, 2, 14)
    power_generated = goodweapi.get_power_generation_per_day(day)
    
    print(f'Day {day.strftime("%d/%m/%Y")}\tPower Generated: {power_generated} kW')

def __get_power_generation_between_dates(goodweapi:GoodweApi) -> void:
    
    data = goodweapi.get_power_generation_between_dates(
        start_date=datetime.datetime(2023, 1, 1),
        end_date=datetime.datetime(2023, 3, 2)
    )
    
    print(json.dumps(data, indent = 4) )

def main():

    # Read secret credentials from JSON file.
    config = read_json_config(json_credentials_config_file)
    
    if(config is None): 
        return
    
    system_id = config['goodwe_api_connection']['system_id']
    user = config['goodwe_api_connection']['account']
    password = config['goodwe_api_connection']['password']

    # Goodew Api client initialization.
    goodweapi = GoodweApi(
        system_id=system_id,
        account=user,
        password=password,
        logging=True)
    
    # TODO: Uncomment the function that you want use it!
    
    # __get_power_generation_per_day(goodweapi)
    __get_power_generation_between_dates(goodweapi)
    

if __name__ == "__main__":
    
    main()