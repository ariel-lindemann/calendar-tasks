import pytest
from app import export
from datetime import datetime

def test_export_to_ical(tmp_path):
    calendar = export.cal_from_events([
        export.Event(
            name="Test Event",
            start_date = datetime(2024, 1, 1),
            end_date = datetime(2024, 1, 2),
        )
    ])

    file_name = tmp_path / "test_calendar"
    file_path = export.create_ical_file(calendar, str(file_name))

    assert file_path == f"{file_name}.ics"
    with open(file_path, "r") as file:
        content = file.read()
        assert "BEGIN:VCALENDAR" in content
        assert "SUMMARY:Test Event" in content
        assert "DTSTART:20240101T000000" in content
        assert "DTEND:20240102T000000" in content