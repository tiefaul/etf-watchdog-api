<script lang="ts">
  import { ModalButton } from ".";

  let showModal: boolean = $state(false);
</script>


<header class='header-flex-container'>
  <h1>ETF Watchdog</h1>
  <button onclick={() => (showModal = true)}>+ Add Stock</button>
</header>

<ModalButton bind:showModal />

<div>
  <p>Track and manage your investments</p>
  <hr />
</div>


<style>
  .header-flex-container {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin-right: 20px;
    margin-left: 20px;
  }
  .header-flex-container h1 {
    margin-bottom: 0px;
  }
  p {
    margin-top: 0px;
    margin-left: 20px;
  }
  hr {
    margin-bottom: 15px;
  }
</style>

