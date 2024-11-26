<script lang="ts">
  import { onMount } from 'svelte';
  import { gameStore } from '$lib/stores/gameStore';
  import StoryMap from '$lib/components/StoryMap.svelte';

  let showMap = false;

  function handleChoice(choiceId: string) {
    gameStore.makeChoice(choiceId);
  }

  function handleNodeSelect(event: CustomEvent) {
    const node = $gameStore.nodes[event.detail.nodeId];
    if (node?.choices?.length === 1) {
      handleChoice(node.choices[0].id);
    }
  }

  onMount(async () => {
    await gameStore.startGame();
    // Enable map by default after game starts
    showMap = true;
  });
</script>

<div class="game-container">
  {#if $gameStore.isLoading}
    <p>Loading your adventure...</p>
  {:else if $gameStore.error}
    <p class="error">{$gameStore.error}</p>
  {:else if $gameStore.currentNode}
    <div class="story-section">
      <h2>{$gameStore.currentNode.title}</h2>
      <p>{$gameStore.currentNode.content}</p>

      {#if $gameStore.currentNode.choices && $gameStore.currentNode.choices.length > 0}
        <div class="choices-section">
          <h3>What will you do?</h3>
          <div class="choice-list">
            {#each $gameStore.currentNode.choices as choice}
              <button
                class="choice-button"
                on:click={() => handleChoice(choice.id)}
              >
                {choice.text}
              </button>
            {/each}
          </div>
        </div>
      {/if}
    </div>

    <button class="toggle-map" on:click={() => showMap = !showMap}>
      {showMap ? 'Hide' : 'Show'} Story Map
    </button>

    {#if showMap}
      <StoryMap on:nodeSelect={handleNodeSelect} />
    {/if}
  {/if}
</div>

<style>
  .game-container {
    max-width: 800px;
    margin: 2rem auto;
    padding: 2rem;
    background: rgba(16, 24, 39, 0.7);
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(10px);
  }

  .story-section {
    background: rgba(30, 41, 59, 0.8);
    padding: 2.5rem;
    border-radius: 8px;
    margin-bottom: 2rem;
    border: 1px solid rgba(100, 181, 246, 0.2);
    transition: all 0.3s ease;
  }

  .story-section:hover {
    border-color: rgba(100, 181, 246, 0.4);
    box-shadow: 0 0 20px rgba(100, 181, 246, 0.1);
  }

  h2 {
    color: #64b5f6;
    margin-bottom: 1.5rem;
    font-size: 2rem;
    text-shadow: 0 0 10px rgba(100, 181, 246, 0.3);
  }

  h3 {
    color: #90caf9;
    margin-bottom: 1rem;
    font-size: 1.2rem;
  }

  p {
    color: #e2e8f0;
    line-height: 1.8;
    margin-bottom: 2rem;
    font-size: 1.1rem;
  }

  .choices-section {
    margin-top: 2.5rem;
  }

  .choice-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .choice-button {
    background: rgba(100, 181, 246, 0.1);
    border: 2px solid rgba(100, 181, 246, 0.3);
    color: #e2e8f0;
    padding: 1.2rem;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 1.1rem;
    text-align: left;
  }

  .choice-button:hover {
    background: rgba(100, 181, 246, 0.2);
    border-color: rgba(100, 181, 246, 0.5);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(100, 181, 246, 0.2);
  }

  .choice-button:active {
    transform: translateY(0);
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .story-section {
    animation: fadeIn 0.5s ease-out;
  }

  .toggle-map {
    width: 100%;
    padding: 1rem;
    background: rgba(100, 181, 246, 0.1);
    border: 2px solid rgba(100, 181, 246, 0.3);
    color: #e2e8f0;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 1rem;
    margin-top: 1rem;
  }

  .toggle-map:hover {
    background: rgba(100, 181, 246, 0.2);
    border-color: rgba(100, 181, 246, 0.5);
  }
</style>