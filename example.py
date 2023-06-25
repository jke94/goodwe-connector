from goodwe_connector.goodwe_api import GoodweApi
import datetime
import configparser
import os.path
import json
import time

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

def __get_power_generation_per_day(goodweapi:GoodweApi) -> None:
        
    day = datetime.datetime(2023, 6, 22)
    data = goodweapi.get_power_generation_per_day(day)
    
    print("Day and kW of power generated: ")
    print(json.dumps(data, indent = 4))

def __get_power_generation_between_dates(goodweapi:GoodweApi) -> None:
    
    data = goodweapi.get_power_generation_between_dates(
        start_date=datetime.datetime(2023, 6, 1),
        end_date=datetime.datetime(2023, 6, 30)
    )
    
    print(json.dumps(data, indent = 4))
    
def __get_power_station_generated_every_five_minutes_per_day(goodweapi:GoodweApi) -> None:
    
    day = datetime.datetime(2022, 5, 23)
    data = goodweapi.get_power_station_generated_every_five_minutes_per_day(date=day)
    
    print(json.dumps(data, indent = 4))

def __get_power_station_monitor_detail(goodweapi:GoodweApi, year:int, month:int) -> None:
    
    data = goodweapi.get_power_station_monitor_detail(year=year, month=month)
    
    print(json.dumps(data, indent = 4, ensure_ascii=False))

def main():

    start_time = time.time()

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
    
    print('Uncomment some function to run it! ;)')

    # __get_power_generation_per_day(goodweapi)
    __get_power_generation_between_dates(goodweapi)
    # __get_power_station_generated_every_five_minutes_per_day(goodweapi)
    # __get_power_station_monitor_detail(goodweapi, year=2022, month=12)
    
    print("--- %s seconds ---" % (time.time() - start_time))
    
if __name__ == "__main__":
    
    main()