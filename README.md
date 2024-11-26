# Teleport Massive

**Teleport Massive** is an immersive Choose Your Own Adventure (CYOA) game built using Python, FastAPI, SQLite, and Svelte. It offers dynamic storytelling, interactive choices, and a responsive web interface to provide an engaging user experience.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Directory Structure](#directory-structure)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Interactive Storytelling**: Navigate through a branching narrative with multiple story paths.
- **Responsive UI**: Modern and responsive design ensures a seamless experience across devices.
- **Persistent Game State**: Track your progress and revisit previous decisions.
- **Dynamic Theming**: Visual themes adapt based on story context for enhanced immersion.
- **Audio Effects**: Ambient sounds and sound effects enrich the storytelling experience.
- **Modular Architecture**: Clean separation of concerns facilitates easy maintenance and scalability.

## Tech Stack

- **Backend**: Python, FastAPI, SQLite
- **Frontend**: Svelte
- **Others**:
  - **Dataclasses** for structured data
  - **SQLite** for lightweight data storage
  - **Svelte Stores** for state management
  - **Web Audio API** for audio effects
  - **Vite** for frontend tooling

## Setup Instructions

### Prerequisites

- **Python**: Version 3.10 or higher
- **Node.js**: Version 14 or higher
- **npm** or **yarn**: Package managers for JavaScript

### Backend Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/teleport-massive.git
   cd teleport-massive
   ```

2. **Set Up Python Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Backend Dependencies**

   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Initialize the Database**

   This will create the necessary tables and insert initial story data.

   ```bash
   python backend/main.py
   ```

5. **Run the Backend Server**

   ```bash
   uvicorn backend.api:app --reload
   ```

   The backend API will be accessible at `http://localhost:8000`.

### Frontend Setup

1. **Navigate to the Frontend Directory**

   ```bash
   cd frontend
   ```

2. **Install Frontend Dependencies**

   ```bash
   npm install
   # or
   yarn install
   ```

3. **Run the Frontend Development Server**

   ```bash
   npm run dev
   # or
   yarn dev
   ```

   The frontend application will be accessible at `http://localhost:5173`.

4. **Access the Game**

   Open your browser and navigate to `http://localhost:5173` to start playing **Teleport Massive**.

## Directory Structure

teleport-massive/
├── backend/
│   ├── api.py
│   ├── game_engine.py
│   ├── game_state.py
│   ├── choice.py
│   ├── choice_repository.py
│   ├── story_node.py
│   ├── story_node_repository.py
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.svelte
│   │   ├── audio.ts
│   │   ├── stores/
│   │   │   └── gameStore.ts
│   │   ├── themes.ts
│   │   └── types.ts
│   ├── public/
│   │   └── audio/
│   │       ├── forest-ambient.mp3
│   │       └── cave-ambient.mp3
│   ├── package.json
│   ├── svelte.config.js
│   └── vite.config.js
├── tests/
│   ├── test_story_node.py
│   ├── test_choice.py
│   └── test_game_engine.py
├── README.md
└── .gitignore



### Description of Key Directories and Files

#### `backend/`

Contains all backend-related code, including data models, repositories, game logic, and API endpoints.

- **`api.py`**: Defines RESTful API endpoints using FastAPI.
- **`game_engine.py`**: Implements the core game logic and manages game flow.
- **`game_state.py`**: Tracks the current state of the game for each player.
- **`choice.py`**: Defines the `Choice` data structure.
- **`choice_repository.py`**: Handles CRUD operations for choices in the database.
- **`story_node.py`**: Defines the `StoryNode` data structure.
- **`story_node_repository.py`**: Handles CRUD operations for story nodes in the database.
- **`main.py`**: Entry point for initializing the database and starting the backend server.
- **`requirements.txt`**: Lists all Python dependencies for the backend.

#### `frontend/`

Contains all frontend-related code built with Svelte, including components, styles, and assets.

- **`src/`**: Source code for the frontend application.
  - **`App.svelte`**: Main Svelte component that orchestrates the UI.
  - **`audio.ts`**: Manages audio playback for ambient sounds and effects.
  - **`stores/gameStore.ts`**: Implements Svelte stores for state management.
  - **`themes.ts`**: Defines dynamic themes based on story context.
  - **`types.ts`**: TypeScript definitions for data structures.
- **`public/`**: Static assets served by the frontend.
  - **`audio/`**: Contains audio files for ambient sounds and sound effects.
    - **`forest-ambient.mp3`**: Ambient sound for forest scenes.
    - **`cave-ambient.mp3`**: Ambient sound for cave scenes.
- **`package.json`**: Lists all JavaScript dependencies and scripts for the frontend.
- **`svelte.config.js`**: Configuration file for Svelte.
- **`vite.config.js`**: Configuration file for Vite, the frontend build tool.

#### `tests/`

Contains all test cases for the project to ensure code reliability and correctness.

- **`test_story_node.py`**: Tests for the `StoryNode` data structure and repository.
- **`test_choice.py`**: Tests for the `Choice` data structure and repository.
- **`test_game_engine.py`**: Tests for the `GameEngine` functionality.

#### Root Directory

- **`README.md`**: Overview and setup instructions for the project.
- **`.gitignore`**: Specifies files and directories to be ignored by Git.

## Usage

1. **Start the Backend Server**

   ```bash
   cd backend
   uvicorn api:app --reload
   ```

2. **Start the Frontend Server**

   ```bash
   cd frontend
   npm run dev
   ```

3. **Play the Game**

   Open your browser and go to `http://localhost:5173` to start your adventure in **Teleport Massive**.

## Contributing

Contributions are welcome! To contribute:

1. **Fork the Repository**

   Click on the "Fork" button at the top right of the repository page.

2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/YourFeatureName
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add some feature"
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeatureName
   ```

5. **Open a Pull Request**

   Navigate to your forked repository and open a pull request with a detailed description of your changes.

## License

This project is licensed under the [MIT License](LICENSE).
