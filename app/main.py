from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.generate_calendar import generate_calendar_file
from app.models import CalendarConfig, Event
from app.persistence import delete_event, get_event_by_id, save_event, update_event

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.post("/generate_calendar/")
async def generate_calendar(config: CalendarConfig):
    try:
        path = generate_calendar_file(config)
        return FileResponse(
            path, media_type="text/calendar", filename=f"{config.calendar_name}.ics"
        )

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/events/")
def create_event(event: Event):
    save_event(event)
    return {"message": "Event created successfully"}

@app.get("/events/{event_id}")
def read_event(event_id: int):
    event = get_event_by_id(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@app.put("/events/{event_id}")
def update_event_endpoint(event_id: int, event: Event):
    existing_event = get_event_by_id(event_id)
    if existing_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    update_event(event_id, event)
    return {"message": "Event updated successfully"}

@app.delete("/events/{event_id}")
def delete_event_endpoint(event_id: int):
    existing_event = get_event_by_id(event_id)
    if existing_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    delete_event(event_id)
    return {"message": "Event deleted successfully"}

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Recurring Appointments Calendar API! Use the /generate-calendar endpoint to generate a calendar file."
    }
