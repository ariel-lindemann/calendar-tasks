<script lang="ts">
	import EventView from './EventView.svelte';
	import type { Event } from '$lib/types';

	let { events, onEventChanged }: { events: Event[]; onEventChanged: () => void } = $props();
</script>

<div class="event-list">
	{#each events as event}
		<EventView {event} {onEventChanged} />
	{/each}
</div>
