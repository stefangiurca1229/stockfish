"""Tests for the application's home screen UI.

These tests verify that the HomeScreen provided by main.py exposes the
expected visual elements and that their callbacks are callable. The
module includes fixtures that import the application module and create
an instance of the home screen for use by the tests.
"""

import sys
import pytest

pytest.importorskip('tkinter')

import tkinter as tk
from tkinter import Button

import importlib

@pytest.fixture(scope="module")
def app_module():
    """Import and return the main application module.

    This fixture attempts to import the top-level `main` module which is
    expected to define the HomeScreen class. If the module is not found
    the tests are skipped.
    """
    # Import the main app module (should be main.py)
    try:
        mod = importlib.import_module("main")
    except ModuleNotFoundError:
        pytest.skip("main.py not found")
    return mod

@pytest.fixture
def home_screen(app_module):
    """Create a Tkinter root and instantiate the HomeScreen.

    Yields a tuple (root, app) where `root` is the Tk root window and
    `app` is the HomeScreen instance. Ensures the root window is
    destroyed after the test to avoid leaking GUI state between tests.
    """
    # Create the Tk root and home screen
    root = tk.Tk()
    app = app_module.HomeScreen(root)
    yield root, app
    root.destroy()

def test_home_screen_buttons_exist(home_screen):
    """Ensure the expected buttons are present on the home screen.

    This test searches the root window for Button widgets and asserts
    that their labels match the expected list.
    """
    root, app = home_screen
    # Find all buttons in the root window
    buttons = [w for w in root.winfo_children() if isinstance(w, Button)]
    labels = sorted([b.cget("text") for b in buttons])
    assert labels == ["Play vs Player", "Play vs Stockfish"]


def test_button_callbacks_are_callable(home_screen):
    """Verify that button callbacks can be invoked without raising.

    The test iterates over all Button widgets on the home screen and
    calls their `invoke()` method to ensure the bound callbacks are
    callable and do not raise exceptions.
    """
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
    """Check basic visual properties of the home screen.

    For now this asserts the window title matches the expected
    application title.
    """
    root, app = home_screen
    # Check window title or other visual cues
    assert root.title() == "Stockfish Chess"
