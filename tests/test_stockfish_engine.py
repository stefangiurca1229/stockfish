import pytest
import os
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents import stockfish_engine

STOCKFISH_PATH = os.environ.get("STOCKFISH_PATH", "/usr/local/bin/stockfish")

@pytest.fixture(scope="module")
def engine():
    # Use the real Stockfish binary if available, else skip
    if not os.path.exists(STOCKFISH_PATH):
        pytest.skip("Stockfish binary not found at {}".format(STOCKFISH_PATH))
    engine = stockfish_engine.StockfishEngine(STOCKFISH_PATH)
    yield engine
    engine.quit()

def test_suggest_move_from_fen(engine):
    # Standard starting position
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    move = engine.suggest_move(fen)
    assert isinstance(move, str)
    assert len(move) in (4, 5)  # e.g., e2e4 or e7e8q
    # Should be a legal move in UCI format
    assert move[:2] in [f'{f}{r}' for f in 'abcdefgh' for r in '12345678']
    assert move[2:4] in [f'{f}{r}' for f in 'abcdefgh' for r in '12345678']

def test_invalid_fen_raises(engine):
    with pytest.raises(ValueError):
        engine.suggest_move("invalid-fen-string")

def test_time_limit(engine):
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    # Should return a move within 1 second
    move = engine.suggest_move(fen, time_limit=1)
    assert isinstance(move, str)

def test_quit_idempotent(engine):
    # Calling quit multiple times should not raise
    engine.quit()
    engine.quit()
