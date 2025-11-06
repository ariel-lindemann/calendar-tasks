<script lang="ts">
	import type { Event } from '$lib/types';
	import { updateEvent, deleteEvent } from '$lib/event_crud';
	import RecurrenceForm from './RecurrenceForm.svelte';

	let { event, onEventChanged }: { event: Event; onEventChanged: () => void } = $props();
	let showEditPopup: boolean = $state(false);
	let showError: boolean = $state(false);
	let errorMessage: string = $state('');
	let editedEvent: Event = $state({ ...event });

	// for binding local inputs (they don't show properly with Date objects)
	let startDateInput: string = $state(formatDateForInput(event.start_date));
	let endDateInput: string = $state(formatDateForInput(event.end_date));

	function openEditPopup() {
		// Create a fresh copy of the event for editing
		editedEvent = { ...event };
		startDateInput = formatDateForInput(event.start_date);
		endDateInput = formatDateForInput(event.end_date);
		showEditPopup = true;
	}

	function cancelEdit() {
		showEditPopup = false;
	}

	async function saveEdit() {
		editedEvent.start_date = new Date(startDateInput);
		editedEvent.end_date = new Date(endDateInput);
		const [success, errorMessage] = await updateEvent(editedEvent, event.id);
		if (success) {
			event = {
				...editedEvent
			};
			onEventChanged?.();
			showEditPopup = false;
		} else {
			showErrorMessage(errorMessage || 'Failed to update event. Please try again.');
		}
	}

	async function handleDelete() {
		const confirmation = window.confirm('Are you sure you want to delete this event?');
		if (!confirmation) {
			return;
		}
		const success = await deleteEvent(event.id);
		if (success) {
			onEventChanged?.();
		} else {
			showErrorMessage('Failed to delete event. Please try again.');
		}
	}

	function showErrorMessage(message: string) {
		errorMessage = message;
		showError = true;
		setTimeout(() => {
			showError = false;
		}, 3000);
	}

	function formatDateForInput(date: Date): string {
		return date.toISOString().slice(0, 16);
	}
</script>

{#if !showEditPopup}
	<div class="event-view">
		<h3>{event.name}</h3>
		<p>{event.start_date.toLocaleString()} - <br /> {event.end_date.toLocaleString()}</p>
		{#if event.description}
			<p><strong>Description:</strong> <br /> {event.description}</p>
		{/if}
		{#if event.location}
			<p><strong>Location:</strong><br /> {event.location}</p>
		{/if}
		{#if event.recurrence}
			<p><strong>Recurrence:</strong><br /> {event.recurrence}</p>
		{/if}
		<button onclick={handleDelete}>Delete</button>
		<button onclick={openEditPopup}>Edit</button>
		{#if showError}
			<div class="error-message">
				<p>{errorMessage}</p>
			</div>
		{/if}
	</div>
{/if}

{#if showEditPopup}
	<div class="event-view">
		<h3>{editedEvent.name} (Edit)</h3>
		<input type="text" bind:value={editedEvent.name} />
		<input type="datetime-local" bind:value={startDateInput} />
		<input type="datetime-local" bind:value={endDateInput} />
		<textarea bind:value={editedEvent.description}></textarea>
		<input type="text" bind:value={editedEvent.location} />
		Recurrence:
		<RecurrenceForm bind:recurrenceRule={editedEvent.recurrence} />
		<input type="text" bind:value={editedEvent.recurrence} />
		<button onclick={saveEdit}>Save</button>
		<button onclick={cancelEdit}>Cancel</button>
		{#if showError}
			<div class="error-message">
				<p>{errorMessage}</p>
			</div>
		{/if}
	</div>
{/if}

<style>
</style>
