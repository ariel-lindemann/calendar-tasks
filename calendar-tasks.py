import json
from ics import Calendar, Event
from datetime import datetime, timedelta


def read_config(file_path: str):
    with open(file_path, "r") as file:
        config = json.load(file)
    return config


def validate_config(config: dict):
    if "calendar_name" not in config:
        config["calendar_name"] = "recurring_appointments"

    if "start_date" not in config:
        config["start_date"] = datetime.today()
    else:
        config["start_date"] = datetime.strptime(config["start_date"], "%Y-%m-%d")

    if "end_date" not in config:
        config["end_date"] = config["start_date"] + timedelta(days=365)
    else:
        date = datetime.strptime(config["end_date"], "%Y-%m-%d")
        config["end_date"] = (
            date
            if date >= config["start_date"]
            else config["start_date"] + timedelta(days=365)
        )

    if "recurrence_interval_days" not in config:
        config["recurrence_interval_days"] = 1

    return config


config = read_config("config.json")
config = validate_config(config)

calendar_name = config["calendar_name"]
appointment_names = config["appointment_names"]

start_date = config["start_date"]
end_date = config["end_date"]

recurrence = timedelta(days=config["recurrence_interval_days"])

num_appointments = 20

calendar = Calendar()

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

with open(f"{calendar_name}.ics", "w") as file:
    file.writelines(calendar)

print(f"Calendar file '{calendar_name}.ics' created successfully.")
