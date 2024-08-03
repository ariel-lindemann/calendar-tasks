# Calendar Tasks

This project provides a FastAPI-based API for generating calendar files with recurring appointments. Users can send configuration details through a POST request to receive an .ics calendar file as a response.
Features

+ Accepts a list of appointment names, start date, end date, and recurrence interval.
+ Generates a calendar file with recurring events.
+ Ensures valid configurations with fallback to default values.
+ Serves the generated calendar file for download.

## Installation

Clone the repository:
```sh
git clone https://github.com/ariel-lindemann/calendar-tasks
cd calendar-tasks
```

Install the dependencies:
```sh
pip install -r requrements.txt
```

Run the API
```sh
fastapi run calendar-tasks.py
```

## Usage

Send a POST request to the `/generate_calendar` endpoint, with the following json body:
```json
{
    "appointment_names": ["Meeting A", "Meeting B", "Meeting C"],
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "recurrence_interval_days": 14
}
```
You will receive an .ics calendar file in response.

Using `curl`:

```sh
curl -X POST "http://localhost:8000/generate_calendar/" -H "Content-Type: application/json" -d '{
    "appointment_names": ["Meeting A", "Meeting B", "Meeting C"],
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "recurrence_interval_days": 14
}'

## Documentation

You can take a look at the OpenAPI specification of the enpoints at `localhost:8000/docs`
```
