from fastapi import HTTPException
from fastapi.routing import APIRouter
from fastapi.responses import FileResponse

from app.models import CalendarConfig, Event
from app.generate_calendar import generate_calendar_file
from app.persistence import delete_event, get_event_by_id, save_event, update_event
    
router = APIRouter()

@router.post("/generate_calendar/")
async def generate_calendar(config: CalendarConfig):
    try:
        path = generate_calendar_file(config)
        return FileResponse(
            path, media_type="text/calendar", filename=f"{config.calendar_name}.ics"
        )

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/events/")
async def create_event(event: Event):
    save_event(event)
    return {"message": "Event created successfully"}

@router.get("/events/{event_id}")
async def read_event(event_id: int):
    event = get_event_by_id(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/events/{event_id}")
async def update_event_endpoint(event_id: int, event: Event):
    existing_event = get_event_by_id(event_id)
    if existing_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    update_event(event_id, event)
    return {"message": "Event updated successfully"}

@router.delete("/events/{event_id}")
async def delete_event_endpoint(event_id: int):
    existing_event = get_event_by_id(event_id)
    if existing_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    delete_event(event_id)
    return {"message": "Event deleted successfully"}