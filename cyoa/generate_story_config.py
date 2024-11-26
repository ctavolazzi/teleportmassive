import uuid
import json
import logging
from datetime import datetime
import os
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def generate_id() -> str:
    return uuid.uuid1().hex

# Generate IDs for all nodes and choices
nodes = {}

# Starting node
start_node_id = generate_id()
nodes[start_node_id] = {
    "id": start_node_id,
    "type": "story_start",
    "title": "The Quantum Paradox",
    "content": """You are Dr. Sarah Chen, a quantum physicist at the Temporal Research Institute.
    Late one night, your quantum computer displays unprecedented readings. Three distinct
    anomalies appear on your screen...""",
    "choices": [
        {
            "id": generate_id(),
            "text": "Investigate the time dilation anomaly",
            "target_node_id": None
        },
        {
            "id": generate_id(),
            "text": "Examine the parallel universe breach",
            "target_node_id": None
        },
        {
            "id": generate_id(),
            "text": "Study the quantum entanglement spike",
            "target_node_id": None
        }
    ],
    "metadata": {},
    "visits": 0,
    "last_visited": None
}

# Layer 1: Initial Investigation Outcomes
time_dilation_id = generate_id()
nodes[time_dilation_id] = {
    "id": time_dilation_id,
    "type": "story_branch",
    "title": "Temporal Distortion",
    "content": """The time dilation readings are off the charts. Your watch begins running at
    different speeds across your field of vision. Through the lab window, you notice cars
    moving in slow motion while your computer displays time accelerating rapidly.""",
    "choices": [
        {
            "id": generate_id(),
            "text": "Attempt to stabilize the temporal field",
            "target_node_id": None
        },
        {
            "id": generate_id(),
            "text": "Document the phenomenon for research",
            "target_node_id": None
        }
    ],
    "metadata": {},
    "visits": 0,
    "last_visited": None
}

parallel_universe_id = generate_id()
nodes[parallel_universe_id] = {
    "id": parallel_universe_id,
    "type": "story_branch",
    "title": "Reality Breach",
    "content": """As you examine the breach, reality itself seems to split. Through a
    shimmering tear in space-time, you see another version of your lab where everything
    is slightly different. A parallel version of yourself stares back in amazement.""",
    "choices": [
        {
            "id": generate_id(),
            "text": "Attempt to communicate with your parallel self",
            "target_node_id": None
        },
        {
            "id": generate_id(),
            "text": "Try to seal the breach",
            "target_node_id": None
        }
    ],
    "metadata": {},
    "visits": 0,
    "last_visited": None
}

quantum_spike_id = generate_id()
nodes[quantum_spike_id] = {
    "id": quantum_spike_id,
    "type": "story_branch",
    "title": "Quantum Entanglement",
    "content": """The quantum entanglement readings reveal an unprecedented level of
    particle synchronization. Objects in your lab begin to mirror each other's movements,
    and you feel a strange connection to the quantum fabric of reality.""",
    "choices": [
        {
            "id": generate_id(),
            "text": "Attempt to harness the quantum synchronization",
            "target_node_id": None
        },
        {
            "id": generate_id(),
            "text": "Try to break the entanglement",
            "target_node_id": None
        }
    ],
    "metadata": {},
    "visits": 0,
    "last_visited": None
}

# Layer 2: Consequences
temporal_mastery_id = generate_id()
nodes[temporal_mastery_id] = {
    "id": temporal_mastery_id,
    "type": "story_branch",
    "title": "Temporal Mastery",
    "content": """Your attempts to stabilize the temporal field have given you unprecedented
    control over local time flow. You can now create controlled time bubbles and manipulate
    the flow of time within them.""",
    "choices": [
        {
            "id": generate_id(),
            "text": "Use your power to prevent future disasters",
            "target_node_id": None
        },
        {
            "id": generate_id(),
            "text": "Focus on understanding the implications",
            "target_node_id": None
        }
    ],
    "metadata": {},
    "visits": 0,
    "last_visited": None
}

