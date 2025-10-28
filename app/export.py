import json
import icalendar as ical
from datetime import timedelta, date
import logging
logger = logging.getLogger("uvicorn.app.export")

from app.models import CalendarConfig, Event, Sequence

def basic_calendar() -> ical.Calendar:
    calendar = ical.Calendar()
    calendar.add("version", "2.0")
    calendar.add("prodid", "-//Ariel Lindemann//calendar-tasks//EN")
    return calendar

def cal_from_events(events: list[Event]) -> ical.Calendar:
    calendar = basic_calendar()
    for event in events:
        cal_event = ical.Event()
        cal_event.add("summary", event.name)
        cal_event.add("dtstart", event.start_date)
        cal_event.add("dtend", event.end_date)
        calendar.add_component(cal_event)
    return calendar

def read_config(file_path: str) -> CalendarConfig:
    with open(file_path, "r") as file:
        config = json.load(file)
    return config


def create_ical_file(calendar: ical.Calendar, file_name: str):
    file_path = f"{file_name}.ics"

    with open(file_path, "w") as file:
        file.write(calendar.to_ical().decode("utf-8"))

    logger.info(f"Calendar file {file_path} created successfully.")

    return file_path


def from_events(events: list[Event], file_name: str) -> str:
    return create_ical_file(cal_from_events(events), file_name)


def write_sequence(sequence: Sequence, calendar: ical.Calendar) -> ical.Calendar:
    appointment_names = sequence.appointment_names

    start_date = sequence.start_date
    end_date = sequence.end_date

    recurrence = timedelta(days=sequence.recurrence_interval_days)

    current_date = start_date
    index = 0

    while current_date <= end_date:
        event = ical.Event()
        event.add("summary", appointment_names[index % len(appointment_names)])
        # if only date is passed, it is considered all-day
        event.add("start", current_date.date()) 
        calendar.add_component(event)

        current_date += recurrence
        index += 1

    return calendar

def from_calendar_config(config: CalendarConfig) -> str:
    calendar = basic_calendar()

    for sequence in config.sequences:
        calendar = write_sequence(sequence, calendar)

    return create_ical_file(calendar, config.calendar_name)
