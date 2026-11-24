<script lang="ts">
  interface SidebarDialogProps {
    showSidebar: boolean,
    sidebarSymbol: string
  }

  let {
    showSidebar = $bindable(),
    sidebarSymbol = ''
    }: SidebarDialogProps = $props();

  let dialog: HTMLDialogElement;
  let timeout: number;


  // Set a timeout for dialog close animation
  const onclick = () => {
    dialog.close();
    if (timeout) clearTimeout(timeout);
    timeout = setTimeout(() => {
      showSidebar = false;
      }, 200);
  }

  $effect(() => {
    if (showSidebar) dialog.showModal();
    });
</script>


<dialog bind:this={dialog}>
  <button aria-label="close sidebar" class="fa-solid fa-x" {onclick}></button>
  <h1>This is a test: {sidebarSymbol}</h1>
</dialog>


<style>
  button {
    cursor: pointer;
    float: right;
    border: none;
    background: none;
  }

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
