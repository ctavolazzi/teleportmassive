import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Game title
TITLE = "Teleport Massive CYOA"

# Sample Scenarios stored within the code for this demonstration
scenarios = {
    "start": {
        "description": "Sam Iker wakes up in a futuristic city, still feeling the sensation of flying around a skyscraper.",
        "choices": [
            "explore the city streets",
            "look for a way back to the skyscraper",
            "find a place to eat",
            "other"
        ],
        "next_scenarios": [
            "city_explore",
            "skyscraper_search",
            "city_eat",
            "custom_action"
        ]
    },
    "city_explore": {
        "description": "Sam explores the bustling city streets, filled with strange and advanced technology.",
        "choices": [
            "talk to a street vendor",
            "enter a neon-lit bar",
            "sit on a bench",
            "other"
        ],
        "next_scenarios": [
            "vendor_talk",
            "bar_entry",
            "bench_rest",
            "custom_action"
        ]
    },
    "skyscraper_search": {
        "description": "Sam searches for a way back to the skyscraper, feeling a strong desire to fly again.",
        "choices": [
            "ask a passerby for directions",
            "search for a taxi",
            "try to climb the building",
            "other"
        ],
        "next_scenarios": [
            "ask_passersby",
            "find_taxi",
            "climb_building",
            "custom_action"
        ]
    },
    "city_eat": {
        "description": "Sam finds a local diner and enjoys a meal, feeling refreshed and ready for more adventure.",
        "choices": [
            "ask the waiter for recommendations",
            "explore the diner further",
            "leave a good tip",
            "other"
        ],
        "next_scenarios": [
            "waiter_recommend",
            "diner_explore",
            "leave_tip",
            "custom_action"
        ]
    },
}

# Game state
game_state = {
    "current_scenario": "start",
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

def display_scenario(scenario_key):
    # Fetch the scenario from predefined scenarios
    scenario = scenarios[scenario_key]
    
    # Display the scenario description
    logging.info(f"Displaying scenario: {scenario['description']}")
    print(scenario['description'])

    # Display choices
    print("\nChoices:")
    for i, choice in enumerate(scenario['choices'], start=1):
        print(f"{i}. {choice}")  # Display numbered choices

    return scenario

# Simulating player choices - this could be replaced with real input later
def simulate_player_choice(scenario):
    # Just a simple strategy to choose the first option (for demonstration)
    choice_index = 0  # Simulating the first choice
    selected_choice = scenario['choices'][choice_index]
    logging.info(f"Simulated player chose: {selected_choice}")
    
    # Find the next scenario based on the choice made
    next_scenario_key = scenario['next_scenarios'][choice_index]
    return next_scenario_key

# Game loop simulation
current_scenario_key = game_state["current_scenario"]
for _ in range(5):  # Simulate up to 5 iterations
    current_scenario = display_scenario(current_scenario_key)
    current_scenario_key = simulate_player_choice(current_scenario)

# Final logging to indicate end of simulation
logging.info("Game simulation complete.")