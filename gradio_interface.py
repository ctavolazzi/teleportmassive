import gradio as gr
import logging
from pathlib import Path
from typing import Tuple, Dict, Any

from story_generator import StoryGenerator
from game_state import GameState

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TeleportMassiveUI:
    def __init__(self):
        self.story_generator = StoryGenerator()
        self.game_state = GameState()
        self.current_choices = []

    def update_story(self, choice: str, state: Dict[str, Any]) -> Tuple[str, list, Dict[str, Any]]:
        """Update the story based on user choice"""
        try:
            # Generate continuation based on the choice
            prompt = f"""Continue the story based on the choice: {choice}
            Maintain the same style and atmosphere. Include 2-3 paragraphs and end with 3-4 new choices."""

            result = self.story_generator.generate_story(prompt)

            # Update game state
            self.game_state.move_to(choice)

            # Extract current story content
            current_content = self.story_generator.read_story()

            # Parse choices from the content (basic implementation)
            choices = [line.strip('- ') for line in current_content.split('\n')
                      if line.strip().startswith('- ')]
            self.current_choices = choices

            return current_content, choices, self.game_state.get_state()

        except Exception as e:
            logger.error(f"Error updating story: {e}")
            return "An error occurred.", ["Restart"], self.game_state.get_state()

    def create_interface(self) -> gr.Blocks:
        """Create the Gradio interface"""
        with gr.Blocks(title="Teleport Massive CYOA") as interface:
            # Header
            gr.Markdown("# Teleport Massive: Choose Your Own Adventure")

            # Story display
            with gr.Row():
                story_display = gr.Markdown(value=self.story_generator.read_story() or "Loading story...")

            # Choices
            with gr.Row():
                choice_selector = gr.Radio(
                    choices=self.current_choices,
                    label="What will you do?",
                    interactive=True
                )

            # Submit button
            with gr.Row():
                submit_btn = gr.Button("Make Your Choice")

            # Game state (hidden from user but tracked)
            state = gr.State(self.game_state.get_state())

            # Event handlers
            submit_btn.click(
                fn=self.update_story,
                inputs=[choice_selector, state],
                outputs=[story_display, choice_selector, state]
            )

            # Initialize story if empty
            if not self.story_generator.read_story():
                initial_prompt = """
                Write the beginning of our story about Sam Iker waking up from a dream.
                Include elements of mystery and subtle magic.
                End with 3-4 clear choices for the reader.
                """
                self.story_generator.generate_story(initial_prompt)
                story_display.value = self.story_generator.read_story()

        return interface

def main():
    # Create and launch the interface
    ui = TeleportMassiveUI()
    interface = ui.create_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True
    )

if __name__ == "__main__":
    main()