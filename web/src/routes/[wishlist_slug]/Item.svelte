<script>
  import MdLockOutline from 'svelte-icons/md/MdLockOutline.svelte'
  import MdOpenInNew from 'svelte-icons/md/MdOpenInNew.svelte'
  import MdChat from 'svelte-icons/md/MdChat.svelte'
  import FaGift from 'svelte-icons/fa/FaGift.svelte'
  import SquareImage from '$lib/components/SquareImage.svelte'
  import IconButton from '$lib/components/IconButton.svelte';
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();
  const reserve = () => dispatch('reserve');
  export let data;
  const { name, image_url, description, quantity, reserved, price, shop_url } = data;
</script>

<div class="flex flex-row h-24 shadow-md w-full bg-white">
  <SquareImage src="{image_url}" alt="{name}" size={24}>
    <FaGift slot="placeholder"/>
  </SquareImage>


  <div class="flex flex-row justify-between items-center w-full px-4 py-1">
    <div class="flex flex-col justify-center content-center">
      {#if shop_url}
        <a href="{shop_url}" class="flex flex-row items-center gap-2 hover:text-orange-700 group">
          <h3 class="text-2xl">{name}</h3>
            <span class="py-0.5 px-0.5 border text-gray-500 border-gray-400 border-dashed rounded-full group-hover:border-orange-700 group-hover:text-orange-700">
              <div class="w-4 h-4"><MdOpenInNew/></div>
            </span>
        </a>
      {:else}
        <h3 class="text-2xl">{name}</h3>
      {/if}
      {#if description}
        <div class="text-xs">{description}</div>
      {/if}
      {#if price}
        <div class="text-xs">${price}</div>
      {/if}
    </div>
    <div class="flex flex-row gap-3 items-center justify-end">
      <IconButton on:click={reserve} text="Reserve" extra="{reserved}/{quantity ? (quantity > 9 ? '#' : quantity) : '∞ '}">
        <MdLockOutline slot="icon"/>
      </IconButton>
    </div>
  </div>
</div>
