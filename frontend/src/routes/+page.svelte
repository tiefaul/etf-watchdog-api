<script lang='ts'>
  import { Card } from '$lib/components';
  let { data } = $props();
</script>

<div class="flex-container">
  {#each data.stocks as { ticker_symbol, price, shares }}
    <Card ticker_symbol={ticker_symbol} price={price} shares={shares}  />
  {/each}
</div>

<style>
  .flex-container {
    padding: 10px 10px 10px 10px;
    display: flex;
    flex-wrap: wrap;
    flex-direction: row;
    gap: 20px;
  }
</style>
