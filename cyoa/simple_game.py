import uuid
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import gradio as gr
import logging
from .models import StoryNode, Choice
from .story_loader import StoryLoader

print("Starting script...")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

print("Logging configured...")

class SimpleGame:
    def __init__(self, story_path: str | Path):
        self.story_nodes: Dict[str, StoryNode] = {}
        self.current_node_id: Optional[str] = None
        self.load_story(story_path)

    def load_story(self, story_path: str | Path):
        """Load story from JSON file"""
        self.story_nodes = StoryLoader.load_from_json(story_path)

        if not StoryLoader.validate_story(self.story_nodes):
            raise ValueError("Invalid story configuration")

        # Find start node
        start_nodes = [node for node in self.story_nodes.values()
                      if node.type == "story_start"]
        if not start_nodes:
            raise ValueError("No start node found in story")

        self.current_node_id = start_nodes[0].id
        logger.info(f"Story loaded with {len(self.story_nodes)} nodes")

    def get_current_node(self) -> Optional[StoryNode]:
        if not self.current_node_id:
            return None
        return self.story_nodes.get(self.current_node_id)

    def make_choice(self, choice_id: str) -> Optional[StoryNode]:
        current_node = self.get_current_node()
        if not current_node:
            return None

        # Find the chosen choice
        choice = next((c for c in current_node.choices if c.id == choice_id), None)
        if not choice or not choice.target_node_id:
            return None

        # Update current node
        self.current_node_id = choice.target_node_id
        next_node = self.story_nodes.get(self.current_node_id)
        if next_node:
            next_node.visit()
        return next_node

print("SimpleGame class defined...")

def create_interface():
    print("Creating interface...")
    game = SimpleGame()
    current_node = game.nodes[game.current_node_id]

    with gr.Blocks(theme=gr.themes.Soft()) as interface:
        gr.Markdown("# Simple Adventure Game")

        with gr.Row():
            with gr.Column(scale=2):
                content = gr.Markdown(f"### {current_node.title}\n\n{current_node.content}")
                choices = gr.Radio(
                    choices=[c["text"] for c in current_node.choices],
                    label="What do you do?",
                    interactive=True
                )
                submit = gr.Button("Make Choice")

            with gr.Column(scale=1):
                timeline = gr.HTML(game.generate_timeline_html())

        submit.click(
            fn=game.make_choice,
            inputs=[choices],
            outputs=[content, choices, timeline]
        )

    print("Interface created.")
    return interface

print("Starting main execution...")

if __name__ == "__main__":
    try:
        print("Creating and launching interface...")
        demo = create_interface()
        demo.launch(server_name="0.0.0.0", server_port=7860)
    except Exception as e:
        print(f"Error occurred: {e}")
        logger.exception("Failed to start application")
        raise

print("Script completed.")