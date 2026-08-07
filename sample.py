from goodwe_connector.cli import main


if __name__ == "__main__":
    main()

# How to run it:
# python sample.py power_generation_per_day --date 2025-02-22
# python sample.py power_generation_between_days --start_date 2025-01-01 --end_date 2025-02-21
# python sample.py power_generation_between_days_to_csv --start_date 2025-02-01 --end_date 2025-02-10 --file_name enero-febrero-2025.csv --show_info
# python sample.py power_station_monitor_detail --year 2025 --month 1
# python sample.py power_station_generated_every_five_minutes_per_day --date 2025-01-10