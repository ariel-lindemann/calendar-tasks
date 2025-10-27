from datetime import datetime, timedelta
from pydantic import BaseModel, field_validator, model_validator

class Event(BaseModel):
    id: int | None = None
    name: str
    start_date: datetime
    end_date: datetime
    description: str | None = None
    location: str | None = None

    @model_validator(mode="after")
    def end_must_be_after_start(self):
        if self.end_date < self.start_date:
            raise ValueError("end_date must be after start_date")
        return self

class Sequence(BaseModel):
    start_date: datetime = datetime.today()
    end_date: datetime = datetime.today() + timedelta(days=365)
    recurrence_interval_days: int = 1
    appointment_names: list[str] = []

    @model_validator(mode="after")
    def end_must_be_after_start(self):
        if self.end_date <= self.start_date:
            raise ValueError("end_date must be after start_date")
        return self

    @field_validator("recurrence_interval_days")
    def recurrence_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("recurrence_interval_days must be positive")
        return v

class CalendarConfig(BaseModel):
    calendar_name: str = "recurring_appointments"
    sequences: list[Sequence] = []
