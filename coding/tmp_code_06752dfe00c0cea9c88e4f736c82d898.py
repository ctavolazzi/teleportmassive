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

def display_scenario(scenario):
    # Display the scenario description
    logging.info(f"Displaying scenario: {scenario['description']}")
    print(scenario['description'])

    # Display choices
    print("\nChoices:")
    for i, choice in enumerate(scenario['choices'], start=1):
        print(f"{i}. {choice}")  # Display numbered choices

    # Get player's choice
    player_choice = input("What do you want to do? (Enter the number or write 'Other' to specify): ")

    # Handle player choice
    if player_choice.isdigit() and 1 <= int(player_choice) <= len(scenario['choices']):
        choice_index = int(player_choice) - 1
        selected_choice = scenario['choices'][choice_index]
        logging.info(f"Player chose: {selected_choice}")
        return selected_choice
    elif player_choice.strip().lower() == "other":
        custom_action = input("You chose 'Other'. What do you want to do? ")
        logging.info(f"Player chose a custom action: {custom_action}")
        return custom_action
    else:
        logging.warning("Invalid choice made by the player.")
        print("Invalid choice. Please try again.")
        return display_scenario(scenario)

# Call the display function to show the starting scenario
choice = display_scenario(start_scenario)