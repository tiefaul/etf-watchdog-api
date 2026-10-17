<script lang='ts'>
  import { fly } from 'svelte/transition';

  let { showSidebar = $bindable() }: { showSidebar: boolean } = $props();
</script>


{#if showSidebar}
  <nav transition:fly={{x:250, opacity:1}}>
    <h1>This is a test</h1>
  </nav>
{/if}

<style>
  nav {
    position: fixed;
    top: 0;
    right: 0;
    height: 100%;
    padding: 2rem 1rem 0.6rem;
    border-left: 1px solid #aaa;
    background: #fff;
    overflow-y: auto;
    width: 10rem;
  }
</style>
