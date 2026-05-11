# Stockfish Chess Engine Integration

A Python project that wraps the [Stockfish](https://stockfishchess.org/) chess engine and provides a terminal-based chess interface.

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Architecture](#architecture)
- [Testing](#testing)
- [API Reference](#api-reference)

## Overview

This project integrates the Stockfish chess engine into a Python application, exposing a clean interface for:

- Getting best-move suggestions given a FEN position string
- Configuring engine options (threads, hash table size, etc.)
- A terminal home screen to choose between playing against Stockfish or another player

## Requirements

- Python 3.9+
- [Stockfish binary](https://stockfishchess.org/download/) installed on your system
- `python-chess` — see `requirements.txt`

## Installation

1. Install the Stockfish binary for your OS and note its path.
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
| `STOCKFISH_DEFAULT_OPTIONS` | `Threads=1, Hash=16` | UCI options passed to the engine on startup. |

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

## Testing

```bash
pytest tests/
```

Integration tests that require the Stockfish binary are skipped automatically when the binary is not found. Set `STOCKFISH_PATH` to point at your binary to run them:

```bash
STOCKFISH_PATH=/usr/games/stockfish pytest tests/
```

## API Reference

### `StockfishEngine(path, options=None)`

| Parameter | Type | Description |
|---|---|---|
| `path` | `str` | Absolute path to the Stockfish binary |
| `options` | `dict` | UCI engine options (e.g. `{"Threads": 4, "Hash": 128}`) |

#### `suggest_move(fen, time_limit=1.0) -> str`

Returns the best move in UCI notation (e.g. `"e2e4"`).

Raises `ValueError` for an invalid FEN string, `RuntimeError` if no move is returned within the time limit.

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
