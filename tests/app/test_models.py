import pytest
from app.models import Event
from datetime import datetime

def test_event_is_between_no_recurrence():
    event = Event(
        name="Test Event",
        start_date=datetime(2024, 1, 10, 10, 0),
        end_date=datetime(2024, 1, 10, 12, 0),
        description="A test event",
        location="Test Location",
        recurrence=None
    )
    assert event.is_between(datetime(2024, 1, 9), datetime(2024, 1, 11)) is True
    assert event.is_between(datetime(2024, 1, 11), datetime(2024, 1, 12)) is False


def test_event_is_between_with_recurrence():
    recurrence_rule = "FREQ=DAILY;COUNT=5"  # Daily for 5 occurrences
    event = Event(
        name="Recurring Event",
        start_date=datetime(2024, 1, 10),
        end_date=datetime(2024, 1, 12),
        description="A recurring test event",
        location="Test Location",
        recurrence=recurrence_rule
    )

    assert event.is_between(datetime(2024, 2, 25), datetime(2024, 2, 26)) is False
    assert event.is_between(datetime(2024, 1, 9), datetime(2024, 1, 11)) is True
    