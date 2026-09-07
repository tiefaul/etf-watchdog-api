<script lang="ts">
  let {
    ticker_symbol = 'Placeholder',
    company_name = 'Placeholder',
    price = '0',
    shares = '0'
    } = $props()

  const displayRed = (number: string): string => {
    return parseInt(number) >= 0 ? 'green': 'red';
    }
</script>

<div class="card">
  <div class="container">
    <h3><b>{ticker_symbol}</b></h3>
    <p>{company_name}</p>
    <div class="justify-between">
      <span>Current price</span><span style:--color={ displayRed(price) }>${price}</span>
    </div>
    <div class="justify-between">
      <span>Shares</span><span>{shares}</span>
    </div>
  </div>
</div>

<style>
  .card {
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    transition: 0.3s;
    width: 19%;
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

  .container > h3 {
    margin-bottom: 0px;
    margin-top: 10px;
  }

  .container > p {
    font-size: 12px;
    margin-top: 0px;
  }

  .justify-between {
    display: flex;
    justify-content: space-between;
  }

  .justify-between > span {
    color: var(--color);
    font-size: 15px;
    margin-bottom: 8px;
  }
</style>
