import gradio as gr
import uuid
from datetime import datetime
from typing import Dict, List, Optional

class StoryNode:
    def __init__(self, id: str, title: str, content: str, choices: List[Dict[str, str]]):
        self.id = id
        self.title = title
        self.content = content
        self.choices = choices

class SimpleGame:
    def __init__(self):
        self.nodes: Dict[str, StoryNode] = {}
        self.current_node_id: Optional[str] = None
        self.load_story()

    def load_story(self):
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

        # Additional nodes
        pick_flowers_node = StoryNode(
            id="pick_flowers",
            title="Flower Picking",
            content="You pick a bouquet of beautiful flowers and feel happier.",
            choices=[
                {"text": "Return to the crossroads", "target_node_id": "start"}
            ]
        )

        rest_meadow_node = StoryNode(
            id="rest_meadow",
            title="Resting",
            content="You lie down and rest, feeling rejuvenated.",
            choices=[
                {"text": "Return to the crossroads", "target_node_id": "start"}
            ]
        )

        light_torch_node = StoryNode(
            id="light_torch",
            title="Lit Path",
            content="With the torch lit, you see sparkling gems embedded in the cave walls.",
            choices=[
                {"text": "Collect the gems", "target_node_id": "collect_gems"},
                {"text": "Exit the cave", "target_node_id": "start"}
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

    def make_choice(self, choice_text: str) -> (str, List[str]):
        current_node = self.nodes[self.current_node_id]
        choice = next((c for c in current_node.choices if c["text"] == choice_text), None)
        if choice:
            self.current_node_id = choice["target_node_id"]
            next_node = self.nodes[self.current_node_id]
            content = f"### {next_node.title}\n\n{next_node.content}"
            choices = [c["text"] for c in next_node.choices]
            return content, choices
        else:
            return "Invalid choice. Please select a valid option.", [c["text"] for c in current_node.choices]

def create_interface():
    game = SimpleGame()
    current_node = game.nodes[game.current_node_id]

    with gr.Blocks(title="Simple Adventure Game") as interface:
        gr.Markdown("# Simple Choose Your Own Adventure Game")

        content = gr.Markdown(f"### {current_node.title}\n\n{current_node.content}")

        choices = gr.Radio(
            choices=[c["text"] for c in current_node.choices],
            label="Choose an action:",
            interactive=True
        )
        submit = gr.Button("Go")

        def on_submit(choice_text):
            new_content, new_choices = game.make_choice(choice_text)
            content.value = new_content
            choices.choices = new_choices
            choices.value = None  # Reset the selection

        submit.click(
            fn=on_submit,
            inputs=choices,
            outputs=[]
        )

    return interface

if __name__ == "__main__":
    demo = create_interface()
    demo.launch()