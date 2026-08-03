<script lang="ts">
  let { etfName } = $props()
</script>

<div class="card">
  <div class="container">
    <h4><b>{etfName}</b></h4>
    <p>This is placeholder data for the time being</p>
  </div>
</div>

<style>
  .card {
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
  transition: 0.3s;
  width: 20%;
  border-radius: 15px;
  margin-top: 20px;
  margin-bottom: 20px;
}

.card:hover {
  box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
}

.container {
  padding: 2px 16px;
  overflow-wrap: break-word;
}
</style>
