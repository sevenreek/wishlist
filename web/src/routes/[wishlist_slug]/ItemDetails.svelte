<script>
	import MdLockOutline from 'svelte-icons/md/MdLockOutline.svelte';
	import MdOpenInNew from 'svelte-icons/md/MdOpenInNew.svelte';
	import FaGift from 'svelte-icons/fa/FaGift.svelte';
	import SquareImage from '$lib/components/SquareImage.svelte';
	import IconButton from '$lib/components/IconButton.svelte';
	import Input from '$lib/components/Input.svelte';
	export let data;
	const { name, image_url, description, quantity, reserved, price, shop_url } = data;
	let values = {
		count: 1,
		name: '',
		anonymous: false
	};
</script>

<div class="flex flex-col w-full">
	<div class="flex flex-col xl:flex-row w-full h-48">
		<SquareImage src={image_url} alt={name} size={48}>
			<FaGift slot="placeholder" />
		</SquareImage>

		<div class="flex flex-col xl:flex-row justify-between items-center w-full px-4 py-1 gap-2">
			<div class="flex flex-col content-center items-start gap-1">
				<h3 class="text-4xl">{name}</h3>
				<div class="flex items-center content-center divide-x-2 gap-1">
					{#if price}
						<span class="text-lg font-semibold text-zinc-700 pr-1">${price}</span>
					{/if}

					{#if shop_url}
						<a href={shop_url} class="pl-1.5 text-gray-600 hover:text-orange-700">
							Visit store
							<div class='inline-block w-3 h-3'>
								<MdOpenInNew slot="icon" />
							</div>
						</a>
						<!--
						<IconButton size="sm" on:click={() => alert('hello')} text="Visit store">
							<MdOpenInNew slot="icon" />
						</IconButton>
            -->
					{/if}
				</div>
				{#if description}
					<div class="text-xs">{description}</div>
				{/if}
			</div>
			<div class="flex flex-col gap-2 justify-end justify-items-stretch">
				<span>
					Reserve
					<Input type="number" width="w-20" bind:value={values.count} />
					<span>out of </span><span>{quantity}&nbsp;requested</span>
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
