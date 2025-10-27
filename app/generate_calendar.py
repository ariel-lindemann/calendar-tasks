import json
from ics import Calendar
from pydantic import BaseModel

from app.sequence import write_sequence, Sequence

class CalendarConfig(BaseModel):
    calendar_name: str = "recurring_appointments"
    sequences: list[Sequence] = []

def read_config(file_path: str) -> CalendarConfig:
    with open(file_path, "r") as file:
        config = json.load(file)
    return config


def generate_calendar_file(config: CalendarConfig) -> str:

    calendar = Calendar()

    for sequence in config.sequences:
        calendar = write_sequence(sequence, calendar)

    calendar_file_path = f"{config.calendar_name}.ics"

    with open(calendar_file_path, "w") as file:
        file.writelines(calendar)

    print(f"Calendar file {calendar_file_path} created successfully.")

    return calendar_file_path
