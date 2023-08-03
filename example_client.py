import datetime
import configparser
import os.path
import json
import time

from goodwe_connector.goodwe_constants import JSON_CREDENTIALS_CONFIG_FILE
from goodwe_connector.goodwe_context import GoodweContext
from goodwe_connector.goodwe_api import GoodweApi
from goodwe_connector.strategies.power_generation_per_day import PowerGenerationPerDay
from goodwe_connector.strategies.power_generation_between_dates import PowerGenerationBetweenDays
from goodwe_connector.strategies.power_generation_between_dates_to_csv import PowerGenerationBetweenDaysToCsv
from goodwe_connector.strategies.power_station_monitor_detail import PowerStationMonitorDetail

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

    # 1: Get power generation a specific day.
    
    context = GoodweContext(
        goodwe_api=goodweapi,
        strategy=PowerGenerationPerDay(date=datetime.datetime(2023, 8, 2)))
    
    data = context.process()
    print(json.dumps(data, indent = 4))
    
    # 2: Get power generation between range of days.
    
    context.strategy = PowerGenerationBetweenDays(
        start_date=datetime.datetime(2023, 8, 1),
        end_date=datetime.datetime(2023, 8, 3)
    )
    
    data = context.process()
    print(json.dumps(data, indent = 4))

    # 3: Get power generation between range of days and save in CSV file.

    context.strategy = PowerGenerationBetweenDaysToCsv(
        start_date=datetime.datetime(2023, 8, 1),
        end_date=datetime.datetime(2023, 8, 3),
        file_name='./simple_test.csv',
        show_info=True
    )

    data = context.process()
    
    # 4: Get power generation between range of days and save in CSV file.

    context.strategy = PowerStationMonitorDetail(
        year=2023,
        month=5
    )

    data = context.process()
    print(json.dumps(data, indent = 4))

    # __get_power_station_generated_every_five_minutes_per_day(goodweapi)
    
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    
    main()