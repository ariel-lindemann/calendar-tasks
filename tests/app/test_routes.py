from fastapi.testclient import TestClient
from app.main import app
from app.models import Event
import app.persistence as persistence
import pytest

client = TestClient(app)

normal_event = {
    "name": "Test Event",
    "start_date": "2024-01-10T10:00:00",
    "end_date": "2024-01-10T12:00:00",
    "description": "A test event",
    "location": "Test Location",
    "recurrence": None
}

event_missing_field = {
    "start_date": "2024-01-10T10:00:00",    
    "end_date": "2024-01-10T12:00:00",
    "description": "A test event",
    "location": "Test Location",
    "recurrence": None
}

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200

def test_version_endpoint():
    response = client.get("/version")
    assert response.status_code == 200
    assert "version" in response.json()

def test_generate_calendar():
    config = {
        "calendar_name": "Test Calendar",
        "sequences": [
            {
                "appointment_names": ["Appointment 1", "Appointment 2"],
                "start_date": "2024-01-01T00:00:00",
                "end_date": "2024-01-10T00:00:00",
                "recurrence_interval_days": 2
            },
            {
                "appointment_names": ["Appointment 1", "Appointment 3"],
                "start_date": "2024-01-11T00:00:00",
                "end_date": "2024-01-20T00:00:00",
                "recurrence_interval_days": 5
            }
        ]
    }
    response = client.post("/generate_calendar/", json=config)
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/calendar; charset=utf-8"
    assert ".ics" in response.headers["content-disposition"]

@pytest.fixture(autouse=True)
def setup_test_db(monkeypatch, tmp_path):
    test_db_path = str(tmp_path / "test_events.db")
    monkeypatch.setattr(persistence, "db_path", test_db_path)
    persistence.init_db()
    yield

def test_create_event_success():
    response = client.post("/events/", json=[normal_event])
    assert response.status_code == 200

def test_create_event_missing_field():
    response = client.post("/events/", json=[event_missing_field])
    assert response.status_code == 422  # Unprocessable content

def test_create_event_multiple():
    response = client.post("/events/", json=[normal_event, normal_event])
    assert response.status_code == 200

def test_read_events():
    response = client.get("/events/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 0  # Initially empty

def test_read_multiple_events():
    num_events = 25
    for _ in range(num_events):
        persistence.save_event(Event(**normal_event))
    response = client.get("/events/")
    assert response.status_code == 200
    assert len(response.json()) == num_events

def test_read_event_not_found():
    response = client.get("/events/9999/")
    assert response.status_code == 404

def test_get_event_by_id():
    persistence.save_event(Event(**normal_event))
    response = client.get("/events/1/")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Event"

def test_update_event_success():
    persistence.save_event(Event(**normal_event))
    updated_event = normal_event.copy()
    updated_event["name"] = "Updated Event"
    response = client.put("/events/1/", json=updated_event)
    assert response.status_code == 200
    persistence.get_event_by_id(1)
    assert persistence.get_event_by_id(1).name == "Updated Event" # type: ignore

def test_update_event_not_found():
    updated_event = normal_event.copy()
    updated_event["name"] = "Updated Event"
    response = client.put("/events/9999/", json=updated_event)
    assert response.status_code == 404

def test_delete_event_success():
    persistence.save_event(Event(**normal_event))
    response = client.delete("/events/1/")
    assert response.status_code == 200
    assert persistence.get_event_by_id(1) is None

def test_delete_event_not_found():
    response = client.delete("/events/9999/")
    assert response.status_code == 404

def test_export_all_events():
    persistence.save_event(Event(**normal_event))
    response = client.get("/export/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/calendar; charset=utf-8"
    assert ".ics" in response.headers["content-disposition"]