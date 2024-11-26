import uuid
import json
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any, Tuple
from pathlib import Path

import gradio as gr
import logging
from enum import Enum
import argparse
import math

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    force=True
)
logger = logging.getLogger(__name__)

class NodeType(Enum):
    STORY_START = "story_start"
    STORY_BRANCH = "story_branch"
    STORY_END = "story_end"

@dataclass
class Choice:
    id: str
    text: str
    target_node_id: str
    requirements: Dict[str, Any] = field(default_factory=dict)

    def is_available(self, player_state: Dict[str, Any]) -> bool:
        return True  # Implement any logic for choice availability

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "text": self.text,
            "target_node_id": self.target_node_id,
            "requirements": self.requirements
        }

    @staticmethod
    def from_dict(data: dict) -> 'Choice':
        return Choice(
            id=data["id"],
            text=data["text"],
            target_node_id=data["target_node_id"],
            requirements=data.get("requirements", {})
        )

@dataclass
class StoryNode:
    id: str
    type: NodeType
    title: str
    content: str
    choices: List[Choice] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    visits: int = 0
    last_visited: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type.value,
            "title": self.title,
            "content": self.content,
            "choices": [choice.to_dict() for choice in self.choices],
            "metadata": self.metadata,
            "visits": self.visits,
            "last_visited": self.last_visited
        }

    @staticmethod
    def from_dict(data: dict) -> 'StoryNode':
        return StoryNode(
            id=data["id"],
            type=NodeType(data["type"]),
            title=data["title"],
            content=data["content"],
            choices=[Choice.from_dict(c) for c in data.get("choices", [])],
            metadata=data.get("metadata", {}),
            visits=data.get("visits", 0),
            last_visited=data.get("last_visited")
        )

class GameState:
    def __init__(self, game_id: str, session_id: str, save_dir: Path):
        self.game_id = game_id
        self.session_id = session_id
        self.current_node_id: Optional[str] = None
        self.player_state: Dict[str, Any] = {}
        self.choice_history: List[Dict[str, Any]] = []
        self.timeline: List[Dict[str, Any]] = []
        self.game_started = datetime.now(timezone.utc).isoformat()

        self.save_dir = save_dir / "sessions" / self.session_id
        self.save_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Created session directory: {self.save_dir}")

    def record_choice(self, choice: Choice) -> None:
        timestamp = datetime.now(timezone.utc).isoformat()
        self.choice_history.append({
            "choice_id": choice.id,
            "choice_text": choice.text,
            "target_node_id": choice.target_node_id,
            "timestamp": timestamp
        })
        self.timeline.append({
            "title": f"Choice {len(self.choice_history)}",
            "description": choice.text,
            "timestamp": timestamp
        })
        self.save_game_state()

    def to_dict(self) -> dict:
        return {
            "game_id": self.game_id,
            "session_id": self.session_id,
            "current_node_id": self.current_node_id,
            "player_state": self.player_state,
            "choice_history": self.choice_history,
            "timeline": self.timeline,
            "game_started": self.game_started
        }

    @staticmethod
    def from_dict(data: dict, save_dir: Path) -> 'GameState':
        state = GameState(data["game_id"], data["session_id"], save_dir)
        state.current_node_id = data.get("current_node_id")
        state.player_state = data.get("player_state", {})
        state.choice_history = data.get("choice_history", [])
        state.timeline = data.get("timeline", [])
        state.game_started = data.get("game_started")
        return state

    def save_game_state(self) -> None:
        """Save the current game state to the session directory"""
        save_path = self.save_dir / "state.json"
        try:
            with open(save_path, 'w') as f:
                json.dump(self.to_dict(), f, indent=2)
            logger.debug(f"Game state saved to {save_path}")
        except Exception as e:
            logger.error(f"Failed to save game state: {e}")

