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

<div class='card'>
  <div class='container'>
    <h3><b>{ticker_symbol}</b></h3>
    <p>{company_name}</p>
    <div class='justify-between'>
      <span>Current price</span><span style:--color={ displayRed(price) }>${price}</span>
    </div>
    <div class='justify-between'>
      <span>Shares</span><span>{shares}</span>
    </div>
  </div>
</div>

<style>
  .card {
    box-shadow: 0 0.25rem 0.5rem 0 rgba(0,0,0,0.2);
    transition: 0.3s;
    border-radius: 0.938rem;
    margin-top: 1.25rem;
    margin-bottom: 1.25rem;
  }

  .card:hover {
    box-shadow: 0 0.5rem 1rem 0 rgba(0,0,0,0.2);
  }

  .container {
    padding: 0.125rem 1rem;
    overflow-wrap: break-word;
  }

  .container > h3 {
    margin-bottom: 0px;
    margin-top: 0.625rem;
  }

  .container > p {
    font-size: 0.75rem;
    margin-top: 0px;
  }

  .justify-between {
    display: flex;
    justify-content: space-between;
  }

  .justify-between > span {
    color: var(--color);
    font-size: 0.938rem;
    margin-bottom: 0.5rem;
  }
</style>
