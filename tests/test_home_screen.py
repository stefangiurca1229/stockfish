import importlib
import tkinter as tk
from unittest.mock import patch

import pytest


def _has_display() -> bool:
    try:
        root = tk.Tk()
        root.destroy()
        return True
    except Exception:
        return False


requires_display = pytest.mark.skipif(
    not _has_display(), reason="no display available"
)


@requires_display
def test_build_home_screen_creates_two_buttons():
    from main import build_home_screen

    root = tk.Tk()
    build_home_screen(root)

    buttons = [w for w in root.winfo_children() if isinstance(w, tk.Button)]
    assert len(buttons) == 2

    labels = {b.cget("text") for b in buttons}
    assert "Play vs Stockfish" in labels
    assert "Play vs Player" in labels

    root.destroy()


def test_main_module_importable():
    import importlib
    import sys

    mod = importlib.import_module("main")
    assert callable(getattr(mod, "main", None))
    assert callable(getattr(mod, "build_home_screen", None))
