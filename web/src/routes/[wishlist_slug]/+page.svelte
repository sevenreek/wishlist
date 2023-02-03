<script lang='ts'>
	import FaGifts from 'svelte-icons/fa/FaGifts.svelte';
	import type { PageData } from './$types';

	import SquareImage from '$lib/components/SquareImage.svelte';
    import Input from '$lib/components/Input.svelte';
	import Modal from '$lib/components/Modal.svelte';
    import type {ItemData, WishlistData} from '$lib/api/wishlist'

	import ItemDetails from './ItemDetails.svelte';
	import Item from './Item.svelte';
	export let data: PageData;
	let modalVisible = true;
	const openModal = () => (modalVisible = true);
	const closeModal = () => (modalVisible = false);
    let chosenItem: ItemData | null = null;
    const chooseItem = (item: ItemData) => {
      chosenItem = item;
      openModal();
    }
</script>

<div class="flex flex-col items-center bg-gray-100 main-content">
	<div class="flex flex-row h-56 shadow-lg w-full bg-white">
		<div class="flex justify-center content-center">
			<SquareImage src={data.image_url} alt={data.name} size={56}>
				<FaGifts slot="placeholder" />
			</SquareImage>
		</div>
		<div class="p-2 ml-2 flex flex-col justify-center content-center">
			<h1 class="text-4xl">{data.name}</h1>
			<div class="py-2">{@html data.description}</div>
		</div>
	</div>

	<div
		class="flex flex-col gap-4 mt-8 mx-1 min-w-full md:min-w-[80%] lg:min-w-[60%] xl:min-w-[50%] m-2"
	>
		{#each data.items as item}
			<Item on:reserve={() => chooseItem(item)} data={item} />
		{/each}
	</div>
</div>
{#if modalVisible && chosenItem}
	<Modal on:close={closeModal} title='Confirm reservation'>
      <ItemDetails data={chosenItem}/>
	</Modal>
{/if}
