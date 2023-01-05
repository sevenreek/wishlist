<script>
	import { page } from '$app/stores';
</script>

<header>

	<nav class="flex justify-between bg-zinc-800 border-gray-200 px-2 sm:px-4 py-2.5 w-full">
		<ul class="text-white flex flex-row space-x-4 text-xl w-full">
			<li aria-current={$page.url.pathname === '/' ? 'page' : undefined}>
				<a href="/">Home</a>
			</li>
		</ul>
		<ul class="text-white justify-end flex flex-row space-x-4 text-xl w-full">
			<li aria-current={$page.url.pathname === '/login' ? 'page' : undefined}>
				<a href="/login">Sign in</a>
			</li>
			<li aria-current={$page.url.pathname === '/register' ? 'page' : undefined}>
				<a href="/register">Register</a>
			</li>
		</ul>
	</nav>

</header>

<style lang="postcss">
  a {
    @apply hover:underline;
  }
</style>
