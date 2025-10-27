import json
import ics
from datetime import timedelta
import logging
logger = logging.getLogger("uvicorn.app.export")

from app.models import CalendarConfig, Event, Sequence

def read_config(file_path: str) -> CalendarConfig:
    with open(file_path, "r") as file:
        config = json.load(file)
    return config


def export_to_ical(calendar: ics.Calendar, file_name: str):
    file_path = f"{file_name}.ics"

    with open(file_path, "w") as file:
        file.writelines(calendar) # type: ignore

    logger.info(f"Calendar file {file_path} created successfully.")

    return file_path


def from_events(events: list[Event], file_name: str) -> str:
    calendar = ics.Calendar()
    for event in events:
        cal_event = ics.Event()
        cal_event.name = event.name
        cal_event.begin = event.start_date
        cal_event.end = event.end_date
        calendar.events.add(cal_event)
    return export_to_ical(calendar, file_name)

def write_sequence(sequence: Sequence, calendar: ics.Calendar) -> ics.Calendar:
    appointment_names = sequence.appointment_names

    start_date = sequence.start_date
    end_date = sequence.end_date

    recurrence = timedelta(days=sequence.recurrence_interval_days)

    current_date = start_date
    index = 0

    while current_date <= end_date:
        event = ics.Event()
        event.name = appointment_names[index % len(appointment_names)]
        event.begin = current_date
        event.make_all_day()
        calendar.events.add(event)

        current_date += recurrence
        index += 1

    return calendar

def from_calendar_config(config: CalendarConfig) -> str:
    calendar = ics.Calendar()

    for sequence in config.sequences:
        calendar = write_sequence(sequence, calendar)

    return export_to_ical(calendar, config.calendar_name)
