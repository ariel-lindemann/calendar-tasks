import sqlite3
import logging
logger = logging.getLogger("uvicorn.app.persistence")

from app.models import Event

db_path = "events.db"

def save_event(event: Event):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                description TEXT,
                location TEXT,
                recurrence TEXT
            )
        """)

        cursor.execute("""
            INSERT INTO events (name, start_date, end_date, description, location, recurrence)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (event.name, event.start_date.isoformat(), event.end_date.isoformat(), event.description, event.location, event.recurrence))

        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Failed to save event: {e}. Event data: {event.model_dump_json()}")
        raise RuntimeError(f"Failed to save event: {e}")

def get_event_by_id(event_id: int) -> Event | None:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, start_date, end_date, description, location, recurrence FROM events WHERE id = ?", (event_id,))
    row = cursor.fetchone()

    conn.close()

    if row:
        return Event(
            id=row[0],
            name=row[1],
            start_date=row[2],
            end_date=row[3],
            description=row[4],
            location=row[5],
            recurrence=row[6]
        )
    return None

def update_event(event_id: int, event: Event):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE events
        SET name = ?, start_date = ?, end_date = ?, description = ?, location = ?, recurrence = ?
        WHERE id = ?
    """, (event.name, event.start_date.isoformat(), event.end_date.isoformat(), event.description, event.location, event.recurrence, event_id))

    conn.commit()
    conn.close()

def delete_event(event_id: int):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))

    conn.commit()
    conn.close()

def get_all_events() -> list[Event]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, start_date, end_date, description, location, recurrence FROM events")
    rows = cursor.fetchall()

    conn.close()

    events = []
    for row in rows:
        events.append(Event(
            id=row[0],
            name=row[1],
            start_date=row[2],
            end_date=row[3],
            description=row[4],
            location=row[5],
            recurrence=row[6]
        ))
    return events