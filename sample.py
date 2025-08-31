import argparse
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
from goodwe_connector.strategies.power_station_generated_every_five_minutes_per_day import PowerStationGeneratedEveryFiveMinutesPerDay

STRATEGY_REGISTRY = {
    "power_generation_per_day": PowerGenerationPerDay,
    "power_generation_between_days": PowerGenerationBetweenDays,
    "power_generation_between_days_to_csv": PowerGenerationBetweenDaysToCsv,
    "power_station_monitor_detail": PowerStationMonitorDetail,
    "power_station_generated_every_five_minutes_per_day": PowerStationGeneratedEveryFiveMinutesPerDay,
}

def read_json_config(confg_file_name) -> dict:
    if(not os.path.exists(confg_file_name)):
        print(f'Error! File: {confg_file_name}, does not exits! The file needs store the secrets for the connection.')
        return None
    file = open(confg_file_name)
    config = configparser.ConfigParser()
    config.read_dict(json.load(file))
    file.close()
    return config

def parse_args():
    parser = argparse.ArgumentParser(description="Goodwe Connector Strategy Runner")
    parser.add_argument("strategy", choices=STRATEGY_REGISTRY.keys(), help="Strategy to execute")
    parser.add_argument("--date", type=str, help="Date (YYYY-MM-DD)")
    parser.add_argument("--start_date", type=str, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end_date", type=str, help="End date (YYYY-MM-DD)")
    parser.add_argument("--year", type=int, help="Year")
    parser.add_argument("--month", type=int, help="Month")
    parser.add_argument("--file_name", type=str, help="CSV file name")
    parser.add_argument("--show_info", action="store_true", help="Show info (for CSV strategy)")
    return parser.parse_args()

def main():
    start_time = time.time()
    args = parse_args()

    config = read_json_config(JSON_CREDENTIALS_CONFIG_FILE)
    if(config is None): 
        return
    
    system_id = config['goodwe_api_connection']['system_id']
    user = config['goodwe_api_connection']['account']
    password = config['goodwe_api_connection']['password']

    goodweapi = GoodweApi(
        system_id=system_id,
        account=user,
        password=password,
        logging=True
    )

    strategy_cls = STRATEGY_REGISTRY[args.strategy]
    strategy_kwargs = {}

    # Map arguments to strategy parameters
    if args.date:
        strategy_kwargs["date"] = datetime.datetime.strptime(args.date, "%Y-%m-%d")
    if args.start_date:
        strategy_kwargs["start_date"] = datetime.datetime.strptime(args.start_date, "%Y-%m-%d")
    if args.end_date:
        strategy_kwargs["end_date"] = datetime.datetime.strptime(args.end_date, "%Y-%m-%d")
    if args.year:
        strategy_kwargs["year"] = args.year
    if args.month:
        strategy_kwargs["month"] = args.month
    if args.file_name:
        strategy_kwargs["file_name"] = args.file_name
    if args.show_info:
        strategy_kwargs["show_info"] = args.show_info

    context = GoodweContext(
        goodwe_api=goodweapi,
        strategy=strategy_cls(**strategy_kwargs)
    )

    data = context.process()
    if data is not None:
        print(json.dumps(data, indent=4))

    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()

# How to run it:
# python sample.py power_generation_per_day --date 2025-02-22
# python sample.py power_generation_between_days --start_date 2025-01-01 --end_date 2025-02-21
# python sample.py power_generation_between_days_to_csv --start_date 2025-02-01 --end_date 2025-02-10 --file_name enero-febrero-2025.csv --show_info
# python sample.py power_station_monitor_detail --year 2025 --month 1
# python sample.py power_station_generated_every_five_minutes_per_day --date 2025-01-10