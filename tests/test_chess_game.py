import pytest
import chess
from unittest.mock import MagicMock, patch
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.chess_game import ChessGame


@pytest.fixture
def game():
    with patch("agents.chess_game.StockfishEngine") as MockEngine:
        instance = MockEngine.return_value
        g = ChessGame.__new__(ChessGame)
        g.board = chess.Board()
        g.engine = instance
        g.ai_color = chess.BLACK
        g.time_limit = 1.0
        yield g


def test_human_move_legal(game):
    assert game.human_move("e2e4") is True
    assert game.board.peek() == chess.Move.from_uci("e2e4")


def test_human_move_illegal(game):
    assert game.human_move("e2e5") is False
    assert game.board.move_stack == []


def test_human_move_invalid_format(game):
    assert game.human_move("not-a-move") is False


def test_ai_move(game):
    game.engine.suggest_move.return_value = "e7e5"
    # Put it in a state where Black is to move
    game.board.push(chess.Move.from_uci("e2e4"))
    move = game.ai_move()
    assert move == "e7e5"
    assert game.board.peek() == chess.Move.from_uci("e7e5")


def test_is_game_over_initial(game):
    assert game.is_game_over() is False


def test_get_result_white_wins(game):
    # Fool's mate — quickest checkmate
    for uci in ["f2f3", "e7e5", "g2g4", "d8h4"]:
        game.board.push(chess.Move.from_uci(uci))
    assert game.is_game_over() is True
    assert game.get_result() == "Black wins"


def test_quit_delegates_to_engine(game):
    game.quit()
    game.engine.quit.assert_called_once()
