import json
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from ics import Calendar, Event

app = FastAPI()


def read_config(file_path: str):
    with open(file_path, "r") as file:
        config = json.load(file)
    return config


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


def validate_config(config: dict) -> dict:
    if "calendar_name" not in config:
        config["calendar_name"] = "recurring_appointments"

    for sequence in config["sequences"]:
        sequence = validate_sequence(sequence)

    return config


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
        event.duration = timedelta(days=1)
        calendar.events.add(event)

        current_date += recurrence
        index += 1

    return calendar


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


@app.post("/generate_calendar/")
async def generate_calendar(config: dict):
    try:
        path = generate_calendar_file(config)
        return FileResponse(
            path, media_type="text/calendar", filename=f"{config['calendar_name']}.ics"
        )

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Recurring Appointments Calendar API! Use the /generate-calendar endpoint to generate a calendar file."
    }
