<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

{@render children?.()}

<style>
	:global {
		body {
			background-color: #f3b894;
			font-family: 'Georgia', serif;
			line-height: 1.2;
		}
		.event-form {
			border: 2px solid #ccc;
			background-color: #f0f0f0;
			width: 400px;
		}

		.event-form h2 {
			margin-top: 0;
		}
		.event-form label {
			display: block;
		}
		.event-form input,
		.event-form textarea {
			width: 100%;
			box-sizing: border-box;
		}
		.error-message {
			color: red;
			font-weight: bold;
			margin-top: 10px;
		}
	}
</style>
