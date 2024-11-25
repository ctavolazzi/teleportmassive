import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main execution function"""
    try:
        # Create game_data directory if it doesn't exist
        Path("game_data").mkdir(exist_ok=True)

        # Run the session setup
        logger.info("Setting up game session...")
        subprocess.run(["python", "setup_game_session.py"], check=True)

    except Exception as e:
        logger.error(f"Error during game setup: {e}")
        raise

if __name__ == "__main__":
    main()