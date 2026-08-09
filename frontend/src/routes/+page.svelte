<script>
  import { Card } from '$lib/components'
</script>

<div class="flex-container">
  <Card ticker_symbol="AAPL" price='100' shares='50' />
  <Card ticker_symbol="SPCX" price='200' shares='10' />
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
