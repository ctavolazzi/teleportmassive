from datetime import datetime
from typing import Annotated
import os
from autogen import ConversableAgent, register_function
from pydantic import BaseModel, Field
import logging
from dotenv import load_dotenv
import autogen
from pathlib import Path
from autogen.coding import LocalCommandLineCodeExecutor

load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('story_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class StoryGenerator:
    def __init__(self, story_dir: str = "stories"):
        """Initialize the story generator with Ollama configuration"""
        self.story_dir = Path(story_dir)
        self.story_dir.mkdir(exist_ok=True)

        # Create timestamped story file
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.story_file = self.story_dir / f"story_{self.timestamp}.md"
        logger.info(f"Story will be saved to: {self.story_file}")

        # Configure Ollama
        self.config_list = [{
            "model": "llama3.2",
            "api_type": "ollama",
            "client_host": "http://localhost:11434",
            "stream": False,
            "temperature": 0.7,
            "native_tool_calls": True,
            "hide_tools": "if_any_run"
        }]

        # Set up code execution environment
        self.workdir = Path("coding")
        self.workdir.mkdir(exist_ok=True)
        self.code_executor = LocalCommandLineCodeExecutor(work_dir=self.workdir)

        # Initialize agents
        self._setup_agents()
        self._register_tools()
        logger.info("Story Generator initialized with Ollama")

    def _setup_agents(self):
        """Set up the storyteller and reader agents"""
        system_message = """You are a creative AI storyteller who writes and expands stories in markdown format.
        Your task is to:
        1. Read the existing story from the markdown file
        2. Add new content that naturally continues the narrative
        3. Include descriptive elements and dialogue
        4. Save the expanded story back to the file
        5. Maintain consistent character development and plot progression

        When writing, follow these rules:
        - Each addition should be at least 2-3 paragraphs
        - Include atmospheric details and character emotions
        - Maintain continuity with previous content
        - Use markdown formatting for structure
        - End each section with a subtle hook for future expansion"""

        self.assistant = autogen.AssistantAgent(
            name="assistant",
            system_message=system_message,
            llm_config={"config_list": self.config_list}
        )

        self.user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            code_execution_config={"executor": self.code_executor}
        )

    def read_story(self) -> str:
        """Read the current story content"""
        try:
            with open(self.story_file, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            logger.info("No existing story found, starting fresh")
            return ""
        except Exception as e:
            logger.error(f"Error reading story: {e}")
            return ""

    def append_to_story(self, new_content: str) -> str:
        """Append new content to the story file"""
        try:
            current_content = self.read_story()

            # Clean up the content
            new_content = (new_content
                         .replace("***** Suggested tool call", "")
                         .replace("***** Response from calling tool", "")
                         .replace("*****", "")
                         .strip())

            with open(self.story_file, 'w') as f:
                if current_content:
                    # Check if this content is truly new
                    if new_content not in current_content:
                        logger.info("Appending new content to existing story")
                        f.write(f"{current_content}\n\n{new_content}")
                    else:
                        logger.info("Content already exists, skipping append")
                        f.write(current_content)
                else:
                    logger.info("Writing initial content")
                    f.write(new_content)

            logger.info(f"Successfully updated story in {self.story_file}")
            return "Successfully updated story"
        except Exception as e:
            logger.error(f"Error updating story: {e}")
            return f"Error updating story: {e}"

    def _register_tools(self):
        """Register tools with the agents"""
        # Create standalone functions for registration
        def read_story_func():
            return self.read_story()

        def append_to_story_func(content: str):
            return self.append_to_story(content)

        # Register the functions
        register_function(
            read_story_func,
            caller=self.assistant,
            executor=self.user_proxy,
            name="read_story",
            description="Read the current story content"
        )

        register_function(
            append_to_story_func,
            caller=self.assistant,
            executor=self.user_proxy,
            name="append_to_story",
            description="Append new content to the story"
        )

    def generate_story(self, prompt: str = None) -> str:
        """Generate or continue the story"""
        if prompt is None:
            prompt = """Create or continue the story in markdown format."""

        logger.info("Generating story content")

        # First, read existing content
        existing_content = self.read_story()
        if existing_content:
            prompt = f"""Continue this story:

{existing_content}

Continue from where this left off, maintaining the same style and atmosphere."""

        # Get the chat result
        chat_result = self.user_proxy.initiate_chat(
            self.assistant,
            message=prompt
        )

        # Process the last substantive message from the assistant
        last_content = None
        for message in self.user_proxy.chat_messages[self.assistant]:
            if (message["role"] == "assistant" and
                "content" in message and
                len(message["content"]) > 100 and  # Minimum length to filter out system messages
                not message["content"].startswith("*****")):  # Filter out tool calls
                last_content = message["content"]

        # If we found substantial content, save it
        if last_content:
            logger.info("Found new content to save")
            self.append_to_story(last_content)

        return chat_result

def main():
    """Main function to demonstrate usage"""
    generator = StoryGenerator()

    # Generate initial story
    initial_prompt = """
    Write the beginning of our story about Alex discovering an old manuscript.
    The story should include elements of mystery and subtle magic.
    """
    generator.generate_story(initial_prompt)

if __name__ == "__main__":
    main()