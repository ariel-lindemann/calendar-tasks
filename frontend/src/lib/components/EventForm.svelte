<script lang="ts">
	import type { Event } from '$lib/types';

	// Accept a function prop for handling submission
	let {
		onSubmit,
		onEventChanged
	}: { onSubmit: (event: Array<Event>) => Promise<boolean>; onEventChanged: () => void } = $props();

	let showError: boolean = $state(false);
	let errorMessage: string = $state('');

	let name: string = $state('');
	let start_date: string = $state('');
	let end_date: string = $state('');
	let description: string = $state('');
	let location: string = $state('');
	let recurrence: string = $state('');

	async function showErrorMessage(message: string) {
		errorMessage = message;
		showError = true;
		setTimeout(() => {
			showError = false;
		}, 3000);
	}

	async function handleSubmit() {
		if (!name || !start_date || !end_date) {
			alert('Please fill in all required fields.');
			return;
		}

		const event: Event = {
			name,
			start_date: new Date(start_date),
			end_date: new Date(end_date),
			description: description || undefined,
			location: location || undefined,
			recurrence: recurrence || undefined
		};

		let success = await onSubmit([event]);

		if (success) {
			// Clear form after submission
			name = '';
			start_date = '';
			end_date = '';
			description = '';
			location = '';
			recurrence = '';
			onEventChanged?.();
		} else {
			showErrorMessage('Failed to create event. Please try again.');
		}
	}
</script>

<div class="event-form">
	<h3>New Event</h3>
	<form>
		<label>
			Name:
			<input type="text" name="name" bind:value={name} required />
		</label>

		<label>
			Start Date:
			<input type="datetime-local" name="start_date" bind:value={start_date} required />
		</label>

		<label>
			End Date:
			<input type="datetime-local" name="end_date" bind:value={end_date} required />
		</label>

		<label>
			Description:
			<textarea name="description" bind:value={description}></textarea>
		</label>

		<label>
			Location:
			<input type="text" name="location" bind:value={location} />
		</label>

		<label>
			Recurrence:
			<input type="text" name="recurrence" bind:value={recurrence} />
		</label>

		<button type="submit" onclick={handleSubmit}>Create Event</button>
		{#if showError}
			<div class="error-message">
				{errorMessage}
			</div>
		{/if}
	</form>
</div>
