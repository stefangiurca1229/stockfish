import os

# Path to Stockfish binary (default can be overridden by env var)
STOCKFISH_PATH = os.environ.get("STOCKFISH_PATH", "/usr/local/bin/stockfish")

# Default engine settings (can be extended as needed)
STOCKFISH_DEFAULT_OPTIONS = {
    "Threads": 1,
    "Hash": 16,
}
