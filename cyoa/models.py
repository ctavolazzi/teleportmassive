from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime

@dataclass
class Choice:
    id: str
    text: str
    target_node_id: Optional[str]
    requirements: Dict[str, Any] = field(default_factory=dict)

    def is_available(self, player_state: Dict[str, Any]) -> bool:
        # TODO: Implement requirement checking
        return True

@dataclass
class StoryNode:
    id: str
    title: str
    content: str
    choices: List[Choice]
    type: str = "story_branch"
    metadata: Dict[str, Any] = field(default_factory=dict)
    visits: int = 0
    last_visited: Optional[datetime] = None

    def visit(self):
        self.visits += 1
        self.last_visited = datetime.now()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "content": self.content,
            "choices": [vars(c) for c in self.choices],
            "metadata": self.metadata,
            "visits": self.visits,
            "last_visited": self.last_visited.isoformat() if self.last_visited else None
        }