import os
import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Union, Set
from dotenv import load_dotenv

load_dotenv()

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

# Third-party imports
from dotenv import load_dotenv
from autogen import ConversableAgent, UserProxyAgent
from autogen.coding import CodeBlock, DockerCommandLineCodeExecutor

# Local imports
from cyoa.game_state import GameState

# Constants and paths
BASE_DIR = Path(__file__).parent.absolute()
LOGS_DIR = BASE_DIR / "logs"
GENERATED_CODE_DIR = BASE_DIR / "generated_code"

# Create necessary directories
LOGS_DIR.mkdir(exist_ok=True)
GENERATED_CODE_DIR.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(processName)s | %(threadName)s | %(name)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(LOGS_DIR / f"autogen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AutogenGame:
    def __init__(self):
        """Initialize the game with configurations and agents"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        # Set up working directory for code execution
        self.work_dir = BASE_DIR / "coding"
        self.work_dir.mkdir(exist_ok=True)

        # Configure OpenAI settings
        self.config_list = [
            {
                "model": "gpt-4o-mini",
                "api_key": self.api_key,
                "timeout": 120,
            }
        ]

        # Assistant configuration
        self.assistant_config = {
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0.7,
            "timeout": 120,
        }

        # System message for the assistant
        self.assistant_system_message = """You are an AI game developer creating a text-based Choose Your Own Adventure game.
Your task is to:
1. Generate engaging game content
2. Track game state
3. Handle player choices
4. Create immersive narratives

When writing code:
1. Use clear, well-documented functions
2. Include error handling
3. Follow Python best practices
4. Save generated code to files

Begin by creating the initial game scene and core game mechanics."""

        # Set up code executor
        self.code_executor = DockerCommandLineCodeExecutor(
            work_dir=self.work_dir
        )

        # Initialize agents
        self.setup_agents()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup"""
        self.cleanup()

    def setup_agents(self):
        """Set up the AI agents for the game"""
        logger.info("Setting up agents")

        # Create the assistant agent with updated system message
        self.assistant = ConversableAgent(
            name="assistant",
            system_message="""You are an AI game developer creating a text-based Choose Your Own Adventure game.
Your task is to:
1. Generate engaging game content
2. Track game state
3. Handle player choices
4. Create immersive narratives

When writing code:
1. Use clear, well-documented functions
2. Include error handling
3. Follow Python best practices
4. Save generated code to files

Begin by creating the initial game scene and core game mechanics.""",
            llm_config=self.assistant_config,
            code_execution_config={"executor": self.code_executor},
            human_input_mode="NEVER",
            max_consecutive_auto_reply=3
        )

        # Create the user proxy agent
        self.user_proxy = UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            code_execution_config={"executor": self.code_executor},
            system_message="""You are a user testing the CYOA game.
Your role is to:
1. Request game content generation
2. Test game functionality
3. Provide feedback on game mechanics
4. Verify game state tracking
Do not engage in casual conversation."""
        )

        # Add code saving functionality
        def save_generated_code(content: str, agent_name: str):
            """Save code blocks found in the message content with proper file extensions"""
            if isinstance(content, dict):
                content = content.get("content", "")
            elif not isinstance(content, str):
                return

            # Define standard file extensions mapping
            EXTENSION_MAP = {
                'python': 'py',
                'py': 'py',
                'javascript': 'js',
                'js': 'js',
                'typescript': 'ts',
                'ts': 'ts',
                'markdown': 'md',
                'md': 'md',
                'html': 'html',
                'css': 'css',
                'json': 'json',
                'yaml': 'yaml',
                'yml': 'yml',
                'shell': 'sh',
                'bash': 'sh',
                'sh': 'sh',
                'sql': 'sql',
                'rust': 'rs',
                'go': 'go',
                'java': 'java',
                'cpp': 'cpp',
                'c++': 'cpp',
                'c': 'c',
                'ruby': 'rb',
                'rb': 'rb',
                'php': 'php',
                'swift': 'swift',
                'kotlin': 'kt',
                'scala': 'scala',
                'r': 'r',
                'dockerfile': 'dockerfile',
                'docker': 'dockerfile',
            }

            if "```" in content:
                code_blocks = content.split("```")
                for i in range(1, len(code_blocks), 2):
                    if code_blocks[i]:
                        # Extract language and code
                        lines = code_blocks[i].split('\n')
                        first_line = lines[0].strip().lower()  # Normalize language string

                        # Handle language specification with filepath
                        if ':' in first_line:
                            lang_spec, filepath = first_line.split(':', 1)
                            lang = lang_spec.strip()
                            # Use existing extension if filepath provided
                            ext = Path(filepath).suffix[1:] if Path(filepath).suffix else EXTENSION_MAP.get(lang, 'txt')
                        else:
                            lang = first_line
                            ext = EXTENSION_MAP.get(lang, 'txt')
                            filepath = None

                        code = '\n'.join(lines[1:]) if len(lines) > 1 else lines[0]

                        # Create timestamp and filename
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        code_dir = BASE_DIR / "generated_code"
                        code_dir.mkdir(exist_ok=True)

                        if filepath:
                            # Use specified path but maintain timestamp
                            full_path = code_dir / f"{timestamp}_{agent_name}_{filepath}"
                            full_path.parent.mkdir(parents=True, exist_ok=True)
                            filename = full_path
                        else:
                            # Generate filename with proper extension
                            filename = code_dir / f"{timestamp}_{agent_name}.{ext}"

                        # Add metadata as comments using language-appropriate syntax
                        COMMENT_SYNTAX = {
                            'py': '#',
                            'js': '//',
                            'ts': '//',
                            'java': '//',
                            'cpp': '//',
                            'c': '//',
                            'rb': '#',
                            'php': '//',
                            'swift': '//',
                            'kt': '//',
                            'scala': '//',
                            'r': '#',
                            'sql': '--',
                            'sh': '#',
                            'yaml': '#',
                            'yml': '#',
                            'dockerfile': '#',
                        }

                        comment_char = COMMENT_SYNTAX.get(ext, '#')
                        metadata = [
                            f"{comment_char} Generated by {agent_name}",
                            f"{comment_char} Timestamp: {datetime.now().isoformat()}",
                            f"{comment_char} Language: {lang}",
                            f"{comment_char} File: {filename.name}",
                            ""  # Empty line after metadata
                        ]

                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write('\n'.join(metadata))
                            f.write(code)

                        logger.info(f"Saved generated code to {filename}")

        # Store original receive methods
        assistant_original_receive = self.assistant.receive
        user_proxy_original_receive = self.user_proxy.receive

        # Create wrapped receive methods
        def assistant_receive(message, sender, request_reply=False, silent=False):
            save_generated_code(message, "assistant")
            return assistant_original_receive(message, sender, request_reply, silent)

        def user_proxy_receive(message, sender, request_reply=False, silent=False):
            save_generated_code(message, "user_proxy")
            return user_proxy_original_receive(message, sender, request_reply, silent)

        # Replace receive methods with wrapped versions
        self.assistant.receive = assistant_receive
        self.user_proxy.receive = user_proxy_receive

    def start_game(self):
        """Start the game interaction between agents"""
        logger.info("Starting Autogen CYOA game")

        try:
            # Initial game setup message with clear instructions
            self.user_proxy.initiate_chat(
                self.assistant,
                message="""Generate the following game components:

1. Create the initial game scene in markdown format
2. Write a Python class to track game state
3. Implement a function to handle player choices
4. Create a logging system for game actions

Begin with the first task: Create the initial game scene in markdown.""",
                clear_history=True  # Clear any previous conversation
            )

        except Exception as e:
            logger.error(f"Error during game execution: {str(e)}")
            raise

    def cleanup(self):
        """Cleanup resources"""
        try:
            self.code_executor.stop()
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")

def main():
    """Main entry point for the game"""
    try:
        # Initialize game
        game = AutogenGame()
        logger.info("Starting Autogen CYOA game")

        # Set up initial game state
        game_state = GameState()

        # Start the game loop
        while True:
            # Get current scene and choices
            current_scene = game.get_current_scene(game_state)
            print(current_scene)

            # Get player input
            try:
                choice = int(input("Enter your choice (or 0 to quit): "))
                if choice == 0:
                    break

                # Process player choice
                game.process_choice(choice, game_state)

            except ValueError:
                print("Please enter a valid number")
            except Exception as e:
                logger.error(f"Error processing choice: {e}")
                print("Something went wrong. Please try again.")

    except KeyboardInterrupt:
        print("\nGame terminated by user")
    except Exception as e:
        logger.error(f"Game error: {e}")
        print("An error occurred. Please check the logs.")
    finally:
        logger.info("Game ended")

if __name__ == "__main__":
    main()