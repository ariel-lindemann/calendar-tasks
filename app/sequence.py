from datetime import timedelta
from ics import Calendar, Event

from app.models import Sequence


def write_sequence(sequence: Sequence, calendar: Calendar) -> Calendar:
    appointment_names = sequence.appointment_names

    start_date = sequence.start_date
    end_date = sequence.end_date

    recurrence = timedelta(days=sequence.recurrence_interval_days)

    current_date = start_date
    index = 0

    while current_date <= end_date:
        event = Event()
        event.name = appointment_names[index % len(appointment_names)]
        event.begin = current_date
        event.make_all_day()
        calendar.events.add(event)

        current_date += recurrence
        index += 1

    return calendar
