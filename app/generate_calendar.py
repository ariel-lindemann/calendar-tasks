import json

from ics import Calendar
from sequence import validate_sequence, write_sequence

def read_config(file_path: str):
    with open(file_path, "r") as file:
        config = json.load(file)
    return config


def validate_config(config: dict) -> dict:
    if "calendar_name" not in config:
        config["calendar_name"] = "recurring_appointments"

    for sequence in config["sequences"]:
        sequence = validate_sequence(sequence)

    return config


def generate_calendar_file(config: dict) -> str:
    config = validate_config(config)

    calendar = Calendar()

    for sequence in config["sequences"]:
        calendar = write_sequence(sequence, calendar)

    calendar_file_path = f"{config['calendar_name']}.ics"

    with open(calendar_file_path, "w") as file:
        file.writelines(calendar)

    print(f"Calendar file {calendar_file_path} created successfully.")

    return calendar_file_path
