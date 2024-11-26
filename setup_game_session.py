import uuid
import logging
import os
import subprocess
from pathlib import Path
from datetime import datetime
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_game_session():
    try:
        # Create base game_data directory
        base_dir = Path("game_data")
        base_dir.mkdir(exist_ok=True)

        # Generate single session ID
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = uuid.uuid4().hex
        session_id = f"{timestamp}_{unique_id}"

        # Create session directory
        session_dir = base_dir / "sessions" / session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created session directory: {session_dir}")

        # Create initial state file
        state = {
            "game_id": uuid.uuid1().hex,
            "session_id": session_id,
            "current_node_id": None,
            "player_state": {},
            "choice_history": [],
            "timeline": [
                {
                    "title": "Game Start",
                    "description": "Beginning of the journey",
                    "timestamp": datetime.now().isoformat()
                }
            ],
            "game_started": datetime.now().isoformat()
        }

        with open(session_dir / "state.json", 'w') as f:
            json.dump(state, f, indent=2)

        # Generate story configuration
        env = os.environ.copy()
        env["GAME_SESSION_ID"] = session_id

        # Run generate_story_config.py with session ID
        subprocess.run(
            ["python", "generate_story_config.py"],
            env=env,
            check=True
        )

        # Start the game with this session
        subprocess.run(
            ["python", "app.py", "--session-id", session_id],
            check=True
        )

    except Exception as e:
        logger.error(f"Failed to setup game session: {e}")
        raise

if __name__ == "__main__":
    setup_game_session()