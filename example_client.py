from goodwe_connector.goodwe_api import GoodweApi
import datetime
import configparser
import os.path
import json
import time

from goodwe_connector.strategies.power_generation_per_day import PowerGenerationPerDay
from goodwe_connector.goodwe_context import GoodweContext
JSON_CREDENTIALS_CONFIG_FILE = 'goodwe_config.json'

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

def main():

    start_time = time.time()

    # Read secret credentials from JSON file.
    config = read_json_config(JSON_CREDENTIALS_CONFIG_FILE)
    
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
    
    print('Uncomment some function to run it! ;)')

    context = GoodweContext(
        goodwe_api=goodweapi,
        strategy=PowerGenerationPerDay(date=datetime.datetime(2023, 7, 20)))
    
    data = context.do_some_business_logic()
    
    print(json.dumps(data, indent = 4))

    # __get_power_generation_per_day(goodweapi)
    # __get_power_generation_between_dates(goodweapi)
    # __get_power_generation_between_dates_to_csv(
    #     goodweapi, 
    #     start_date=datetime.datetime(2023, 7, 20),
    #     end_date=datetime.datetime(2023, 7, 31),
    #     file_path_name='./production_by_day.csv')
    # __get_power_station_generated_every_five_minutes_per_day(goodweapi)
    # __get_power_station_monitor_detail(goodweapi, year=2022, month=12)
    
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    
    main()