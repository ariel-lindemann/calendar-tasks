<script lang="ts">
	import EventForm from '$lib/components/EventForm.svelte';
	import EventList from '$lib/components/EventList.svelte';
	import type { Event } from '$lib/types';
	import { createEvents, readEvents } from '$lib/event_crud';
	import { onMount } from 'svelte';

	let events: Event[] = $state([]);
	let loading = $state(false);
	let error = $state('');
	let showForm = $state(false);

	async function onEventChanged() {
		loading = true;
		error = '';
		events = await readEvents();
		loading = false;
	}

	onMount(() => {
		onEventChanged();
	});
</script>

<h1>Calendar Tasks</h1>

<button onclick={() => (showForm = true)}>Add Event</button>

{#if showForm}
	<div class="modal">
		<div class="modal-content">
			<EventForm
				onSubmit={async (event: Array<Event>) => {
					let [success, errorMessage] = await createEvents(event);
					if (success) {
						showForm = false;
					}
					return [success, errorMessage];
				}}
				onCancel={() => (showForm = false)}
				{onEventChanged}
			/>
		</div>
	</div>
{/if}

<button onclick={onEventChanged}>
	{loading ? 'Loading...' : 'Load Events from Backend'}
</button>

{#if error}
	<p style="color: red;">{error}</p>
{/if}

<h2>Upcoming Events</h2>
{#if events.length > 0}
	<EventList {events} {onEventChanged} />
{:else}
	<p>No events loaded yet. Click the button above to fetch events.</p>
{/if}
