import autogen
from pathlib import Path
from autogen.coding import LocalCommandLineCodeExecutor

# Configuration for Ollama with Llama 3.2
config_list = [
    {
        "model": "llama3.2",  # Changed to Llama 3.2
        "api_type": "ollama",
        "client_host": "http://localhost:11434",
        "stream": False,
        "temperature": 0.7,
        "native_tool_calls": True,
        "hide_tools": "if_any_run"
    }
]

# Set up code execution environment
workdir = Path("coding")
workdir.mkdir(exist_ok=True)
code_executor = LocalCommandLineCodeExecutor(work_dir=workdir)

# Create the agents
system_message = """You are a creative AI storyteller who writes and expands stories in markdown format.
Your task is to:
1. Read the existing story from the markdown file (if it exists)
2. Add new content that naturally continues the narrative
3. Include descriptive elements and dialogue
4. Save the expanded story back to the file
5. Maintain consistent character development and plot progression

When writing, follow these rules:
- Each addition should be at least 2-3 paragraphs
- Include atmospheric details and character emotions
- Maintain continuity with previous content
- Use markdown formatting for structure
- End each section with a subtle hook for future expansion

If the story file doesn't exist, start a new one with an engaging opening.
After successfully writing or updating the story, respond with 'FINISH'."""

assistant = autogen.AssistantAgent(
    name="assistant",
    system_message=system_message,
    llm_config={"config_list": config_list}
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={"executor": code_executor},
    is_termination_msg=lambda msg: "FINISH" in msg.get("content", "")
)

# Start the chat
user_proxy.initiate_chat(
    assistant,
    message="""Create an ever-expanding story in markdown format. The story should:
1. Be saved in 'story.md' in the coding directory
2. Start with a character named Alex discovering an old manuscript
3. Include elements of mystery and subtle magic
4. Build naturally with each update
5. Use markdown headers, emphasis, and formatting

Please write the first part of the story or update the existing one."""
)