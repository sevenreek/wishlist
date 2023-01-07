<script>
  import MdLockOutline from 'svelte-icons/md/MdLockOutline.svelte'
  import MdOpenInNew from 'svelte-icons/md/MdOpenInNew.svelte'
  import MdChat from 'svelte-icons/md/MdChat.svelte'
  import FaGift from 'svelte-icons/fa/FaGift.svelte'
  import SquareImage from '$lib/components/SquareImage.svelte'
  export let data;
  const { name, image_url, description, quantity, reserved, price, url, message_count } = data;
</script>

<div class="flex flex-row h-24 shadow-md w-full bg-white">
  <SquareImage src="{image_url}" alt="{name}" size={24}>
    <FaGift slot="placeholder"/>
  </SquareImage>


  <div class="flex flex-row justify-between items-center w-full px-4 py-1">
    <div class="flex flex-col justify-center content-center">
      {#if url}
        <a href="{url}" class="flex flex-row items-center gap-2 hover:text-orange-700 group">
          <h3 class="text-2xl">{name}</h3>
            <span class="py-0.5 px-0.5 border-2 text-gray-500 border-gray-400 border-dashed rounded-full group-hover:border-orange-700 group-hover:text-orange-700">
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
      <!-- Add this when messages are implemented
      <a href="{url}" class="flex flex-row items-center gap-1 justify-end py-1 px-2 border-2 text-gray-500 border-gray-400 border-dashed rounded-full hover:text-orange-700 hover:border-orange-700">
        <span>{message_count}</span>
        <div class="w-5 h-5">
          <MdChat/>
        </div>
      </a>
      -->
      <a href="#" class="flex flex-row items-center gap-1 justify-end py-1 px-3 border-2 text-gray-700 border-gray-400 border-dashed rounded-full hover:text-orange-700 hover:border-orange-700">
        <span class="text-md text-gray-300">{reserved}/{quantity ? (quantity > 9 ? '#' : quantity) : '∞ '}</span>
        <span>Reserve</span>
        <div class="w-5 h-5">
          <MdLockOutline/>
        </div>
      </a>
    </div>
  </div>
</div>
