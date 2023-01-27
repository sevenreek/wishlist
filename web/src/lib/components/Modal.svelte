<script lang="ts">
	export let title: string = '';
	import FaTimes from 'svelte-icons/fa/FaTimes.svelte';
	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();
	const close = () => dispatch('close');
	const handleKeydown = (e: KeyboardEvent) => {
		if (e.key === 'Escape') {
			close();
			return;
		}
	};
	let modal;
</script>

<svelte:window on:keydown={handleKeydown} />

<div class="fixed inset-0 w-screen h-screen bg-black opacity-60" on:click={close} />

<div
	class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white w-full sm:w-5/6 md:w-4/6 lg:w-[calc(100%-40rem)] max-w-3xl overflow-auto rounded-md"
	role="dialog"
	aria-modal="true"
	bind:this={modal}
>
	<div class="flex flex-row-reverse justify-between items-center pl-3 pr-4 py-2 shadow-sm">
		<button on:click={close} class="w-5 h-5 text-gray-500 hover:text-gray-900">
			<FaTimes />
		</button>
		{#if $$slots.header}
			<slot name="header" />
		{:else if title}
			<div class="text-md font-semibold">{title}</div>
		{/if}
	</div>
	<div class="flex flex-col p-4">
		<slot />
	</div>
</div>
