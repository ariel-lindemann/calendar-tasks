from fastapi import HTTPException
from fastapi.routing import APIRouter
from fastapi.responses import FileResponse

from app.models import CalendarConfig, Event
import app.export as export
import app.persistence as persistence
from app.version import get_version

import logging
logger = logging.getLogger("uvicorn.app.routes")
    
router = APIRouter()

@router.get("/version")
async def get_version_endpoint():
    return {"version": get_version()}

@router.post("/generate_calendar/")
async def generate_calendar(config: CalendarConfig):
    try:
        path = export.from_calendar_config(config)
        return FileResponse(
            path, media_type="text/calendar", filename=f"{config.calendar_name}.ics"
        )

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/events/")
async def create_events(events: list[Event]):
    try:
        for event in events:
            persistence.save_event(event)
    except Exception as e:
        logger.error(f"Error saving event: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Event created successfully"}

# TODO add filters
# TODO pagination
@router.get("/events/")
async def read_events():
    events = persistence.get_all_events()
    return events

@router.get("/events/{event_id}")
async def read_event(event_id: int):
    event = persistence.get_event_by_id(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/events/{event_id}")
async def update_event_endpoint(event_id: int, event: Event):
    existing_event = persistence.get_event_by_id(event_id)
    if existing_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    persistence.update_event(event_id, event)
    return {"message": "Event updated successfully"}

@router.delete("/events/{event_id}")
async def delete_event_endpoint(event_id: int):
    existing_event = persistence.get_event_by_id(event_id)
    if existing_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    persistence.delete_event(event_id)
    return {"message": "Event deleted successfully"}

@router.get("/export/")
async def export_all_events():
    try:
        events = persistence.get_all_events()
        path = export.from_events(events, "events_calendar")
        return FileResponse(
            path, media_type="text/calendar", filename=path
        )

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
