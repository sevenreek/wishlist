<script lang="ts">
  export let src: string;
  export let alt: string;
  export let size: number;
  const remSize = size/4;
  const pad = remSize/8;
  const borderSize = size/64;
  const iconSize = remSize - 2*pad;
</script>

{#if src}
  <div class="aspect-square h-full">
    <img class="object-cover h-full" style="width:{remSize}rem;" src="{src}" alt="{alt}"/>
  </div>
{:else}
  <div class="flex flex-col justify-center text-gray-300" style="margin-left: {pad}rem; margin-right: {pad}rem;">
    <div class="rounded-full" style="width:{iconSize}rem; height:{iconSize}rem; padding: {pad}rem; border: {borderSize}rem dotted;">
      <slot name="placeholder"/>
    </div>
  </div>
{/if}

