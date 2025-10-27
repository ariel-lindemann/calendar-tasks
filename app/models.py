from datetime import datetime, timedelta
from pydantic import BaseModel

class Sequence(BaseModel):
    start_date: datetime = datetime.today()
    end_date: datetime = datetime.today() + timedelta(days=365)
    recurrence_interval_days: int = 1
    appointment_names: list[str] = []

class CalendarConfig(BaseModel):
    calendar_name: str = "recurring_appointments"
    sequences: list[Sequence] = []
