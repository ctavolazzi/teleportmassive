import json
from pathlib import Path
from typing import Dict
import logging
from datetime import datetime

from .story_schema import StoryConfig, StoryNodeDict
from .models import StoryNode, Choice

logger = logging.getLogger(__name__)

class StoryLoader:
    @staticmethod
    def load_from_json(file_path: str | Path) -> Dict[str, StoryNode]:
        logger.info(f"Loading story from {file_path}")

        with open(file_path, 'r') as f:
            data: StoryConfig = json.load(f)

        nodes: Dict[str, StoryNode] = {}

        # First pass: Create all nodes
        for node_data in data['nodes']:
            nodes[node_data['id']] = StoryNode(
                id=node_data['id'],
                title=node_data['title'],
                content=node_data['content'],
                choices=[Choice(**choice) for choice in node_data['choices']]
            )

        logger.info(f"Loaded {len(nodes)} nodes")
        return nodes

    @staticmethod
    def validate_story(nodes: Dict[str, StoryNode]) -> bool:
        """Validate that all target_node_ids exist"""
        for node_id, node in nodes.items():
            for choice in node.choices:
                if choice.target_node_id and choice.target_node_id not in nodes:
                    logger.error(f"Node {node_id} has invalid target {choice.target_node_id}")
                    return False
        return True