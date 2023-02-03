<script lang="ts">
  export let src: string;
  export let alt: string;
  export let size: number;
  const remSize = size/4.0;
  const pad = remSize/8.0;
  const borderSize = size/64.0;
  const iconSize = remSize - 2*pad;
  const imageSizing = `width:${remSize}rem; height:${remSize}rem;`;
  const iconSizing = `width:${iconSize}rem; height:${iconSize}rem;`;
</script>

{#if src}
  <div class="flex justify-center aspect-square bg-cover" style="{imageSizing} background-image: url('{src}')"></div>
{:else if $$slots.placeholder}
  <div class="flex flex-col justify-center items-center text-gray-300" style="padding: {pad}rem;">
    <div class="rounded-full" style="{iconSizing} padding: {pad}rem; border: {borderSize}rem dotted;">
      <slot name="placeholder"/>
    </div>
  </div>
{/if}

