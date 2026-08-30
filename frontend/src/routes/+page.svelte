<script lang='ts'>
  import { Card } from '$lib/components';
  let { data } = $props();
  let card = $state(true);
</script>

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
  <div class ="table-container">
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
    display: flex;
    flex-wrap: wrap;
  }

  .switch-container-button {
    border: none;
    background: none;
    padding: 5px 20px;
    text-align: center;
    font-weight: bold;
    display: inline-block;
    font-size: 12px;
    margin: 4px 4px 4px 4px;
    transition-duration: 0.4s;
    cursor: pointer;
  }

  .switch-container-button-active {
    border: none;
    background: none;
    padding: 5px 20px;
    text-align: center;
    font-weight: bold;
    display: inline-block;
    font-size: 12px;
    margin: 4px 4px 4px 4px;
    transition-duration: 0.4s;
    cursor: pointer;
    background-color: white;
    border-radius: 10px;
  }

  .table-container {
    padding: 10px 10px 10px 10px;
    border-style: outset inset inset outset;
    border-radius: 15px;
    margin-top: 20px;
    border-width: 2px;
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
    border-right-style: hidden;
    border-left-style: hidden;
    text-align: left;
    padding: 8px;
  }

  .table-container tbody:nth-child(odd) {
    background-color: #dddddd;
  }
</style>
