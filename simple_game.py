import uuid
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import gradio as gr
import logging

print("Starting script...")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

print("Logging configured...")

class StoryNode:
    def __init__(self, id: str, title: str, content: str, choices: List[dict]):
        self.id = id
        self.title = title
        self.content = content
        self.choices = choices
        self.visits = 0
        self.last_visited = None

print("StoryNode class defined...")

class SimpleGame:
    def __init__(self):
        print("Initializing SimpleGame...")
        self.session_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex}"
        self.save_dir = Path("game_data/sessions") / self.session_id
        self.save_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created session directory: {self.save_dir}")

        # Initialize game state
        self.nodes: Dict[str, StoryNode] = {}
        self.current_node_id = None
        self.timeline = []

        # Load story and save initial state
        self.load_story()
        self.save_state()

    def load_story(self):
        print("Loading story...")
        # Create the start node
        start_node_id = uuid.uuid4().hex

        # Create initial node with two choices
        self.nodes[start_node_id] = StoryNode(
            id=start_node_id,
            title="The Beginning",
            content="You stand at a crossroads. Two paths lie before you.",
            choices=[
                {
                    "id": uuid.uuid4().hex,
                    "text": "Take the path to the left",
                    "target_node_id": None
                },
                {
                    "id": uuid.uuid4().hex,
                    "text": "Take the path to the right",
                    "target_node_id": None
                }
            ]
        )

        self.current_node_id = start_node_id
        self.timeline.append({
            "title": "Game Start",
            "description": "Beginning of the journey",
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        print("Story loaded.")

    def make_choice(self, choice_text: str) -> Tuple[str, List[str], str]:
        print(f"Making choice: {choice_text}")
        current_node = self.nodes[self.current_node_id]

        # Find the chosen choice
        choice = next(
            (c for c in current_node.choices if c["text"].strip() == choice_text.strip()),
            None
        )

        if not choice:
            logger.error(f"Invalid choice or target: {choice_text}")
            return (
                f"### {current_node.title}\n\n{current_node.content}",
                [c["text"] for c in current_node.choices],
                self.generate_timeline_html()
            )

        # If this choice leads nowhere, create a new node
        if not choice["target_node_id"]:
            new_node_id = uuid.uuid4().hex
            self.nodes[new_node_id] = StoryNode(
                id=new_node_id,
                title="A New Path",
                content=f"You continue down the path after {choice_text.lower()}.",
                choices=[
                    {
                        "id": uuid.uuid4().hex,
                        "text": "Take the path to the left",
                        "target_node_id": None
                    },
                    {
                        "id": uuid.uuid4().hex,
                        "text": "Take the path to the right",
                        "target_node_id": None
                    }
                ]
            )
            choice["target_node_id"] = new_node_id

        # Update state
        next_node = self.nodes[choice["target_node_id"]]
        self.current_node_id = next_node.id
        next_node.visits += 1
        next_node.last_visited = datetime.now(timezone.utc).isoformat()

        # Record choice in timeline
        self.timeline.append({
            "title": f"Choice {len(self.timeline)}",
            "description": choice_text,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

        self.save_state()

        return (
            f"### {next_node.title}\n\n{next_node.content}",
            [c["text"] for c in next_node.choices],
            self.generate_timeline_html()
        )

    def generate_timeline_html(self) -> str:
        html = '<div style="height: 400px; overflow-y: auto; padding: 20px; background: rgba(0,0,0,0.2); border-radius: 8px;">'
        for event in self.timeline:
            html += f'''
                <div style="margin: 10px 0; padding: 10px; background: rgba(255,255,255,0.1); border-radius: 4px;">
                    <div style="font-weight: bold;">{event['title']}</div>
                    <div style="color: #ccc;">{event['description']}</div>
                </div>
            '''
        html += '</div>'
        return html

    def save_state(self):
        state = {
            "session_id": self.session_id,
            "current_node_id": self.current_node_id,
            "timeline": self.timeline
        }
        with open(self.save_dir / "state.json", 'w') as f:
            json.dump(state, f, indent=2)
        print("State saved.")

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