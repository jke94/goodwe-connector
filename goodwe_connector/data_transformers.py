from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import pandas as pd


def parse_daily_generation(data: Iterable[dict], target_date: datetime) -> dict:
    for day in data:
        if day.get("d") == target_date.strftime("%m/%d/%Y"):
            return {target_date.strftime("%Y-%m-%d"): day.get("p")}
    return {}


def parse_generation_series(data: Iterable[dict], start_date: datetime) -> dict:
    generation: Dict[str, float] = {}

    for day in data:
        if day.get("d") == start_date.strftime("%m/%d/%Y"):
            generation[start_date.strftime("%Y-%m-%d")] = day.get("p")
    return generation


def format_generation_summary(generation: dict) -> str:
    if not generation:
        return "Generated 0.00 kWh (avg. 0.00 kWh per day) in 0 days."

    average = sum(generation.values()) / len(generation.keys())
    average_str = "{:.2f}".format(average)
    total_power_generated = "{:.2f}".format(sum(generation.values()))
    return f"Generated {total_power_generated} kWh (avg. {average_str} kWh per day) in {len(generation.keys())} days."


def write_generation_to_csv(generation: dict, file_name: str) -> None:
    output_path = Path(file_name)
    dataframe = pd.DataFrame(generation.items(), columns=["Date", "ProductionkWh"])
    dataframe.to_csv(output_path, index=False, sep=";", decimal=",")
