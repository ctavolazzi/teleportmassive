<script lang="ts">
	import '../app.css';
	import { page } from '$app/stores';
</script>

<div class="app">
	<header class="header">
		<div class="header-content">
			<h1 class="title">Teleport Massive</h1>
			<nav class="nav">
				<a
					href="/"
					class="nav-link"
					class:active={$page.url.pathname === '/'}
				>
					Home
				</a>
				<a
					href="/game"
					class="nav-link"
					class:active={$page.url.pathname === '/game'}
				>
					Play
				</a>
				<a
					href="/about"
					class="nav-link"
					class:active={$page.url.pathname === '/about'}
				>
					About
				</a>
			</nav>
		</div>
	</header>

	<main class="main">
		<div class="content">
			<slot />
		</div>
	</main>

	<footer class="footer">
		<div class="footer-content">
			<p>&copy; {new Date().getFullYear()} Teleport Massive. All rights reserved.</p>
		</div>
	</footer>
</div>

<style>
	.app {
		min-height: 100vh;
		display: flex;
		flex-direction: column;
		background-color: #1a1a1a;
		color: #ffffff;
	}

	.header {
		background-color: #2a2a2a;
		padding: 1rem 0;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
	}

	.header-content {
		max-width: 1200px;
		margin: 0 auto;
		padding: 0 1rem;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.title {
		font-size: 1.5rem;
		font-weight: bold;
		margin: 0;
		color: #64b5f6;
	}

	.nav {
		display: flex;
		gap: 2rem;
	}

	.nav-link {
		color: #ffffff;
		text-decoration: none;
		font-weight: 500;
		padding: 0.5rem 1rem;
		border-radius: 0.25rem;
		transition: all 0.2s;
	}

	.nav-link:hover {
		color: #64b5f6;
		background-color: rgba(100, 181, 246, 0.1);
	}

	.nav-link.active {
		color: #64b5f6;
		background-color: rgba(100, 181, 246, 0.15);
	}

	.main {
		flex: 1;
		padding: 2rem 0;
	}

	.content {
		max-width: 1200px;
		margin: 0 auto;
		padding: 0 1rem;
	}

	.footer {
		background-color: #2a2a2a;
		padding: 1.5rem 0;
		margin-top: auto;
	}

	.footer-content {
		max-width: 1200px;
		margin: 0 auto;
		padding: 0 1rem;
		text-align: center;
		color: #888;
	}
</style>