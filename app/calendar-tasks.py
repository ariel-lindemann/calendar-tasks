import json

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from ics import Calendar
from sequence import validate_sequence, write_sequence

app = FastAPI()


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
