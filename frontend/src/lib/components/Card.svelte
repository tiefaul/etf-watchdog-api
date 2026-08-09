<script lang="ts">
  let {
    etfName = 'Placeholder',
    price = '0'
    } = $props()

  const displayRed = (number: string): string => {
    return parseInt(number) >= 0 ? 'green': 'red';
    }
</script>

<div class="card">
  <div class="container">
    <h4><b>{etfName}</b></h4>
    <p style:--font-size="12px">company name</p>
    <div class="justify-between">
      <span>Current price</span><span style:--color={ displayRed(price) }>${price}</span>
    </div>
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

.container > h4 {
  margin-bottom: 0px;
  margin-top: 10px;
}

.container > p {
  font-size: var(--font-size);
  margin-top: 0px;
}

.justify-between {
  display: flex;
  font-size: var(--font-side);
  color: ver(--color);
  justify-content: space-between;
}

.justify-between > span {
  color: var(--color);
  margin-bottom: 8px;
}
</style>
