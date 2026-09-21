<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';
  import { ModalButton } from "$lib/components";

	let { children } = $props();
  let showModal: boolean = $state(false);
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Bitcount+Prop+Single:wght@100..900&family=Roboto:ital,wght@0,100..900;1,100..900&display=swap');
  </style>
</svelte:head>


<header class='header-flex-container'>
  <h1>ETF Watchdog</h1>
  <button onclick={() => (showModal = true)}>+ Add Stock</button>
</header>

<ModalButton bind:showModal />

<div>
  <p>Track and manage your investments</p>
  <hr />
</div>


<style>
  .header-flex-container {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin-right: 20px;
    margin-left: 20px;
  }
  .header-flex-container h1 {
    margin-bottom: 0px;
  }
  p {
    margin-top: 0px;
    margin-left: 20px;
  }
  hr {
    margin-bottom: 15px;
  }
</style>


{@render children()}
