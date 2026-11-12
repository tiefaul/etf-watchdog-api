<script lang="ts">
  let { showModal = $bindable() }: { showModal: boolean }  = $props();
  let dialog: HTMLDialogElement;

  $effect(() => {
    if (showModal) dialog.showModal();
    });
</script>


<dialog
  bind:this={dialog}
  onclose={() => (showModal = false)}
  onclick={(e) => { if (e.target === dialog) dialog.close(); }}
>
    <form method="POST" id="stock-creation-form">
      <h2>Add Stock</h2>
      <label for='ticker_symbol'>Ticker Symbol</label>
      <input
        name='ticker_symbol'
        id='ticker_symbol'
        type='text'
        placeholder='e.g AAPL'
        minlength='1'
        maxlength='5'
      />
      <div>
        <button type='submit'>Add Stock</button>
        <button type='button' onclick={() => dialog.close()}>Cancel</button>
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

  button[type=submit] {
    cursor: pointer;
    background-color: black;
    color: var(--primary-color);
    border-radius: 0.5rem;
    padding: 0.5rem 1rem;
    border: 1px;
    font-weight: bold;
    border-style: solid;
  }

  button[type=button] {
    cursor: pointer;
    color: black;
    border-radius: 0.5rem;
    padding: 0.5rem 1rem;
    border: 1px;
    font-weight: bold;
    border-style: solid;
    background-color: var(--primary-color)
  }

  div {
    margin-top: 0.5rem;
  }
</style>
