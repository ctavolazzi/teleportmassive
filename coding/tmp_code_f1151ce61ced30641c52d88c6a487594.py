import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Game title
TITLE = "Teleport Massive CYOA"

# Scenario setup
start_scenario = {
    "description": "Sam Iker wakes up in a futuristic city, still feeling the sensation of flying around a skyscraper.",
    "choices": [
        "Explore the city streets",
        "Look for a way back to the skyscraper",
        "Find a place to eat",
        "Other..."
    ]
}

# Game state
game_state = {
    "current_scenario": start_scenario,
    "character_stats": {
        "name": "Sam Iker",
        "energy": 100,
        "happiness": 50
    },
    "location": {
        "name": "Futuristic City",
        "is_day_time": True
    },
    "items": [],
    "player_actions": []
}

# Logging action
logging.info(f"Game started with title: '{TITLE}'")
logging.info(f"Initial scenario: {start_scenario['description']}")