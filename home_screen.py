import tkinter as tk

class HomeScreen:
    def __init__(self, root):
        self.root = root
        root.title("Stockfish Chess")
        self.button_stockfish = tk.Button(root, text="Play vs Stockfish", command=self.play_vs_stockfish)
        self.button_player = tk.Button(root, text="Play vs Player", command=self.play_vs_player)
        self.button_stockfish.pack(pady=10)
        self.button_player.pack(pady=10)

    def play_vs_stockfish(self):
        pass

    def play_vs_player(self):
        pass
