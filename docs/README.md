# Stockfish Chess Engine Integration

A Python project that wraps the [Stockfish](https://stockfishchess.org/) chess engine and provides a terminal-based chess interface.

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Architecture](#architecture)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Project Structure](#project-structure)

## Overview

This project integrates the Stockfish chess engine into a Python application, exposing a clean interface for:

- Getting best-move suggestions given a FEN position string
- Configuring engine options (threads, hash table size, etc.)
- A terminal home screen to choose between playing against Stockfish or another player

Key implementation details:
- Non-blocking stdout reader (runs in a background thread)
- FEN validation via `python-chess`
- Configurable time limit per move

## Requirements

- Python 3.9+
- [Stockfish binary](https://stockfishchess.org/download/) installed on your system
- `python-chess` — see `requirements.txt`

## Installation

1. Install the Stockfish binary for your OS:

   **macOS (Homebrew)**
   ```bash
   brew install stockfish
   ```

   **Ubuntu/Debian**
   ```bash
   sudo apt-get install stockfish
   ```

   **Windows** — download from https://stockfishchess.org/download/

2. Clone the repository:
   ```bash
   git clone https://github.com/stefangiurca1229/stockfish.git
   cd stockfish
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

`config.py` controls engine defaults:

| Variable | Default | Description |
|---|---|---|
| `STOCKFISH_PATH` | `/usr/local/bin/stockfish` | Path to the Stockfish binary. Override with the `STOCKFISH_PATH` env var. |
| `STOCKFISH_DEFAULT_OPTIONS` | `{"Threads": 1, "Hash": 16}` | UCI options passed to the engine on startup. |

Override the binary path at runtime:
```bash
export STOCKFISH_PATH=/usr/games/stockfish
```

## Usage

### Getting a move suggestion

```python
from agents.stockfish_engine import StockfishEngine

engine = StockfishEngine("/usr/local/bin/stockfish")

fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
move = engine.suggest_move(fen, time_limit=1.0)
print(move)  # e.g. "e2e4"

engine.quit()
```

### Using custom engine options

```python
options = {
    "Threads": 4,
    "Hash": 128,
    "Skill Level": 10,
}
engine = StockfishEngine(path="/usr/local/bin/stockfish", options=options)
```

### Home Screen (terminal UI)

```python
from ui.home_screen import HomeScreen

screen = HomeScreen()
print(screen.render())
choice = screen.select(1)  # "stockfish" or "player"
```

## Architecture

```
.
├── agents/
│   └── stockfish_engine.py   # StockfishEngine — subprocess wrapper around the UCI protocol
├── ui/
│   └── home_screen.py        # HomeScreen — terminal menu component
├── tests/
│   ├── test_stockfish_engine.py
│   └── test_home_screen.py
├── config.py                 # Engine path and default UCI options
├── docs/
│   └── README.md             # This file
└── requirements.txt
```

### StockfishEngine

Communicates with Stockfish over stdin/stdout using the [UCI protocol](https://www.shredderchess.com/chess-features/uci-universal-chess-interface.html). A dedicated reader thread drains stdout into a `queue.Queue` to prevent deadlocks.

Lifecycle:
1. `__init__` — spawns the subprocess and calls `_init_engine`
2. `_init_engine` — sends `uci` / `isready` handshake and applies any configured options
3. `suggest_move` — sends `position fen <fen>` + `go movetime <ms>`, waits for `bestmove`
4. `quit` — sends `quit` and closes all streams

### HomeScreen

A pure-Python terminal menu. `render()` returns a formatted ASCII box; `select()` accepts an integer index or a string key/label.

## API Reference

### `StockfishEngine(path, options=None)`

Starts a Stockfish subprocess and initializes the UCI protocol.

| Parameter | Type | Description |
|---|---|---|
| `path` | `str` | Absolute path to the Stockfish binary |
| `options` | `dict` \| `None` | UCI engine options (e.g. `{"Threads": 4, "Hash": 128}`). Defaults to `{}`. |

#### `suggest_move(fen, time_limit=1.0) -> str`

Returns the best move in UCI format (e.g. `"e2e4"`, `"e7e8q"`).

| Parameter | Type | Default | Description |
|---|---|---|---|
| `fen` | `str` | — | A valid FEN string representing the board position. |
| `time_limit` | `float` | `1.0` | Maximum search time in seconds. |

Raises:
- `ValueError` — if the FEN string is invalid.
- `RuntimeError` — if Stockfish does not return a move within the time limit.

#### `quit()`

Shuts down the engine subprocess. Safe to call multiple times.

---

### `HomeScreen(title="Welcome", buttons=None)`

| Parameter | Type | Description |
|---|---|---|
| `title` | `str` | Title displayed at the top of the menu |
| `buttons` | `dict` | `{key: (label, callback)}` mapping |

#### `render() -> str`

Returns the ASCII menu string ready to print.

#### `select(choice) -> str`

Accepts an `int` (1-based index) or `str` (key or label). Invokes the button's callback if set. Returns the selected key.

Raises `ValueError` for an out-of-range index or unrecognised string.

## Testing

Tests require a real Stockfish binary and are skipped automatically when it is not found.

```bash
pytest tests/
```

Set `STOCKFISH_PATH` to point at your binary:

```bash
STOCKFISH_PATH=/usr/games/stockfish pytest tests/
```

### Test coverage

| Test | Description |
|---|---|
| `test_suggest_move_from_fen` | Verifies a legal UCI move is returned for the starting position. |
| `test_invalid_fen_raises` | Ensures `ValueError` is raised for a malformed FEN. |
| `test_time_limit` | Confirms a move is returned within the specified time limit. |
| `test_quit_idempotent` | Ensures calling `quit()` multiple times does not raise. |
