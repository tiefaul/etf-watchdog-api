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
  <div>
    <form method="POST">
      <label for='ticker_symbol'>
        Ticker Symbol
        <input name='ticker_symbol' id='ticker_symbol' type='text'>
      </label>
      <button>Submit</button>
    </form>
  </div>
  <div>
    <button onclick={() => dialog.close()}>close modal</button>
  </div>
</dialog>
