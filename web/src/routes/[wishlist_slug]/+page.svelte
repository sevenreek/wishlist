<script>
  import Item from './Item.svelte';
  import SquareImage from '$lib/components/SquareImage.svelte';
  import FaGifts from 'svelte-icons/fa/FaGifts.svelte'
  /** @type {import('./$types').PageData} */
  export let data;

</script>

<div class="flex flex-col items-center bg-gray-100 main-content">
  <div class="flex flex-row h-56 shadow-lg w-full bg-white">
    <div class="flex justify-center content-center">
      <SquareImage src="{data.wishlist.image_url}" alt="{data.wishlist.name}" size={56}>
        <FaGifts slot="placeholder"/>
      </SquareImage>
    </div>
    <div class="p-2 ml-2 flex flex-col justify-center content-center">
      <h1 class="text-4xl">{data.wishlist.name}</h1>
      <div class="py-2">{@html data.wishlist.description}</div>
    </div>
  </div>

  <div class="flex flex-col gap-4 mt-8 mx-1 min-w-full md:min-w-[80%] lg:min-w-[60%] xl:min-w-[50%] m-2">
    { #each data.items as item }
      <Item data={item}/>
    {/each}
  </div>
</div>
