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
			margin-bottom: 10px;
			line-height: 1.2;
		}

		p {
			font-size: 0.75em;
		}

		/* Event Form Styles */
		.event-form {
			border: 2px solid #ccc;
			padding: 10px;
			background-color: #d4f1d4; /* Light green for form */
			width: 200px;
		}

		.event-form h3 {
			margin-top: 0;
			margin-bottom: 12px;
		}

		.event-form label {
			display: block;
			margin-bottom: 10px;
			font-size: 0.75em;
		}

		.event-form input,
		.event-form textarea {
			width: 100%;
			box-sizing: border-box;
			margin-top: 4px;
		}

		.event-form button {
			margin-top: 8px;
		}

		.event-view {
			border: 2px solid black;
			padding: 10px;
			background-color: #f9f9f9;
			width: 200px;
		}

		.event-view h3 {
			font-size: 1.1em;
			margin: 0 0 8px 0;
		}

		.event-view p {
			font-size: 0.85em;
			margin: 4px 0;
			word-wrap: break-word;
		}

		.event-view strong {
			display: inline-block;
			margin-top: 8px;
		}

		.event-view button {
			margin-top: 8px;
			margin-right: 4px;
		}

		.event-list {
			display: flex;
			flex-direction: row;
			flex-wrap: wrap;
			gap: 15px;
			padding: 5px;
			width: fit-content;
		}

		.error-message {
			color: red;
			font-weight: bold;
		}
	}
</style>
