import gradio as gr
import uuid
from datetime import datetime
from typing import Dict, List, Optional
import logging
import os
import sqlite3
from pathlib import Path

# Database setup
DB_PATH = Path("cyoa.db")

def init_db():
    """Initialize the database with required tables."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create story_nodes table
    c.execute('''
        CREATE TABLE IF NOT EXISTS story_nodes (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create choices table with foreign keys
    c.execute('''
        CREATE TABLE IF NOT EXISTS choices (
            id TEXT PRIMARY KEY,
            node_id TEXT NOT NULL,
            text TEXT NOT NULL,
            target_node_id TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (node_id) REFERENCES story_nodes(id),
            FOREIGN KEY (target_node_id) REFERENCES story_nodes(id)
        )
    ''')

    conn.commit()
    conn.close()

def insert_initial_story():
    """Insert the initial story nodes and choices into the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Check if we already have story nodes
    c.execute('SELECT COUNT(*) FROM story_nodes')
    if c.fetchone()[0] > 0:
        conn.close()
        return

    # Insert story nodes
    nodes = [
        ("start", "The Crossroads", "You stand at a crossroads in a dark forest. Paths lead to the **left** and **right**."),
        ("left_path", "A Peaceful Meadow", "You find yourself in a peaceful meadow filled with wildflowers."),
        ("right_path", "A Dark Cave", "You enter a dark cave. The sound of dripping water echoes around you."),
        ("pick_flowers", "Flower Picking", "You gather a beautiful bouquet of wildflowers."),
        ("rest_meadow", "Resting", "You take a peaceful rest in the meadow, feeling refreshed."),
        ("light_torch", "Lit Path", "With your torch lit, you see sparkling gems in the cave walls."),
        ("proceed_dark", "Stumble in the Dark", "You trip over a rock and decide it's best to turn back."),
        ("collect_gems", "Gem Collector", "You collect the gems and feel a sense of accomplishment."),
        ("end", "The End", "You reach the end of the story.")
    ]

    # Insert story nodes into the database
    c.executemany('INSERT INTO story_nodes (id, title, content) VALUES (?, ?, ?)', nodes)

    # Insert choices into the database
    choices = [
        ("choice1", "start", "Go left", "left_path", "2023-04-01 12:00:00"),
        ("choice2", "start", "Go right", "right_path", "2023-04-01 12:00:00"),
        ("choice3", "left_path", "Pick flowers", "pick_flowers", "2023-04-01 12:00:00"),
        ("choice4", "left_path", "Rest", "rest_meadow", "2023-04-01 12:00:00"),
        ("choice5", "right_path", "Proceed", "proceed_dark", "2023-04-01 12:00:00"),
        ("choice6", "right_path", "Turn back", "end", "2023-04-01 12:00:00"),
        ("choice7", "pick_flowers", "Collect gems", "collect_gems", "2023-04-01 12:00:00"),
        ("choice8", "collect_gems", "End", "end", "2023-04-01 12:00:00")
    ]

    # Insert choices into the database
    c.executemany('INSERT INTO choices (id, node_id, text, target_node_id, created_at) VALUES (?, ?, ?, ?, ?)', choices)

    conn.commit()
    conn.close()