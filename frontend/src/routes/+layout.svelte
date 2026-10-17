<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';
  import { ModalDialog } from "$lib/components";

	let { children } = $props();
  let showModal: boolean = $state(false);
</script>


<svelte:head>
  <title>ETF Watchdog</title>
  <link rel="icon" href={favicon} />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.3.1/css/all.css" integrity="sha512-x9WwyMYBnlXMNQ6kQ/Lyzu1NqIhLQKL5Oq6xByfXuRj7s9CskyCbLv/1IjqzJmXwFXWr0ov6jBV7Qbc0hh9nHg==" crossorigin="anonymous" referrerpolicy="no-referrer">
</svelte:head>

<header class='header-flex-container'>
  <h1>ETF Watchdog</h1>
  <button onclick={() => (showModal = true)}>+ Add Stock</button>
</header>
<div>
  <p>Track and manage your investments</p>
  <hr />
</div>

<ModalDialog bind:showModal />

{@render children()}


<style>
	@import url('https://fonts.googleapis.com/css2?family=Bitcount+Prop+Single:wght@100..900&family=Roboto:ital,wght@0,100..900;1,100..900&display=swap');

	:root {
		--primary-color: #fafafa;
		--primary-font: 'Roboto', sans-serif;
	}

  :global(body) {
		background-color: var(--primary-color);
		font-family: var(--primary-font);
  }

  .header-flex-container {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin: 1.25rem 1.25rem 0px 1.25rem;
  }

  .header-flex-container h1 {
    margin-top: 0px;
    margin-bottom: 0px;
  }

  .header-flex-container button {
    border: none;
    background: black;
    color: white;
    font-weight: bold;
    border-radius: 0.625rem;
    height: calc(0.25rem * 9);
    cursor: pointer;
    padding-left: 0.75rem;
    padding-right: 0.75rem;
  }

  p {
    margin-top: 0px;
    margin-left: 1.25rem;
  }

  hr {
    margin-bottom: 0.938rem;
  }
</style>
