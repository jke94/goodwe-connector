from goodwe_connector.goodwe_api import GoodweApi
import datetime

goodweapi = GoodweApi(
    system_id='',
    account='',
    password='')

data = goodweapi.dummy_function(
    "v2/PowerStationMonitor/GetPowerStationPowerAndIncomeByDay",
    datetime.datetime(2023,2,19))

print(data)