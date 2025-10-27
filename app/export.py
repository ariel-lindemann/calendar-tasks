import json
from ics import Calendar
import ics

from app.sequence import write_sequence
from app.models import CalendarConfig, Event

def read_config(file_path: str) -> CalendarConfig:
    with open(file_path, "r") as file:
        config = json.load(file)
    return config


def export_to_ical(calendar: Calendar, file_name: str):
    file_path = f"{file_name}.ics"

    with open(file_path, "w") as file:
        file.writelines(calendar) # type: ignore

    print(f"Calendar file {file_path} created successfully.")

    return file_path


def from_events(events: list[Event], file_name: str) -> str:
    calendar = Calendar()
    for event in events:
        cal_event = ics.Event()
        cal_event.name = event.name
        cal_event.begin = event.start_date
        cal_event.end = event.end_date
        calendar.events.add(cal_event)
    return export_to_ical(calendar, file_name)


def from_calendar_config(config: CalendarConfig) -> str:

    calendar = Calendar()

    for sequence in config.sequences:
        calendar = write_sequence(sequence, calendar)

    return export_to_ical(calendar, config.calendar_name)
