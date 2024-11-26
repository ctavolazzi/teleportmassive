from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.absolute()
STORY_DIR = BASE_DIR / "stories"
LOGS_DIR = BASE_DIR / "logs"

# Ensure directories exist
STORY_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Game configuration
GAME_CONFIG = {
    "title": "Teleport Massive CYOA",
    "description": "An interactive story where your choices matter.",
    "author": "AI Storyteller",
    "version": "0.1.0",
    "story_file": STORY_DIR / "current_story.md",
    "max_choices": 4,
    "min_content_length": 100,
    "theme": {
        "primary_color": "#2E86C1",
        "secondary_color": "#85C1E9",
        "text_color": "#2C3E50",
        "background_color": "#ECF0F1"
    }
}

# Gradio interface configuration
GRADIO_CONFIG = {
    "server_port": 7860,
    "server_name": "0.0.0.0",
    "share": True,
    "theme": "default",
    "allow_flagging": False,
    "analytics_enabled": False
}

# Logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": LOGS_DIR / "game.log",
            "formatter": "standard"
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard"
        }
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "INFO"
        }
    }
}