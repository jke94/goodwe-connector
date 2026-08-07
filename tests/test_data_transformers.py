from datetime import datetime

from goodwe_connector.data_transformers import parse_daily_generation, write_generation_to_csv


def test_parse_daily_generation_returns_matching_day():
    # Arrange
    target_date = datetime(2024, 1, 2)
    payload = [{"d": "01/02/2024", "p": 10.5}, {"d": "01/03/2024", "p": 12.0}]

    # Act
    result = parse_daily_generation(payload, target_date)

    # Assert
    assert result == {"2024-01-02": 10.5}


def test_write_generation_to_csv_creates_file(tmp_path):
    # Arrange
    output_path = tmp_path / "generation.csv"

    # Act
    write_generation_to_csv({"2024-01-01": 10.5, "2024-01-02": 11.0}, str(output_path))

    # Assert
    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8-sig").startswith("Date;ProductionkWh")
