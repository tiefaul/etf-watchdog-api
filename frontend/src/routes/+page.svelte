<script>
  import { Card } from '$lib/components'
</script>

<div class="flex-container">
  <Card etfName="AAPL" />
  <Card etfName="SPCX" />
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
