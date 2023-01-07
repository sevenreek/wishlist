<script>
	import Header from './Header.svelte';
    import '../app.css';
</script>

<div class="app h-full">
	<Header />

	<main class="main-content">
		<slot />
	</main>

	<footer>
	</footer>
</div>

<style>
</style>
