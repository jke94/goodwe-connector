from goodwe_connector.goodwe_api import GoodweApi
import datetime
import configparser
import os.path

def main():

    config_file = 'goodwe_config.json'
    
    if(not os.path.exists(config_file)):
        print(f'Error! File: {config_file}, does not exits! The file needs store the secrets for the connection.')
        return None

    # Read secrets configuration file
    config = configparser.ConfigParser()
    config.read(config_file)
    
    system_id = config['goowdw_api_connection']['system_id']
    user = config['goodwe_api_connection']['account']
    password = config['goodwe_api_connection']['password']

    goodweapi = GoodweApi(
        system_id=system_id,
        account=user,
        password=password)

    data = goodweapi.dummy_function(
        "v2/PowerStationMonitor/GetPowerStationPowerAndIncomeByDay",
        datetime.datetime(2023,2,19))

    print(data)

if __name__ == "__main__":
    main()