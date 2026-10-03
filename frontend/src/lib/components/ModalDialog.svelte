<script lang="ts">
  let { showModal = $bindable() }: { showModal: boolean }  = $props();
  let dialog = $state() as HTMLDialogElement;

  $effect(() => {
    if (showModal) dialog.showModal();
    });
</script>


<dialog
  bind:this={dialog}
  onclose={() => (showModal = false)}
  onclick={(e) => { if (e.target === dialog) dialog.close(); }}
>
    <form method="POST">
      <h2>Add Stock</h2>
      <label for='ticker_symbol'>Ticker Symbol</label>
      <input name='ticker_symbol' id='ticker_symbol' type='text' placeholder='e.g AAPL'>
      <div>
        <input type='submit' value='Add Stock'>
        <button onclick={() => dialog.close()}>Cancel</button>
      </div>
    </form>
</dialog>


<style>
  dialog {
    border-radius: 0.625rem;
  }

  h2 {
    margin-top: 0;
  }

  label {
    font-weight: bold;
    display: block;
    margin-bottom: 0.5rem;
  }

  input[type=text] {
    width: 80%;
    display: inline-block;
    border-radius: 0.5rem;
    padding: 0.5rem 1rem;
    border: None;
    background: #EEEEEE;
  }

  input[type=submit] {
    cursor: pointer;
    background-color: black;
    color: white;
    border-radius: 0.5rem;
    padding: 0.5rem 1rem;
    border: 1px;
    font-weight: bold;
    border-style: solid;
  }


  button {
    cursor: pointer;
    color: black;
    border-radius: 0.5rem;
    padding: 0.5rem 1rem;
    border: 1px;
    font-weight: bold;
    border-style: solid;
  }

  div {
    margin-top: 0.5rem;
  }
</style>
