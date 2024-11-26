import gradio as gr
import uuid
from datetime import datetime
from typing import Dict, List, Optional
import logging
import os

class GameLogger:
    """Helper logger class to log all game actions."""
    def __init__(self, log_file: str = "game.log"):
        # Configure the logger
        self.logger = logging.getLogger("GameLogger")
        self.logger.setLevel(logging.DEBUG)

        # Prevent adding multiple handlers if logger already has handlers
        if not self.logger.handlers:
            # Create file handler which logs even debug messages
            fh = logging.FileHandler(log_file)
            fh.setLevel(logging.DEBUG)

            # Create console handler with a higher log level
            ch = logging.StreamHandler()
            ch.setLevel(logging.ERROR)

            # Create formatter and add it to the handlers
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)

            # Add the handlers to the logger
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)

        self.logger.debug("Logger initialized.")

    def log(self, message: str):
        self.logger.debug(message)

    def error(self, message: str):
        self.logger.error(message)

# Initialize the logger
game_logger = GameLogger()

class StoryNode:
    def __init__(self, id: str, title: str, content: str, choices: List[Dict[str, str]]):
        self.id = id
        self.title = title
        self.content = content
        self.choices = choices
        game_logger.log(f"StoryNode created: {self.id}, Title: {self.title}")

class SimpleGame:
    def __init__(self):
        game_logger.log("Initializing SimpleGame.")
        self.nodes: Dict[str, StoryNode] = {}
        self.current_node_id: Optional[str] = None
        self.load_story()

    def load_story(self):
        game_logger.log("Loading story nodes.")
        # Define story nodes
        start_node = StoryNode(
            id="start",
            title="The Crossroads",
            content="You stand at a crossroads in a dark forest. Paths lead to the **left** and **right**.",
            choices=[
                {"text": "Take the left path", "target_node_id": "left_path"},
                {"text": "Take the right path", "target_node_id": "right_path"}
            ]
        )

        left_node = StoryNode(
            id="left_path",
            title="A Peaceful Meadow",
            content="You find yourself in a peaceful meadow filled with wildflowers.",
            choices=[
                {"text": "Pick some flowers", "target_node_id": "pick_flowers"},
                {"text": "Rest for a while", "target_node_id": "rest_meadow"}
            ]
        )

        right_node = StoryNode(
            id="right_path",
            title="A Dark Cave",
            content="You enter a dark cave. The sound of dripping water echoes around you.",
            choices=[
                {"text": "Light a torch", "target_node_id": "light_torch"},
                {"text": "Proceed in the dark", "target_node_id": "proceed_dark"}
            ]
        )

        end_node = StoryNode(
            id="end",
            title="The End",
            content="Thank you for playing!",
            choices=[]
        )

        pick_flowers_node = StoryNode(
            id="pick_flowers",
            title="Flower Picking",
            content="You gather a beautiful bouquet of wildflowers.",
            choices=[
                {"text": "Return to the crossroads", "target_node_id": "start"}
            ]
        )

        rest_meadow_node = StoryNode(
            id="rest_meadow",
            title="Resting",
            content="You take a peaceful rest in the meadow, feeling refreshed.",
            choices=[
                {"text": "Return to the crossroads", "target_node_id": "start"}
            ]
        )

        light_torch_node = StoryNode(
            id="light_torch",
            title="Lit Path",
            content="With your torch lit, you see sparkling gems in the cave walls.",
            choices=[
                {"text": "Collect the gems", "target_node_id": "collect_gems"},
                {"text": "Return to the crossroads", "target_node_id": "start"}
            ]
        )

        proceed_dark_node = StoryNode(
            id="proceed_dark",
            title="Stumble in the Dark",
            content="You trip over a rock and decide it's best to turn back.",
            choices=[
                {"text": "Return to the crossroads", "target_node_id": "start"}
            ]
        )

        collect_gems_node = StoryNode(
            id="collect_gems",
            title="Gem Collector",
            content="You collect the gems and feel a sense of accomplishment.",
            choices=[
                {"text": "Exit the cave", "target_node_id": "start"}
            ]
        )

        # Add nodes to the game
        self.nodes = {
            node.id: node for node in [
                start_node, left_node, right_node, end_node,
                pick_flowers_node, rest_meadow_node,
                light_torch_node, proceed_dark_node, collect_gems_node
            ]
        }

        self.current_node_id = "start"
        game_logger.log(f"Story loaded. Starting at node: {self.current_node_id}")

    def make_choice(self, choice_text: str) -> (str, List[str]):
        game_logger.log(f"Player made choice: {choice_text}")
        current_node = self.nodes.get(self.current_node_id)
        if not current_node:
            game_logger.error(f"Current node ID '{self.current_node_id}' does not exist.")
            return "An error occurred. Current node not found.", []

        choice = next((c for c in current_node.choices if c["text"] == choice_text), None)
        if choice:
            self.current_node_id = choice["target_node_id"]
            next_node = self.nodes.get(self.current_node_id)
            if not next_node:
                game_logger.error(f"Target node ID '{self.current_node_id}' does not exist.")
                return "An error occurred. Target node not found.", []
            content = f"### {next_node.title}\n\n{next_node.content}"
            choices = [c["text"] for c in next_node.choices]
            game_logger.log(f"Moved to node: {self.current_node_id}, Title: {next_node.title}")
            return content, choices
        else:
            game_logger.error(f"Invalid choice made: {choice_text}")
            return "Invalid choice. Please select a valid option.", [c["text"] for c in current_node.choices]

def create_interface():
    game_logger.log("Creating game interface.")
    game = SimpleGame()
    current_node = game.nodes.get(game.current_node_id)

    if not current_node:
        game_logger.error(f"Start node '{game.current_node_id}' not found.")
        return gr.Markdown("An error occurred while loading the game.")

    with gr.Blocks(title="Simple Adventure Game") as interface:
        gr.Markdown("# Simple Choose Your Own Adventure Game")

        content = gr.Markdown(f"### {current_node.title}\n\n{current_node.content}")

        choices = gr.Radio(
            choices=[(c["text"], c["text"]) for c in current_node.choices],
            label="Choose an action:",
            interactive=True
        )
        submit = gr.Button("Go")

        def on_submit(choice_text):
            game_logger.log(f"Processing choice: {choice_text}")
            new_content, new_choices = game.make_choice(choice_text)
            content.value = new_content
            # Update choices with tuples
            choices.choices = [(c, c) for c in new_choices] if new_choices else []
            choices.value = None  # Reset the selection
            game_logger.log("Updated content and choices.")
            return [content, choices]

        submit.click(
            fn=on_submit,
            inputs=choices,
            outputs=[content, choices]
        )

    game_logger.log("Interface created successfully.")
    return interface

if __name__ == "__main__":
    game_logger.log("Launching the game.")
    demo = create_interface()
    demo.launch()
    game_logger.log("Game session ended.")