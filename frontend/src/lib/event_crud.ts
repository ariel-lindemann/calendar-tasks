import type { Event } from '$lib/types';

const BASE_URL = 'http://localhost:8000';

export async function createEvents(events: Array<Event>): Promise<boolean> {
    try {
        const response = await fetch(`${BASE_URL}/events/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(events.map(evt => ({
                ...evt,
                start_date: evt.start_date.toISOString(),
                end_date: evt.end_date.toISOString()
            })))
        });
        if (!response.ok) {
            throw new Error(`Failed to create event: ${response.statusText}`);
        }
        return true;
    } catch (err) {
        console.error('Error creating event:', err);
        return false;
    }
}

export async function readEvents(): Promise<Array<Event>> {
    const response = await fetch(`${BASE_URL}/events/`);
    if (!response.ok) {
        throw new Error(`Failed to fetch events: ${response.statusText}`);
    }
    const data = await response.json();
    // Convert date strings to Date objects
    return data.map((event: any) => ({
        ...event,
        start_date: new Date(event.start_date),
        end_date: new Date(event.end_date)
    }));
}
export async function updateEvent(updatedEvent: Event, id?: number): Promise<boolean> {
    if (id === undefined) {
        console.error('Event ID is undefined. Cannot update event.');
        return false;
    }
    try {
        const response = await fetch(`${BASE_URL}/events/${id}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                ...updatedEvent,
                start_date: updatedEvent.start_date.toISOString(),
                end_date: updatedEvent.end_date.toISOString()
            })
        });
        if (!response.ok) {
            throw new Error(`Failed to update event: ${response.statusText}`);
        }
        return true;
    } catch (err) {
        console.error('Error updating event:', err);
        return false;
    }
}
export async function deleteEvent(id: number | undefined): Promise<boolean> {
    if (id === undefined) {
        console.error('Invalid event ID');
        return false;
    }
    try {
        const response = await fetch(`${BASE_URL}/events/${id}`, {
            method: 'DELETE'
        });
        if (!response.ok) {
            throw new Error(`Failed to delete event: ${response.statusText}`);
        }
        return true;
    } catch (err) {
        console.error('Error deleting event:', err);
        return false;
    }
}
