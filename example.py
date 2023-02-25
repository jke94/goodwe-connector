from goodwe_connector.goodwe_api import GoodweApi
import datetime
import configparser
import os.path
import json

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

def main(json_credentials_file):

    # Read secret credentials from JSON file.
    config = read_json_config(json_credentials_file)
    
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

    # Request data to the Goodwe Api.
    day = datetime.datetime(2023, 2, 14)
    power_generated = goodweapi.get_power_generation_per_day(day)
    
    print(f'Day {day.strftime("%d/%m/%Y")}\tPower Generated: {power_generated}')

if __name__ == "__main__":
    
    json_credentials_config_file = 'goodwe_config.json'
    main(json_credentials_config_file)