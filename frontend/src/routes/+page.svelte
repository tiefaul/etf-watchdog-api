<script lang='ts'>
  import { Card, Switch } from '$lib/components';
  let { data } = $props();
</script>

<div class="switch-container">
  <Switch />
</div>

<div class="card-flex-container">
  {#each data.stocks as { ticker_symbol, price, shares }}
    <Card ticker_symbol={ticker_symbol} price={price} shares={shares}  />
  {/each}
</div>


<style>
  .card-flex-container {
    padding: 0px 10px 10px 10px;
    display: flex;
    flex-wrap: wrap;
    flex-direction: row;
    gap: 20px;
  }

  .switch-container {
    border-radius: 12px;
    width: max-content; 
    background-color: lightgray;
    margin-left: 10px;
  }
</style>
