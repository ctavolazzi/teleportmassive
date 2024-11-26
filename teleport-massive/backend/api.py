from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import uuid
import json
from pathlib import Path
from utils.logger import setup_logger
import time

# Setup logger
logger = setup_logger("api")

app = FastAPI()

# Add logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    # Log request details
    logger.info(f"Request started: {request.method} {request.url}")
    logger.debug(f"Headers: {dict(request.headers)}")

    try:
        response = await call_next(request)

        # Log response details
        process_time = (time.time() - start_time) * 1000
        logger.info(f"Request completed: {request.method} {request.url} - Status: {response.status_code} - Duration: {process_time:.2f}ms")

        return response
    except Exception as e:
        logger.error(f"Request failed: {request.method} {request.url} - Error: {str(e)}")
        raise

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class Choice(BaseModel):
    id: str
    text: str
    target_node_id: str
    requirements: Dict[str, any] = {}

class StoryNode(BaseModel):
    id: str
    type: str
    title: str
    content: str
    choices: List[Choice]
    metadata: Dict[str, any] = {}
    visits: int = 0
    last_visited: Optional[str] = None

class GameState(BaseModel):
    session_id: str
    current_node_id: str
    history: List[str] = []
    player_attributes: Dict[str, any] = {}

# In-memory storage
story_nodes: Dict[str, StoryNode] = {}
game_states: Dict[str, GameState] = {}

def load_story():
    """Load story from JSON config file"""
    story_path = Path("stories/quantum_paradox.json")
    try:
        with open(story_path) as f:
            story_data = json.load(f)

        for node_data in story_data["nodes"]:
            story_nodes[node_data["id"]] = StoryNode(**node_data)

        return story_data["start_node_id"]
    except Exception as e:
        print(f"Error loading story: {e}")
        raise

# Initialize story when app starts
start_node_id = load_story()

@app.post("/game/start")
async def start_game():
    session_id = str(uuid.uuid4())
    game_state = GameState(
        session_id=session_id,
        current_node_id=start_node_id,
        history=[],
        player_attributes={}
    )
    game_states[session_id] = game_state

    return {
        "session_id": session_id,
        "node": story_nodes[start_node_id],
        "player_attributes": game_state.player_attributes
    }

@app.post("/game/choice")
async def make_choice(session_id: str, choice_id: str):
    if session_id not in game_states:
        raise HTTPException(status_code=404, detail="Game session not found")

    game_state = game_states[session_id]
    current_node = story_nodes[game_state.current_node_id]

    # Find the chosen choice
    choice = next((c for c in current_node.choices if c.id == choice_id), None)
    if not choice:
        raise HTTPException(status_code=400, detail="Invalid choice")

    # Update game state
    game_state.history.append(game_state.current_node_id)
    game_state.current_node_id = choice.target_node_id

    # Get next node
    next_node = story_nodes[choice.target_node_id]
    next_node.visits += 1
    next_node.last_visited = datetime.now().isoformat()

    return {
        "node": next_node,
        "history": game_state.history,
        "player_attributes": game_state.player_attributes
    }

@app.get("/game/state/{session_id}")
async def get_game_state(session_id: str):
    logger.info(f"Getting game state for session: {session_id}")
    try:
        if session_id not in game_states:
            logger.warning(f"Session not found: {session_id}")
            raise HTTPException(status_code=404, detail="Game session not found")

        logger.debug(f"Current node: {game_state.current_node_id}")
        logger.debug(f"History length: {len(game_state.history)}")

        return {
            "current_node": story_nodes[game_state.current_node_id],
            "history": game_state.history,
            "player_attributes": game_state.player_attributes
        }
    except Exception as e:
        logger.error(f"Error getting game state: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
