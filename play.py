"""Entry point: play chess against the Stockfish AI from the command line."""
import chess
from agents.chess_game import ChessGame
from config import STOCKFISH_PATH, STOCKFISH_DEFAULT_OPTIONS


def main():
    print("Chess — You vs Stockfish AI")
    print("You play as White, AI plays as Black.")
    print("Enter moves in UCI format (e.g. e2e4). Type 'quit' to exit.\n")

    game = ChessGame(STOCKFISH_PATH, STOCKFISH_DEFAULT_OPTIONS)
    try:
        while not game.is_game_over():
            print(game.board)
            print()

            if game.board.turn != game.ai_color:
                while True:
                    raw = input("Your move: ").strip()
                    if raw.lower() == "quit":
                        return
                    if game.human_move(raw):
                        break
                    print("Illegal move — try again.")
            else:
                print("AI is thinking…")
                move = game.ai_move()
                print(f"AI plays: {move}\n")

        print(game.board)
        print(f"\nGame over! Result: {game.get_result()}")
    finally:
        game.quit()


if __name__ == "__main__":
    main()
