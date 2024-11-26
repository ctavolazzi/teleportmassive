import uuid
import json
from datetime import datetime, timezone
from typing import Optional, List, Tuple, Dict, Set
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StoryNode:
    """Represents a generic node in the story tree."""
    def __init__(self, node_id: str, title: str, content: str):
        self.id = node_id                      # Unique node identifier
        self.title = title                     # Node title
        self.content = content                 # Node content

        self.parent_ids: Set[str] = set()      # Set of parent node IDs
        self.child_choices: Dict[str, str] = {}# Maps choice text to child node IDs

        self.metadata: Dict[str, any] = {}     # Additional metadata (tags, requirements, etc.)
        self.visits: int = 0                   # Number of times visited
        self.last_visited: Optional[str] = None# Timestamp of last visit

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
        # Unique game and session IDs
        self.game_id = f"game_{uuid.uuid4().hex}"
        self.session_id = session_id if session_id else f"session_{uuid.uuid4().hex}"

        # Node management
        self.nodes: Dict[str, StoryNode] = {}
        self.root_node_id: Optional[str] = None

        # Initialize the story nodes
        self.init_story_nodes()

        # Initialize or load game state
        if session_id:
            success = self.load_game_state()
            if not success:
                self.init_game_state()
                self.save_game_state()
        else:
            self.init_game_state()
            self.save_game_state()

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

    def add_node(self, node: StoryNode):
        """Add a new node to the story graph."""
        self.nodes[node.id] = node

    def get_node(self, node_id: str) -> Optional[StoryNode]:
        """Retrieve a node by its ID."""
        return self.nodes.get(node_id)

    def add_choice(self, from_node_id: str, choice_text: str, to_node_id: str):
        """Add a choice from one node to another."""
        from_node = self.get_node(from_node_id)
        to_node = self.get_node(to_node_id)
        if from_node and to_node:
            from_node.add_child(choice_text, to_node_id)
            to_node.add_parent(from_node_id)
        else:
            logger.error(f"Failed to add choice from '{from_node_id}' to '{to_node_id}'")

    def traverse_to_node(self, node_id: str) -> List[StoryNode]:
        """Get the path from the root node to the specified node."""
        path = []
        current_node_id = node_id

        while current_node_id != self.root_node_id:
            node = self.get_node(current_node_id)
            if node is None:
                # Node not found
                return []
            path.insert(0, node)
            if not node.parent_ids:
                # No parent, cannot proceed
                return []
            # Assuming single parent for simplicity
            current_node_id = next(iter(node.parent_ids))
        # Add the root node
        root_node = self.get_node(self.root_node_id)
        if root_node:
            path.insert(0, root_node)
        return path

    def init_game_state(self):
        """Initialize game state with IDs and player attributes."""
        self.game_state = {
            "game_id": self.game_id,
            "session_id": self.session_id,
            "current_node_id": self.root_node_id,
            "choices_made": [],
            "player_attributes": {},  # e.g., {"strength": 5, "intelligence": 7}
            "game_started": datetime.now(timezone.utc).isoformat()
        }

    def update_game_state(self, choice_text: str, next_node_id: str):
        """Update the game state with the player's choice."""
        self.game_state['current_node_id'] = next_node_id
        self.game_state['choices_made'].append({
            'choice_text': choice_text,
            'node_id': next_node_id,
            'timestamp': datetime.now(timezone.utc).isoformat()
        })

    def get_available_choices(self) -> List[str]:
        """Get choices available at the current node based on player attributes."""
        current_node = self.get_node(self.game_state['current_node_id'])
        choices = []
        for choice_text, child_node_id in current_node.child_choices.items():
            child_node = self.get_node(child_node_id)
            if child_node and child_node.is_accessible(self.game_state['player_attributes']):
                choices.append(choice_text)
        return choices

    def get_story_context(self) -> str:
        """Retrieve the story context based on the player's path."""
        path = self.traverse_to_node(self.game_state['current_node_id'])
        context = '\n\n'.join(node.content for node in path)
        return context

    def update_story(self, choice_text: str) -> Tuple[str, List[str]]:
        """Update the game state and generate the next story content."""
        try:
            current_node = self.get_node(self.game_state['current_node_id'])
            if not current_node:
                return 'An error occurred: current node not found.', []

            # Find the next node based on the choice
            next_node_id = current_node.child_choices.get(choice_text)
            if not next_node_id:
                return 'Invalid choice selected.', []

            next_node = self.get_node(next_node_id)
            if not next_node:
                return 'An error occurred: next node not found.', []

            # Update game state
            self.update_game_state(choice_text, next_node_id)

            # Update node visit info
            next_node.visits += 1
            next_node.last_visited = datetime.now(timezone.utc).isoformat()

            # Generate content using AI (placeholder)
            context = self.get_story_context()
            next_content = generate_story_content(context)

            # Prepare next set of choices
            choices = self.get_available_choices()

            return next_content, choices
        except Exception as e:
            logger.exception("Error updating story")
            return 'An unexpected error occurred. Please try again.', []

    def save_story_graph(self, filepath: str = 'story_graph.json'):
        """Serialize and save the story graph to a file."""
        graph_data = {node_id: node.to_dict() for node_id, node in self.nodes.items()}
        with open(filepath, 'w') as f:
            json.dump(graph_data, f, indent=2)

    def load_story_graph(self, filepath: str = 'story_graph.json'):
        """Load and deserialize the story graph from a file."""
        try:
            with open(filepath, 'r') as f:
                graph_data = json.load(f)
            self.nodes = {}
            for node_id, node_data in graph_data.items():
                node = StoryNode.from_dict(node_data)
                self.nodes[node_id] = node
            # Set the root node ID
            self.root_node_id = next(iter(self.nodes))  # Assuming the first node is the root
        except Exception as e:
            logger.error(f"Error loading story graph: {e}")

    def save_game_state(self, filepath: str = 'game_state.json'):
        """Save the current game state to a file."""
        with open(filepath, 'w') as f:
            json.dump(self.game_state, f, indent=2)

    def load_game_state(self, filepath: str = 'game_state.json') -> bool:
        """Load the game state from a file."""
        try:
            with open(filepath, 'r') as f:
                self.game_state = json.load(f)
            return True
        except Exception as e:
            logger.error(f"Error loading game state: {e}")
            return False

# Placeholder for AI-generated content
def generate_story_content(context: str) -> str:
    """
    Generate the next part of the story based on the context.
    In a real implementation, this would interface with an AI model.
    """
    return f"{context}\n\n[The story continues based on the player's choices...]"

# Example usage:

if __name__ == '__main__':
    # Initialize the game
    game = TeleportMassiveGame()

    # Simulate a game loop
    while True:
        current_node = game.get_node(game.game_state['current_node_id'])
        print(f"\n{current_node.title}")
        print(f"{current_node.content}\n")

        choices = game.get_available_choices()
        if not choices:
            print("The story has reached an end.")
            break

        print("Available choices:")
        for idx, choice in enumerate(choices, 1):
            print(f"{idx}. {choice}")

        selected = input("Enter the number of your choice (or 'q' to quit): ")
        if selected.lower() == 'q':
            break

        try:
            choice_idx = int(selected) - 1
            if 0 <= choice_idx < len(choices):
                choice_text = choices[choice_idx]
                next_content, _ = game.update_story(choice_text)
                print(next_content)
            else:
                print("Invalid choice number.")
        except ValueError:
            print("Please enter a valid number.")