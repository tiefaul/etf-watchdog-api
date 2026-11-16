<script lang='ts'>
  interface SidebarDialogProps {
    showSidebar: boolean,
    ticker_symbol: string
  }

  let {
    showSidebar = $bindable(),
    ticker_symbol = 'Placeholder'
    }: SidebarDialogProps = $props();

  let dialog: HTMLDialogElement;

  $effect(() => {
    if (showSidebar) dialog.showModal();
    });
</script>


<dialog
  bind:this={dialog}
  onclose={() => (showSidebar = false)}
  onclick={(e) => {if (e.target === dialog) dialog.close()}}
  >
  <h1>This is a test: {ticker_symbol}</h1>
</dialog>

<style>
  dialog {
    left: auto;
    height: 100%;
    padding: 2rem 1rem 0.6rem;
    border-left: 1px solid #aaa;
    background: var(--primary-color);
    overflow-y: auto;
    width: 15rem;
    animation: close 200ms forwards;
    transition:
      display 200ms allow-discrete,
      overlay 200ms allow-discrete;
  }

  dialog[open] {
    animation-fill-mode: forwards;
    animation-iteration-count: 1;
    animation-name: dialogEnter;
    animation-timing-function: ease-out;
    animation: open 400ms forwards;
  }

  @keyframes open {
    from {
      translate: 100%;
      }
    to {
      translate: 0%;
      }
  }

  @keyframes close {
    from {
      translate: 0%;
      }
    to {
      translate: 100%;
      }
  }
</style>
