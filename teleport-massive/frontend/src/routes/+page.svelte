<script lang="ts">
  import { onMount } from 'svelte';

  let isLoaded = false;

  onMount(() => {
    isLoaded = true;
  });
</script>

<div class="home-container" class:loaded={isLoaded}>
  <section class="hero">
    <h1 class="hero-title">Welcome to Teleport Massive</h1>
    <p class="hero-subtitle">An interactive text adventure where your choices shape the story</p>
    <div class="cta-buttons">
      <a href="/game" class="cta-button primary">Start Your Adventure</a>
      <a href="/about" class="cta-button secondary">Learn More</a>
    </div>
  </section>

  <section class="features">
    <h2 class="section-title">Features</h2>
    <div class="feature-grid">
      <div class="feature-card">
        <div class="feature-icon">🎮</div>
        <h3>Interactive Story</h3>
        <p>Every choice matters in this branching narrative adventure</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">💾</div>
        <h3>Save Progress</h3>
        <p>Continue your journey from where you left off</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🌟</div>
        <h3>Multiple Endings</h3>
        <p>Discover different outcomes based on your decisions</p>
      </div>
    </div>
  </section>
</div>

<style>
  .home-container {
    opacity: 0;
    transform: translateY(20px);
    transition: all 0.5s ease-out;
  }

  .loaded {
    opacity: 1;
    transform: translateY(0);
  }

  .hero {
    text-align: center;
    padding: 4rem 1rem;
    background: linear-gradient(to bottom, #2a2a2a, #1a1a1a);
    border-radius: 1rem;
    margin-bottom: 4rem;
  }

  .hero-title {
    font-size: 3rem;
    color: #64b5f6;
    margin-bottom: 1rem;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }

  .hero-subtitle {
    font-size: 1.25rem;
    color: #ffffff;
    margin-bottom: 2rem;
    opacity: 0.9;
  }

  .cta-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
  }

  .cta-button {
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    font-weight: 500;
    text-decoration: none;
    transition: all 0.2s;
  }

  .cta-button.primary {
    background-color: #64b5f6;
    color: #ffffff;
  }

  .cta-button.primary:hover {
    background-color: #42a5f5;
    transform: translateY(-2px);
  }

  .cta-button.secondary {
    background-color: rgba(100, 181, 246, 0.1);
    color: #64b5f6;
    border: 2px solid #64b5f6;
  }

  .cta-button.secondary:hover {
    background-color: rgba(100, 181, 246, 0.2);
    transform: translateY(-2px);
  }

  .features {
    padding: 2rem 0;
  }

  .section-title {
    text-align: center;
    font-size: 2rem;
    color: #64b5f6;
    margin-bottom: 2rem;
  }

  .feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    padding: 1rem;
  }

  .feature-card {
    background-color: #2a2a2a;
    padding: 2rem;
    border-radius: 1rem;
    text-align: center;
    transition: transform 0.2s;
  }

  .feature-card:hover {
    transform: translateY(-5px);
  }

  .feature-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
  }

  .feature-card h3 {
    color: #64b5f6;
    margin-bottom: 0.5rem;
  }

  .feature-card p {
    color: #ffffff;
    opacity: 0.8;
  }

  @media (max-width: 768px) {
    .hero-title {
      font-size: 2rem;
    }

    .hero-subtitle {
      font-size: 1rem;
    }

    .cta-buttons {
      flex-direction: column;
    }

    .feature-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
