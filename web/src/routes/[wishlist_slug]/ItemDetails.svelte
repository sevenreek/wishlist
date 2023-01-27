<script>
	import MdLockOutline from 'svelte-icons/md/MdLockOutline.svelte';
	import MdOpenInNew from 'svelte-icons/md/MdOpenInNew.svelte';
	import FaGift from 'svelte-icons/fa/FaGift.svelte';
	import SquareImage from '$lib/components/SquareImage.svelte';
	import IconButton from '$lib/components/IconButton.svelte';
	export let data;
	const { name, image_url, description, quantity, reserved, price, shop_url } = data;
</script>

<div class="flex flex-col w-full">
	<div class="flex flex-col xl:flex-row w-full h-48">
		<SquareImage src={image_url} alt={name} size={48}>
			<FaGift slot="placeholder" />
		</SquareImage>

		<div class="flex flex-col xl:flex-row justify-between items-center w-full px-4 py-1 gap-2">
			<div class="flex flex-col content-center items-start gap-1">
				<h3 class="text-3xl">{name}</h3>
				<div class="flex items-center content-center">
					{#if price}
						<span class="text-lg font-semibold text-green-700 pr-1">${price}</span>
					{/if}

					{#if shop_url}
						<IconButton size="sm" on:click={() => alert('hello')} text="Visit store">
							<MdOpenInNew slot="icon" />
						</IconButton>
					{/if}
				</div>
				{#if description}
					<div class="text-xs">{description}</div>
				{/if}
			</div>
			<div class="flex flex-col gap-2 justify-end justify-items-stretch">
				<span>
					Reserve
					<input
						class="inline w-16 text-center pl-4 mx-1 border border-slate-200 p-1 rounded-lg"
						type="number"
						placeholder="1"
					/>
					<span>out of </span><span>{quantity} requested</span>
				</span>
				<div class="flex flex-row items-center gap-2">
					<span class="grow-0">as</span>
					<input
						class="border p-1 rounded-lg inline-block w-100 grow"
						type="text"
						placeholder="John Doe"
					/>
				</div>
				<span>
					or
					<label class="text-gray-500">
						<input class="inline mr-2 ml-1" type="checkbox" />Reserve anonymously
					</label>
				</span>
				<IconButton size="lg" on:click={() => alert('hello')} text="Confirm reservation">
					<MdLockOutline slot="icon" />
				</IconButton>
			</div>
		</div>
	</div>
</div>
