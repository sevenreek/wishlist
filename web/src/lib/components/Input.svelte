<script context="module">
	let moduleCounter = 0;
</script>

<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	type InputType = 'email' | 'number' | 'password' | 'text';

	export let value: string | number = '';
	export let label = '';
	export let error = '';
	export let type: InputType = 'text';
	export let className = '';
	export let width = 'w-full';

	const dispatch = createEventDispatcher();
	const handleInput = (evt: Event) => {
		const target = evt.target as HTMLInputElement;
		value = type == 'number' ? parseInt(target.value) : target.value;
		dispatch('input', evt);
	};

	const extraStyle = error ? 'border-red-300 text-red-700 ' : '';
	const labelColor = error ? 'text-red-600 ' : 'text-gray-600';
	const inputID = 'input_' + moduleCounter++;
</script>

<div class="grow inline-block {className}">
	<label class="block text-xs {labelColor} mb-0.5 ml-1.5" for={inputID}>
		{label}
	</label>
	<input
		id={inputID}
		on:change
		on:input={handleInput}
		on:focus
		on:blur
		class="border {width} block {extraStyle} px-2 py-1 rounded-lg"
		{value}
		{type}
		{...$$restProps}
	/>
	{#if error}<span class="block text-red-700 -italic text-sm mt-1">{error}</span>{/if}
</div>
