import chess
from typing import Optional
from agents.stockfish_engine import StockfishEngine


class ChessGame:
    """Manages a full chess game between a human and the Stockfish AI."""

    def __init__(
        self,
        engine_path: str,
        options: Optional[dict] = None,
        ai_color: bool = chess.BLACK,
        time_limit: float = 1.0,
    ):
        self.board = chess.Board()
        self.engine = StockfishEngine(engine_path, options or {})
        self.ai_color = ai_color
        self.time_limit = time_limit

    def human_move(self, move_uci: str) -> bool:
        """Apply a human move in UCI format. Returns True if the move was legal."""
        try:
            move = chess.Move.from_uci(move_uci)
            if move in self.board.legal_moves:
                self.board.push(move)
                return True
            return False
        except ValueError:
            return False

    def ai_move(self) -> str:
        """Get and apply the AI move. Returns the move in UCI format."""
        fen = self.board.fen()
        move_uci = self.engine.suggest_move(fen, self.time_limit)
        move = chess.Move.from_uci(move_uci)
        self.board.push(move)
        return move_uci

    def is_game_over(self) -> bool:
        return self.board.is_game_over()

    def get_result(self) -> str:
        result = self.board.result()
        if result == "1-0":
            return "White wins"
        elif result == "0-1":
            return "Black wins"
        return "Draw"

    def quit(self):
        self.engine.quit()
