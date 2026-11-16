<script lang="ts">
  import { deleteStock } from '$lib/api/stocks';

  interface CardProps {
    ticker_symbol: string,
    company_name: string,
    price: string,
    shares: string
  };

  let {
    ticker_symbol = 'Placeholder',
    company_name = 'Placeholder',
    price = '0',
    shares = '0'
    }: CardProps = $props()


  // Example of what you can do with a function and CSS.
  // const displayRed = (number: string): string => {
  //   return parseInt(number) >= 0 ? 'green': 'red';
  //   }
</script>

<!-- <div class='card' role="button" onclick={()=> showSidebar = !showSidebar} {onkeydown} tabindex='0'> -->
  <div class='justify-between'>
    <h3><b id='ticker'>{ticker_symbol}</b></h3>
    <button
      id="trash"
      class="fa-solid fa-trash"
      title="remove"
      onclick={ async () => {
        await deleteStock(ticker_symbol);
        window.location.reload();
        }}>
    </button>
  </div>
  <p>{company_name}</p>
  <div class='justify-between'>
    <span>Current price</span>
    <span style:color=#118C4F>${price}</span>
    <!-- <span style:--color={ displayRed(price) }>${price}</span> -->
  </div>
  <div class='justify-between'>
    <span>Shares</span>
    <span>{shares}</span>
  </div>
<!-- </div> -->

<!-- <SidebarDialog bind:showSidebar {ticker_symbol} /> -->


<style>
  #trash {
    background: none;
    border: none;
    cursor: pointer;
    color: #b91c1c;
  }

  h3 {
    margin-bottom: 0px;
    margin-top: 0.625rem;
  }

  p {
    font-size: 0.75rem;
    margin-top: 0px;
  }

  .justify-between {
    display: flex;
    justify-content: space-between;
  }

  span {
    /* color: var(--color); */
    font-size: 0.938rem;
    margin-bottom: 0.5rem;
  }
</style>
