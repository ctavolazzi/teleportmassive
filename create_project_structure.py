import os
from pathlib import Path
import shutil

def create_core_structure():
    """Create the essential core game components"""
    base_dir = "teleport-massive"

    # Core structure for game mechanics
    core_structure = {
        "backend": {
            "core": {
                "files": [
                    "story_node.py",     # Base data structure
                    "choice.py",         # Choice data structure
                    "__init__.py"
                ]
            },
            "repositories": {
                "files": [
                    "story_node_repository.py",
                    "choice_repository.py",
                    "__init__.py"
                ]
            },
            "game": {
                "files": [
                    "game_state.py",     # Game state management
                    "game_engine.py",    # Core game logic
                    "__init__.py"
                ]
            },
            "files": [
                "main.py",              # Application entry point
                "requirements.txt",
                "__init__.py"
            ]
        }
    }

    def create_structure(current_path: Path, structure_dict: dict):
        """Recursively create directories and files"""
        # Create files at current level
        if "files" in structure_dict:
            for file in structure_dict["files"]:
                file_path = current_path / file
                if not file_path.exists():
                    file_path.touch()
                    print(f"Created file: {file_path}")

        # Create subdirectories and their contents
        for key, value in structure_dict.items():
            if key != "files":
                new_dir = current_path / key
                if not new_dir.exists():
                    new_dir.mkdir(parents=True)
                    print(f"Created directory: {new_dir}")
                if isinstance(value, dict):
                    create_structure(new_dir, value)

    # Create base directory
    base_path = Path(base_dir)
    if base_path.exists():
        print(f"Directory {base_path} already exists. Removing it...")
        shutil.rmtree(base_path)

    base_path.mkdir()
    print(f"Created base directory: {base_path}")

    # Create the structure
    create_structure(base_path, core_structure)

def create_api_structure():
    """Add API layer to existing structure"""
    api_structure = {
        "backend": {
            "api": {
                "files": [
                    "routes.py",         # API routes
                    "models.py",         # API models/schemas
                    "dependencies.py",    # FastAPI dependencies
                    "__init__.py"
                ]
            },
            "files": [
                "api.py"                # FastAPI application
            ]
        }
    }

    create_structure(Path("teleport-massive"), api_structure)

def create_frontend_structure():
    """Add frontend structure"""
    frontend_structure = {
        "frontend": {
            "src": {
                "components": {
                    "files": [
                        "StoryNode.svelte",
                        "ChoiceList.svelte",
                        "GameUI.svelte"
                    ]
                },
                "stores": {
                    "files": [
                        "gameStore.ts"
                    ]
                },
                "lib": {
                    "files": [
                        "audio.ts",
                        "themes.ts",
                        "types.ts"
                    ]
                },
                "files": [
                    "App.svelte",
                    "main.ts"
                ]
            },
            "public": {
                "audio": {
                    "files": [
                        "forest-ambient.mp3",
                        "cave-ambient.mp3"
                    ]
                },
                "styles": {
                    "files": [
                        "global.css"
                    ]
                }
            },
            "files": [
                "package.json",
                "svelte.config.js",
                "vite.config.js",
                "tsconfig.json"
            ]
        }
    }

    create_structure(Path("teleport-massive"), frontend_structure)

def create_tests_structure():
    """Add test structure"""
    tests_structure = {
        "tests": {
            "unit": {
                "files": [
                    "test_story_node.py",
                    "test_choice.py",
                    "test_game_engine.py",
                    "__init__.py"
                ]
            },
            "integration": {
                "files": [
                    "test_api.py",
                    "test_game_flow.py",
                    "__init__.py"
                ]
            },
            "files": [
                "conftest.py",
                "pytest.ini",
                "__init__.py"
            ]
        }
    }

    create_structure(Path("teleport-massive"), tests_structure)

def create_project():
    """Create complete project structure"""
    # 1. Create core structure
    create_core_structure()

    # 2. Add API layer
    create_api_structure()

    # 3. Add frontend
    create_frontend_structure()

    # 4. Add tests
    create_tests_structure()

    # 5. Add initial content to key files
    initialize_key_files()

    print("\nProject structure created successfully!")
    print_next_steps()

def initialize_key_files():
    """Initialize key files with basic content"""
    base_path = Path("teleport-massive")

    # Add .gitignore
    with open(base_path / ".gitignore", "w") as f:
        f.write(GITIGNORE_CONTENT)

    # Add README.md
    with open(base_path / "README.md", "w") as f:
        f.write(README_CONTENT)

    # Add requirements.txt
    with open(base_path / "backend" / "requirements.txt", "w") as f:
        f.write(REQUIREMENTS_CONTENT)

    # Add package.json
    with open(base_path / "frontend" / "package.json", "w") as f:
        f.write(PACKAGE_JSON_CONTENT)

def print_next_steps():
    """Print setup instructions"""
    print("\nNext steps:")
    print("1. cd teleport-massive")
    print("2. python -m venv venv")
    print("3. source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
    print("4. pip install -r backend/requirements.txt")
    print("5. cd frontend && npm install")

# File contents as constants
GITIGNORE_CONTENT = """
# Python
__pycache__/
*.py[cod]
*$py.class
venv/
.env

# Node
node_modules/
dist/
.svelte-kit/

# IDE
.vscode/
.idea/

# Database
*.db
*.sqlite3

# OS
.DS_Store
Thumbs.db
"""

# Add other content constants (README_CONTENT, REQUIREMENTS_CONTENT, etc.)

if __name__ == "__main__":
    create_project()