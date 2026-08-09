<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';
  import { Header } from '$lib/components';
	let { children } = $props();
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Bitcount+Prop+Single:wght@100..900&family=Roboto:ital,wght@0,100..900;1,100..900&display=swap');
  </style>
</svelte:head>

<Header />

{@render children()}
