<script>
  /** @type {import('./$types').PageData} */
  export let data;
  import MdLockOutline from 'svelte-icons/md/MdLockOutline.svelte'
  import MdOpenInNew from 'svelte-icons/md/MdOpenInNew.svelte'
  import MdChat from 'svelte-icons/md/MdChat.svelte'
</script>

<div class="flex flex-row h-56 mt-4 shadow-lg">
  <div class="flex justify-center content-center">
    <div class="aspect-square h-full">
      <img class="object-cover h-full w-56" src="{data.wishlist.image_url}" alt="Wishlist"/>
    </div>
  </div>
  <div class="p-2 ml-2 flex flex-col justify-center content-center">
    <h1 class="text-4xl">{data.wishlist.name}</h1>
    <div class="py-2">{@html data.wishlist.description}</div>
  </div>
</div>

<div class="flex flex-col gap-4 mt-8 mx-1">
  {#each data.items as { name, image_url, description, quantity, reserved, price, url, message_count }}
    <div class="flex flex-row h-24 shadow-md">
      <div class="aspect-square h-full">
        <img class="object-cover h-full w-24" src="{image_url}" alt="Wishlist"/>
      </div>

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
            <div class="py-2 text-xs">{description}</div>
          {/if}
        </div>
        <div class="flex flex-row gap-3 items-center justify-end">
          <a href="{url}" class="flex flex-row items-center gap-1 justify-end py-1 px-2 border-2 text-gray-500 border-gray-400 border-dashed rounded-full hover:text-orange-700 hover:border-orange-700">
            <span>{message_count}</span>
            <div class="w-5 h-5">
              <MdChat/>
            </div>
          </a>
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
  {/each}
</div>
