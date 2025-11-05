<script lang="ts">
	import { daily } from '$lib/recurrence_rules.ts';
	export let recurrenceRule: string = '';
	let interval: number = 1;
</script>

<div class="recurrence-form">
	<select id="recurrence" bind:value={recurrenceRule}>
		<option value="">None</option>
		<option value={daily(interval)}>Daily</option>
	</select>
	<input type="number" min="1" max="365" bind:value={interval} placeholder="Interval (days)" />
</div>

<style>
	.recurrence-form {
		display: flex;
		gap: 0.5rem;
		align-items: center;
	}
</style>
