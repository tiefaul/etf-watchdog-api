<script lang='ts'>
  import { Card } from '$lib/components';
  let { data } = $props();
  let card = $state(true);
</script>


<main>
  <div class="switch-container">
    <button class="switch-container-button {card ? 'switch-container-button-active' : 'switch-container-button'}" onclick={() => card = true}>Card View</button>
    <button class="switch-container-button {card ? 'switch-container-button' : 'switch-container-button-active'}" onclick={() => card = false}>Table View</button>
  </div>
  {#if card}
    <div class="card-flex-container">
      {#each data.stocks as { ticker_symbol, price, shares, company_name }}
        <Card {ticker_symbol} {price} {shares} {company_name} />
      {/each}
    </div>
  {:else}
    <div class="table-container">
      <h3>Stock Holdings</h3>
        <table>
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Company Name</th>
              <th>Closing Price</th>
              <th>Shares</th>
            </tr>
          </thead>
          {#each data.stocks as { ticker_symbol, price, shares, company_name }}
            <tbody>
              <tr>
                <td>{ticker_symbol}</td>
                <td>{company_name}</td>
                <td>{price}</td>
                <td>{shares}</td>
              </tr>
            </tbody>
          {/each}
      </table>
    </div>
  {/if}
</main>


<style>
  .card-flex-container {
    padding: 0px 0.625rem 10px 0.625rem;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(12rem, 25rem));
    gap: 1.25rem;
  }

  .switch-container {
    border-radius: 0.625rem;
    width: max-content;
    background-color: lightgray;
    margin-left: 0.625rem;
    display: flex;
    flex-wrap: wrap;
  }

  .switch-container-button {
    border: none;
    background: none;
    padding: 0.313rem 1.25rem;
    text-align: center;
    font-weight: bold;
    display: inline-block;
    font-size: 0.75rem;
    margin: 0.25rem 0.25rem 0.25rem 0.25rem;
    transition-duration: 0.4s;
    cursor: pointer;
  }

  .switch-container-button-active {
    border: none;
    background: none;
    padding: 0.313rem 1.25rem;
    text-align: center;
    font-weight: bold;
    display: inline-block;
    font-size: 0.75rem;
    margin: 0.25rem 0.25rem 0.25rem 0.25rem;
    transition-duration: 0.4s;
    cursor: pointer;
    background-color: white;
    border-radius: 0.625rem;
  }

  .table-container {
    padding: 0.625rem 0.625rem 0.625rem 0.625rem ;
    border-style: outset inset inset outset;
    border-radius: 0.938rem;
    margin-top: 1.25rem;
    border-width: 0.125rem;
  }

  .table-container h3 {
    margin-top: 0px;
  }

  .table-container table {
    font-family: arial, sans-serif;
    border-collapse: collapse;
    width: 100%;
    border-left-style: hidden;
    border-right-style: hidden;
  }

  .table-container td, th {
    border: 1px solid #dddddd;
    border-left-style: hidden;
    text-align: left;
    padding: 0.5rem;
  }

  .table-container tbody:nth-child(odd) {
    background-color: #dddddd;
  }
</style>
