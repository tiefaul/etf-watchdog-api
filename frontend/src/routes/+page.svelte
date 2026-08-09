<script>
  import { Card } from '$lib/components'
</script>

<div class="flex-container">
  <Card etfName="AAPL" price='100' />
  <Card etfName="SPCX" price='200' />
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
