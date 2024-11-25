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
        # Here we will handle the choice in the next step
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