multiverse_explorer_id = generate_id()
nodes[multiverse_explorer_id] = {
    "id": multiverse_explorer_id,
    "type": "story_branch",
    "title": "Multiverse Explorer",
    "content": """Through your interaction with the parallel universe, you've gained the
    ability to perceive and navigate multiple realities simultaneously. The multiverse
    has become your laboratory.""",
    "choices": [
        {
            "id": generate_id(),
            "text": "Establish a multiverse research network",
            "target_node_id": None
        },
        {
            "id": generate_id(),
            "text": "Search for the optimal timeline",
            "target_node_id": None
        }
    ],
    "metadata": {},
    "visits": 0,
    "last_visited": None
}

quantum_master_id = generate_id()
nodes[quantum_master_id] = {
    "id": quantum_master_id,
    "type": "story_branch",
    "title": "Quantum Master",
    "content": """Your manipulation of quantum entanglement has given you deep insight into
    the fundamental nature of reality. You can now influence probability itself.""",
    "choices": [
        {
            "id": generate_id(),
            "text": "Use probability manipulation for humanity's benefit",
            "target_node_id": None
        },
        {
            "id": generate_id(),
            "text": "Explore the deeper mysteries of quantum reality",
            "target_node_id": None
        }
    ],
    "metadata": {},
    "visits": 0,
    "last_visited": None
}

# Final Endings
time_lord_ending_id = generate_id()
nodes[time_lord_ending_id] = {
    "id": time_lord_ending_id,
    "type": "story_end",
    "title": "Master of Time",
    "content": """Your mastery of temporal mechanics has given humanity control over time itself.
    You've become the first Time Lord of Earth. THE END.""",
    "choices": [],
    "metadata": {
        "ending_type": "legendary",
        "achievement": "Time Lord"
    },
    "visits": 0,
    "last_visited": None
}

# Connect all nodes
def connect_story_nodes():
    # Connect time dilation branch
    time_dilation_choice = next(
        choice for choice in nodes[start_node_id]["choices"]
        if choice["text"] == "Investigate the time dilation anomaly"
    )
    time_dilation_choice["target_node_id"] = time_dilation_id

    # Connect parallel universe branch
    parallel_choice = next(
        choice for choice in nodes[start_node_id]["choices"]
        if choice["text"] == "Examine the parallel universe breach"
    )
    parallel_choice["target_node_id"] = parallel_universe_id

    # Connect quantum spike branch
    quantum_choice = next(
        choice for choice in nodes[start_node_id]["choices"]
        if choice["text"] == "Study the quantum entanglement spike"
    )
    quantum_choice["target_node_id"] = quantum_spike_id

    # Layer 1 to Layer 2 connections
    # Time dilation path
    stabilize_choice = next(
        choice for choice in nodes[time_dilation_id]["choices"]
        if choice["text"] == "Attempt to stabilize the temporal field"
    )
    stabilize_choice["target_node_id"] = temporal_mastery_id

    # Parallel universe path
    communicate_choice = next(
        choice for choice in nodes[parallel_universe_id]["choices"]
        if choice["text"] == "Attempt to communicate with your parallel self"
    )
    communicate_choice["target_node_id"] = multiverse_explorer_id

    # Quantum path
    harness_choice = next(
        choice for choice in nodes[quantum_spike_id]["choices"]
        if choice["text"] == "Attempt to harness the quantum synchronization"
    )
    harness_choice["target_node_id"] = quantum_master_id

    # Layer 2 to Endings
    # All paths can lead to becoming a Time Lord if the right choices are made
    for node_id in [temporal_mastery_id, multiverse_explorer_id, quantum_master_id]:
        for choice in nodes[node_id]["choices"]:
            choice["target_node_id"] = time_lord_ending_id

# Create the story configuration
story_config = {
    "nodes": list(nodes.values()),
    "start_node_id": start_node_id
}

def save_story_config():
    session_id = os.environ.get('GAME_SESSION_ID')
    if not session_id:
        raise ValueError("No session ID provided")

    session_dir = Path("game_data/sessions") / session_id
    config_path = session_dir / "story_config.json"

    with open(config_path, 'w') as f:
        json.dump(story_config, f, indent=2)

    logger.info(f"Story configuration saved to {config_path}")

# Connect nodes and save configuration
connect_story_nodes()
save_story_config()

print("Story configuration has been generated and saved to story_config.json")