class StoryEngine:
    def __init__(self, session_id: Optional[str] = None):
        self.game_id = uuid.uuid1().hex
        self.session_id = session_id if session_id else uuid.uuid1().hex

        # Setup base save directory
        self.save_dir = Path("game_data")
        self.save_dir.mkdir(parents=True, exist_ok=True)

        # Initialize story content
        self.nodes: Dict[str, StoryNode] = {}
        self.load_story_nodes_from_config()

        # Initialize game state
        self.state = GameState(self.game_id, self.session_id, self.save_dir)
        self.state.current_node_id = self.initial_node_id
        self.state.timeline.append({
            "title": "Game Start",
            "description": "Beginning of the journey",
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        self.state.save_game_state()

        # Generate initial timeline
        self.initial_timeline = self.generate_timeline_html()

    def get_current_node(self) -> StoryNode:
        """Get the current story node"""
        if not self.state.current_node_id:
            self.state.current_node_id = self.initial_node_id
            self.state.save_game_state()

        current_node = self.nodes.get(self.state.current_node_id)
        if not current_node:
            logger.error(f"Current node ID {self.state.current_node_id} not found in nodes")
            raise ValueError(f"Invalid current node ID: {self.state.current_node_id}")

        return current_node

    def load_story_nodes_from_config(self) -> None:
        config_path = self.save_dir / "sessions" / self.session_id / "story_config.json"
        if not config_path.exists():
            logger.error(f"Configuration file not found: {config_path}")
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        with open(config_path, 'r') as f:
            config_data = json.load(f)

        nodes_data = config_data.get("nodes", [])
        for node_data in nodes_data:
            node = StoryNode.from_dict(node_data)
            self.nodes[node.id] = node

        # Set initial node
        self.initial_node_id = config_data.get("start_node_id")
        if not self.initial_node_id or self.initial_node_id not in self.nodes:
            logger.error("Start node ID is invalid or not found in nodes.")
            raise ValueError("Invalid start node ID.")

    def generate_timeline_html(self) -> str:
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

        for event in self.state.timeline:
            timeline_html += f"""
                <div class="event">
                    <div class="event-title">{event['title']}</div>
                    <div class="event-description">{event['description']}</div>
                </div>
            """

        timeline_html += """
            </div>
        </div>
        """
        return timeline_html

    def make_choice(self, choice_text: str) -> Tuple[str, List[str], str]:
        try:
            current_node = self.nodes.get(self.state.current_node_id)
            if not current_node:
                logger.error(f"Current node not found: {self.state.current_node_id}")
                return (
                    "### Error\nCurrent story node not found. Please try again.",
                    [],
                    self.generate_timeline_html()
                )

            # Strip whitespace for more forgiving comparison
            choice = next(
                (c for c in current_node.choices if c.text.strip() == choice_text.strip()),
                None
            )

            if not choice or not choice.target_node_id:
                logger.error(f"Invalid choice or target: {choice_text}")
                return (
                    f"### {current_node.title}\n\n{current_node.content}",
                    [c.text for c in current_node.choices],
                    self.generate_timeline_html()
                )

            next_node = self.nodes.get(choice.target_node_id)
            if not next_node:
                logger.error(f"Target node not found: {choice.target_node_id}")
                return (
                    f"### {current_node.title}\n\n{current_node.content}",
                    [c.text for c in current_node.choices],
                    self.generate_timeline_html()
                )

            # Update state
            self.state.record_choice(choice)
            self.state.current_node_id = next_node.id
            next_node.visits += 1
            next_node.last_visited = datetime.now(timezone.utc).isoformat()

            return (
                f"### {next_node.title}\n\n{next_node.content}",
                [c.text for c in next_node.choices],
                self.generate_timeline_html()
            )
        except Exception as e:
            logger.error(f"Error processing choice: {e}")
            return (
                "### Error\nAn unexpected error occurred. Please try again.",
                [],
                self.generate_timeline_html()
            )

    def generate_story_map(self) -> List[Dict[str, Any]]:
        story_map = []
        for node_id, node in self.nodes.items():
            story_map.append({
                "id": node.id,
                "type": node.type.value,
                "title": node.title,
                "visits": node.visits,
                "last_visited": node.last_visited,
                "choices": [c.to_dict() for c in node.choices]
            })
        return story_map

    def generate_visual_map_html(self) -> str:
        """Generate an interactive visual map of the story nodes"""
        map_html = """
        <style>
            .story-map {
                background: #1a1a1a;
                padding: 20px;
                position: relative;
                min-height: 400px;
            }

            .node {
                position: absolute;
                width: 120px;
                padding: 10px;
                border-radius: 8px;
                background: #2a2a2a;
                border: 2px solid #444;
                cursor: pointer;
                transition: all 0.3s ease;
            }

            .node.visited {
                border-color: #4CAF50;
            }

            .node.current {
                border-color: #2196F3;
                box-shadow: 0 0 10px #2196F3;
            }

            .node-connection {
                position: absolute;
                background: #444;
                height: 2px;
                transform-origin: left center;
                pointer-events: none;
            }

            .layer-0 { top: 20px; }     /* Start node */
            .layer-1 { top: 150px; }    /* First choices */
            .layer-2 { top: 280px; }    /* Consequences */
            .layer-3 { top: 410px; }    /* Endings */
        </style>

        <div class="story-map">
        """

        # Add nodes
        node_positions = {}

        # Calculate positions for each layer
        for node_id, node in self.nodes.items():
            layer = self._get_node_layer(node)
            x_pos = self._calculate_x_position(node, layer)
            node_positions[node_id] = (x_pos, f"layer-{layer}")

            visited_class = "visited" if node.visits > 0 else ""
            current_class = "current" if node_id == self.state.current_node_id else ""

            map_html += f"""
            <div class="node {visited_class} {current_class}"
                 style="left: {x_pos}px;"
                 data-node-id="{node_id}"
                 onclick="selectNode('{node_id}')">
                {node.title}
            </div>
            """

        # Add connections between nodes
        for node_id, node in self.nodes.items():
            for choice in node.choices:
                if choice.target_node_id:
                    start_pos = node_positions[node_id]
                    end_pos = node_positions[choice.target_node_id]
                    map_html += self._generate_connection_html(start_pos, end_pos)

        map_html += """
        </div>

        <script>
        function selectNode(nodeId) {
            // Add navigation logic here
            console.log('Selected node:', nodeId);
        }
        </script>
        """

        return map_html

    def _get_node_layer(self, node: StoryNode) -> int:
        """Determine which layer a node belongs to"""
        if node.type == NodeType.STORY_START:
            return 0
        elif node.type == NodeType.STORY_END:
            return 3
        elif len(node.choices) > 0:
            # Simplified branch detection based on node title/content
            if any(keyword in node.title.lower() for keyword in ['time', 'temporal']):
                return 1
            elif any(keyword in node.title.lower() for keyword in ['parallel', 'universe']):
                return 1
            elif any(keyword in node.title.lower() for keyword in ['quantum', 'entangle']):
                return 1
            return 2
        return 2

    def _calculate_x_position(self, node: StoryNode, layer: int) -> int:
        """Calculate horizontal position for a node based on its type and choices"""
        base_offset = 50
        spacing = 150

        if layer == 0:
            return 400  # Center the start node
        elif layer == 3:
            return 400  # Center the end node

        # Calculate position based on the node's branch type
        branch_positions = {
            'time': 200,
            'parallel': 400,
            'quantum': 600
        }

        # Determine branch type from node content/title
        if 'time' in node.title.lower():
            return branch_positions['time']
        elif 'parallel' in node.title.lower():
            return branch_positions['parallel']
        elif 'quantum' in node.title.lower():
            return branch_positions['quantum']

        return 400  # Default center position

    def _generate_connection_html(self, start_pos: tuple, end_pos: tuple) -> str:
        """Generate HTML for a connection line between nodes"""
        x1, y1_class = start_pos
        x2, y2_class = end_pos

        # Extract actual y positions from class names
        y1 = int(y1_class.split('-')[1]) * 130 + 40
        y2 = int(y2_class.split('-')[1]) * 130 + 40

        length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        angle = math.atan2(y2 - y1, x2 - x1) * 180 / math.pi

        return f"""
        <div class="node-connection"
             style="left: {x1}px;
                    top: {y1}px;
                    width: {length}px;
                    transform: rotate({angle}deg);">
        </div>
        """

def create_interface(session_id: Optional[str] = None) -> gr.Interface:
    engine = StoryEngine(session_id)

    with gr.Blocks(theme=gr.themes.Soft()) as interface:
        # Header section
        with gr.Row(elem_classes="header-container"):
            gr.Markdown(
                "# 🎭 Teleport Massive",
                elem_classes="game-title"
            )
            with gr.Column(scale=1, min_width=100):
                restart = gr.Button("↺ New Game", elem_classes="control-button")

        # Main game container
        with gr.Row(elem_classes="game-container"):
            # Left column - Story content
            with gr.Column(scale=2, elem_classes="story-column"):
                title = gr.Markdown(
                    engine.get_current_node().title,
                    elem_classes="story-title"
                )
                content = gr.Markdown(
                    engine.get_current_node().content,
                    elem_classes="story-content"
                )

                # Choice section
                with gr.Box(elem_classes="choice-container"):
                    gr.Markdown("### What do you do?", elem_classes="choice-header")
                    choices = gr.Radio(
                        choices=[choice.text for choice in engine.get_current_node().choices],
                        label="",
                        interactive=True,
                        elem_classes="choice-options"
                    )
                    submit = gr.Button(
                        "▶ Continue",
                        elem_classes="submit-button"
                    )

            # Right column - Visual elements
            with gr.Column(scale=1, elem_classes="visual-column"):
                # Story map
                with gr.Box(elem_classes="map-container"):
                    gr.Markdown("### Your Journey", elem_classes="map-title")
                    map_display = gr.HTML(
                        engine.generate_visual_map_html(),
                        elem_classes="story-map"
                    )

                # Stats or inventory could go here
                with gr.Box(elem_classes="stats-container", visible=False):
                    gr.Markdown("### Stats", elem_classes="stats-title")
                    # Add stats display here when implemented

        # Event handlers
        def handle_choice(choice_text):
            new_content, new_choices, new_map = engine.make_choice(choice_text)
            return [
                engine.get_current_node().title,
                new_content,
                new_choices,
                new_map
            ]

        submit.click(
            fn=handle_choice,
            inputs=[choices],
            outputs=[title, content, choices, map_display]
        )

        restart.click(
            fn=engine.reset_game,
            inputs=[],
            outputs=[title, content, choices, map_display]
        )

    return interface

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--session-id", required=True, help="Game session ID")
    args = parser.parse_args()

    interface = create_interface(session_id=args.session_id)
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True
    )