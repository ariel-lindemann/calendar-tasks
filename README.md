# Calendar Tasks

This project provides a FastAPI-based API for generating calendar files with recurring appointments. Users can send configuration details through a POST request to receive an .ics calendar file as a response.
Features

+ Accepts a list of **sequences** which consist of appointment names, start date, end date, and recurrence interval.
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
fastapi run app/calendar-tasks.py
```

### Docker

If you want to start the app inside Docker, run:

```sh
docker build . --tag calendar-tasks
docker run -p 8000:8000 calendar-tasks
```

## Usage

Send a POST request to the `/generate_calendar` endpoint, with the following json body:
```json
{
    "calendar_name": "recurring_appointments",
    "sequences": [
        {
            "appointment_names": [
                "Appointment 1",
                "Appointment 2",
                "Appointment 3"
            ],
            "start_date": "2024-08-06",
            "end_date": "2024-09-30",
            "recurrence_interval_days": 14
        },
        {
            "appointment_names": [
                "Appointment 1",
                "Appointment 3"
            ],
            "start_date": "2024-10-02",
            "end_date": "2024-09-31",
            "recurrence_interval_days": 7
        }
    ]
}
```
You will receive an .ics calendar file in response.

Using `curl`:

```sh
curl -X POST "http://localhost:8000/generate_calendar/" -H "Content-Type: application/json" -d '{
    "calendar_name": "recurring_appointments",
    "sequences": [
        {
            "appointment_names": [
                "Appointment 1",
                "Appointment 2",
                "Appointment 3"
            ],
            "start_date": "2024-08-06",
            "end_date": "2024-09-30",
            "recurrence_interval_days": 14
        },
        {
            "appointment_names": [
                "Appointment 1",
                "Appointment 3"
            ],
            "start_date": "2024-10-02",
            "end_date": "2024-09-31",
            "recurrence_interval_days": 7
        }
    ]
}'
```

## Documentation

You can take a look at the OpenAPI specification of the enpoints at `localhost:8000/docs`
