import uuid
import json
from datetime import datetime, timezone
from typing import Optional, List, Tuple, Dict, Set
import logging
from pathlib import Path

# Import Gradio for the web interface
import gradio as gr

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    force=True
)
logger = logging.getLogger(__name__)

print("Starting application...")

class StoryNode:
    """Represents a generic node in the story tree."""
    def __init__(self, node_id: str, title: str, content: str):
        self.id = node_id
        self.title = title
        self.content = content
        self.parent_ids: Set[str] = set()
        self.child_choices: Dict[str, str] = {}
        self.metadata: Dict[str, any] = {}
        self.visits: int = 0
        self.last_visited: Optional[str] = None

    def add_child(self, choice_text: str, child_node_id: str):
        """Add a child node via choice text."""
        self.child_choices[choice_text] = child_node_id

    def add_parent(self, parent_node_id: str):
        """Add a parent node."""
        self.parent_ids.add(parent_node_id)

    def is_accessible(self, player_attributes: Dict[str, any]) -> bool:
        """Determine if the node is accessible based on player attributes."""
        requirements = self.metadata.get('requirements', {})
        for attr, value in requirements.items():
            if player_attributes.get(attr) != value:
                return False
        return True

    def to_dict(self) -> dict:
        """Convert the node to a dictionary for serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'parent_ids': list(self.parent_ids),
            'child_choices': self.child_choices,
            'metadata': self.metadata,
            'visits': self.visits,
            'last_visited': self.last_visited
        }

    @staticmethod
    def from_dict(data: dict) -> 'StoryNode':
        """Create a StoryNode from a dictionary."""
        node = StoryNode(
            node_id=data['id'],
            title=data['title'],
            content=data['content']
        )
        node.parent_ids = set(data.get('parent_ids', []))
        node.child_choices = data.get('child_choices', {})
        node.metadata = data.get('metadata', {})
        node.visits = data.get('visits', 0)
        node.last_visited = data.get('last_visited', None)
        return node

class TeleportMassiveGame:
    def __init__(self, session_id: Optional[str] = None):
        print("Initializing game...")
        self.game_id = f"game_{uuid.uuid4().hex}"
        self.session_id = session_id if session_id else f"session_{uuid.uuid4().hex}"

        # Setup save directory
        self.save_dir = Path("game_data")
        self.save_dir.mkdir(exist_ok=True)

        # Node management
        self.nodes: Dict[str, StoryNode] = {}
        self.root_node_id: Optional[str] = None

        # Initialize the story nodes
        self.init_story_nodes()

        # Initialize or load game state
        if session_id and self.load_game_state():
            logger.info(f"Loaded existing session: {session_id}")
        else:
            self.init_game_state()
            self.save_game_state()

        # Generate initial timeline HTML
        self.initial_timeline = self.generate_timeline_html()

    def add_node(self, node: StoryNode):
        """Add a new node to the story graph."""
        logger.debug(f"Adding node: {node.id} - {node.title}")
        self.nodes[node.id] = node

    def get_node(self, node_id: str) -> Optional[StoryNode]:
        """Retrieve a node by its ID."""
        node = self.nodes.get(node_id)
        if node is None:
            logger.warning(f"Node not found: {node_id}")
        return node

    def generate_timeline_html(self) -> str:
        """Generate HTML for the timeline display"""
        timeline_html = """
        <style>
            .timeline-container {
                height: 400px;
                overflow-y: auto;
                padding: 20px;
                margin: 10px;
                background: rgba(0, 0, 0, 0.2);
                border-radius: 8px;
            }
            .timeline {
                padding: 20px;
                border-left: 2px solid #3b82f6;
                margin-left: 20px;
            }
            .event {
                margin: 10px 0;
                padding-left: 20px;
                position: relative;
                opacity: 0.7;
                transition: opacity 0.3s ease;
            }
            .event:last-child {
                opacity: 1;
            }
            .event::before {
                content: '';
                position: absolute;
                left: -11px;
                top: 50%;
                width: 12px;
                height: 12px;
                background-color: #3b82f6;
                border-radius: 50%;
                transform: translateY(-50%);
            }
            .event-title { color: #fff; }
            .event-description { color: #ccc; }
        </style>
        <div class="timeline-container">
            <div class="timeline">
        """

        # Add timeline events from game state
        for event in self.game_state['timeline']:
            timeline_html += f"""
                <div class="event">
                    <div class="event-title">{event['title']}</div>
                    <div class="event-description">{event['description']}</div>
                </div>
            """

        timeline_html += """
            </div>
        </div>
        <script>
            const container = document.querySelector('.timeline-container');
            if (container) {
                container.scrollTop = container.scrollHeight;
            }
        </script>
        """
        return timeline_html

    def init_story_nodes(self):
        """Initialize the story nodes and build the tree structure."""
        # Create nodes
        root_node = StoryNode(
            node_id='node_root',
            title='Sam Iker Wakes Up',
            content='Sam Iker awakens from a vivid dream where he was soaring around a massive skyscraper...'
        )

        window_node = StoryNode(
            node_id='node_window',
            title='Looking Out the Window',
            content='Sam approaches the window and gazes at the sprawling cityscape below...'
        )

        phone_node = StoryNode(
            node_id='node_phone',
            title='Checking Messages',
            content='Sam picks up his phone from the bedside table...'
        )

        # Build relationships
        root_node.add_child('Look out the window to see the city below', window_node.id)
        root_node.add_child('Check his phone for messages', phone_node.id)

        window_node.add_parent(root_node.id)
        phone_node.add_parent(root_node.id)

        # Add nodes to the node map
        self.add_node(root_node)
        self.add_node(window_node)
        self.add_node(phone_node)

        # Store the root node ID
        self.root_node_id = root_node.id

    def init_game_state(self):
        """Initialize game state with IDs and timeline."""
        self.game_state = {
            "game_id": self.game_id,
            "session_id": self.session_id,
            "current_node_id": self.root_node_id,
            "choices_made": [],
            "player_attributes": {},
            "timeline": [{
                "title": "Game Start",
                "description": "Sam Iker wakes up from a vivid dream",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }],
            "game_started": datetime.now(timezone.utc).isoformat()
        }

    def update_story(self, choice_text: str) -> Tuple[str, List[str], str]:
        """Update the story state and return new content."""
        try:
            current_node = self.get_node(self.game_state['current_node_id'])
            if not current_node:
                return 'Error: Current node not found.', [], self.generate_timeline_html()

            next_node_id = current_node.child_choices.get(choice_text)
            if not next_node_id:
                return 'Invalid choice selected.', [], self.generate_timeline_html()

            next_node = self.get_node(next_node_id)
            if not next_node:
                return 'Error: Next node not found.', [], self.generate_timeline_html()

            # Update game state
            self.game_state['current_node_id'] = next_node_id
            self.game_state['choices_made'].append({
                'choice_text': choice_text,
                'node_id': next_node_id,
                'timestamp': datetime.now(timezone.utc).isoformat()
            })

            # Update timeline
            self.game_state['timeline'].append({
                "title": f"Choice {len(self.game_state['choices_made'])}",
                "description": choice_text,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })

            # Update node visit info
            next_node.visits += 1
            next_node.last_visited = datetime.now(timezone.utc).isoformat()

            # Save game state
            self.save_game_state()

            return next_node.content, list(next_node.child_choices.keys()), self.generate_timeline_html()

        except Exception as e:
            logger.exception("Error updating story")
            return 'An unexpected error occurred.', [], self.generate_timeline_html()

    def save_game_state(self):
        """Save the current game state to a file."""
        save_path = self.save_dir / f"{self.session_id}_state.json"
        try:
            with open(save_path, 'w') as f:
                json.dump(self.game_state, f, indent=2)
            logger.debug(f"Game state saved to {save_path}")
        except Exception as e:
            logger.error(f"Failed to save game state: {e}")

    def load_game_state(self) -> bool:
        """Load the game state from a file."""
        save_path = self.save_dir / f"{self.session_id}_state.json"
        try:
            if not save_path.exists():
                logger.debug(f"No saved state found at {save_path}")
                return False

            with open(save_path, 'r') as f:
                self.game_state = json.load(f)
            logger.debug(f"Game state loaded from {save_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to load game state: {e}")
            return False

def create_interface() -> gr.Blocks:
    game = TeleportMassiveGame()

    with gr.Blocks(title="Teleport Massive") as interface:
        with gr.Row():
            # Left column - Timeline
            with gr.Column(scale=1):
                timeline_display = gr.HTML(value=game.initial_timeline)

            # Right column - Story and Choices
            with gr.Column(scale=2):
                story_display = gr.Markdown(value=game.nodes[game.root_node_id].content)
                choice_selector = gr.Radio(
                    choices=list(game.nodes[game.root_node_id].child_choices.keys()),
                    label="What happens next?",
                    interactive=True
                )
                submit_btn = gr.Button("Make Your Choice")

        # Debug Controls
        with gr.Accordion("Debug Controls", open=False):
            game_state_display = gr.JSON(
                value=game.game_state,
                label="Game State"
            )
            debug_output = gr.Textbox(
                label="Debug Messages",
                lines=3
            )

            with gr.Row():
                refresh_btn = gr.Button("Refresh State")
                reset_btn = gr.Button("Reset Game")

        # Event handlers
        submit_btn.click(
            fn=game.update_story,
            inputs=[choice_selector],
            outputs=[story_display, choice_selector, timeline_display]
        )

        refresh_btn.click(
            fn=lambda: game.game_state,
            outputs=[game_state_display]
        )

        reset_btn.click(
            fn=lambda: (
                game.__init__(),
                game.nodes[game.root_node_id].content,
                list(game.nodes[game.root_node_id].child_choices.keys()),
                game.game_state,
                "Game Reset!"
            ),
            outputs=[
                story_display,
                choice_selector,
                game_state_display,
                debug_output
            ]
        )

    return interface

if __name__ == "__main__":
    print("Main block started...")
    try:
        demo = create_interface()
        print("Launching interface...")
        demo.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            debug=True
        )
    except Exception as e:
        print(f"Error occurred: {e}")
        logger.exception("Failed to start application")
        raise