from datetime import datetime, timedelta

from ics import Calendar, Event


def validate_date(date_str: str, fallback: datetime) -> datetime:
    try:
        valid_date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError as e:
        print(e)
        print(f"Can't assign value {date_str}. Assinging fallback date {fallback}")
        valid_date = fallback

    return valid_date


def validate_sequence(sequence: dict) -> dict:
    if "start_date" not in sequence:
        sequence["start_date"] = datetime.today()
    else:
        sequence["start_date"] = validate_date(sequence["start_date"], datetime.today())

    if "end_date" not in sequence:
        sequence["end_date"] = sequence["start_date"] + timedelta(days=365)
    else:
        date = validate_date(
            sequence["end_date"], sequence["start_date"] + timedelta(days=365)
        )
        sequence["end_date"] = (
            date
            if date >= sequence["start_date"]
            else sequence["start_date"] + timedelta(days=365)
        )

    if "recurrence_interval_days" not in sequence:
        sequence["recurrence_interval_days"] = 1

    return sequence


def write_sequence(sequence: dict, calendar: Calendar) -> Calendar:
    appointment_names = sequence["appointment_names"]

    start_date = sequence["start_date"]
    end_date = sequence["end_date"]

    recurrence = timedelta(days=sequence["recurrence_interval_days"])

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
