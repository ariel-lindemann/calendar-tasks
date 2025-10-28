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

<style>
	.event-list {
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
		gap: 15px;
		border: 2px solid #ddd;
		width: fit-content;
	}
</style>
