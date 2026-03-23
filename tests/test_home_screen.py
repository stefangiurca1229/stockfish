import sys
import pytest

pytest.importorskip('tkinter')

import tkinter as tk
from tkinter import Button

import importlib

@pytest.fixture(scope="module")
def app_module():
    # Import the main app module (should be main.py)
    try:
        mod = importlib.import_module("main")
    except ModuleNotFoundError:
        pytest.skip("main.py not found")
    return mod

@pytest.fixture
def home_screen(app_module):
    # Create the Tk root and home screen
    root = tk.Tk()
    app = app_module.HomeScreen(root)
    yield root, app
    root.destroy()

def test_home_screen_buttons_exist(home_screen):
    root, app = home_screen
    # Find all buttons in the root window
    buttons = [w for w in root.winfo_children() if isinstance(w, Button)]
    labels = sorted([b.cget("text") for b in buttons])
    assert labels == ["Play vs Player", "Play vs Stockfish"]

def test_button_callbacks_are_callable(home_screen):
    root, app = home_screen
    # Find all buttons
    buttons = [w for w in root.winfo_children() if isinstance(w, Button)]
    for b in buttons:
        # Simulate button press
        try:
            b.invoke()
        except Exception as e:
            pytest.fail(f"Button '{b.cget('text')}' callback raised: {e}")

def test_home_screen_visual_elements(home_screen):
    root, app = home_screen
    # Check window title or other visual cues
    assert root.title() == "Stockfish Chess"
