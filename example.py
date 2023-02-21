from goodwe_connector.goodwe_api import GoodweApi
import datetime
import configparser

# Read configuration
config = configparser.ConfigParser()
config.read('goodw_api_config.json')

system_id = config['goowdw_api_connection']['system_id']
user = config['goowdw_api_connection']['account']
password = config['goowdw_api_connection']['password']

goodweapi = GoodweApi(
    system_id=system_id,
    account=user,
    password=password)

data = goodweapi.dummy_function(
    "v2/PowerStationMonitor/GetPowerStationPowerAndIncomeByDay",
    datetime.datetime(2023,2,19))

print(data)