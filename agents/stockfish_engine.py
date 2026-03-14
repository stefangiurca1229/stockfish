import subprocess
import threading
import queue
import time
from typing import Optional
import os
import sys

# Ensure agents/ is in sys.path for test discovery if run as script
if __name__ == "__main__" or __package__ is None:
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

class StockfishEngine:
    def __init__(self, path: str, options: Optional[dict] = None):
        self.path = path
        self.options = options or {}
        self.process = subprocess.Popen(
            [self.path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1
        )
        self._stdout_queue = queue.Queue()
        self._stdout_thread = threading.Thread(target=self._enqueue_output, daemon=True)
        self._stdout_thread.start()
        self._init_engine()
        self._quit = False

    def _enqueue_output(self):
        for line in self.process.stdout:
            self._stdout_queue.put(line)

    def _init_engine(self):
        self._send('uci')
        self._wait_for('uciok')
        for name, value in self.options.items():
            self._send(f'setoption name {name} value {value}')
        self._send('isready')
        self._wait_for('readyok')

    def _send(self, command: str):
        if self.process.stdin:
            self.process.stdin.write(command + '\n')
            self.process.stdin.flush()

    def _wait_for(self, text: str, timeout: float = 5.0):
        start = time.time()
        while time.time() - start < timeout:
            try:
                line = self._stdout_queue.get(timeout=timeout)
                if text in line:
                    return
            except queue.Empty:
                break
        raise RuntimeError(f"Timeout waiting for '{text}' from Stockfish.")

    def suggest_move(self, fen: str, time_limit: float = 1.0) -> str:
        if not self._is_valid_fen(fen):
            raise ValueError("Invalid FEN string")
        self._send(f'position fen {fen}')
        self._send(f'go movetime {int(time_limit * 1000)}')
        start = time.time()
        bestmove = None
        while time.time() - start < time_limit + 1.0:
            try:
                line = self._stdout_queue.get(timeout=0.1)
                if line.startswith('bestmove'):
                    bestmove = line.split()[1]
                    break
            except queue.Empty:
                continue
        if not bestmove:
            raise RuntimeError("No move returned by Stockfish in time limit.")
        return bestmove

    def quit(self):
        if self._quit:
            return
        self._send('quit')
        self.process.stdin.close()
        self.process.stdout.close()
        self.process.stderr.close()
        self.process.wait(timeout=2)
        self._quit = True

    @staticmethod
    def _is_valid_fen(fen: str) -> bool:
        try:
            import chess
            chess.Board(fen)
            return True
        except Exception:
            return False
