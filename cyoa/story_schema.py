from typing import TypedDict, List, Optional, Dict, Any
from datetime import datetime

class ChoiceDict(TypedDict):
    id: str
    text: str
    target_node_id: Optional[str]
    requirements: Dict[str, Any]

class StoryNodeDict(TypedDict):
    id: str
    type: str
    title: str
    content: str
    choices: List[ChoiceDict]
    metadata: Dict[str, Any]
    visits: int
    last_visited: Optional[str]

class StoryConfig(TypedDict):
    version: str
    title: str
    author: str
    created_at: str
    updated_at: str
    nodes: List[StoryNodeDict]