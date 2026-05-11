import tkinter as tk


def _on_play_vs_stockfish():
    print("Starting game vs Stockfish")


def _on_play_vs_player():
    print("Starting game vs Player")


def build_home_screen(root: tk.Tk) -> None:
    root.title("Chess")
    root.geometry("400x300")
    root.resizable(False, False)

    tk.Label(root, text="Chess", font=("Helvetica", 32, "bold")).pack(pady=50)

    tk.Button(
        root,
        text="Play vs Stockfish",
        font=("Helvetica", 14),
        width=20,
        command=_on_play_vs_stockfish,
    ).pack(pady=8)

    tk.Button(
        root,
        text="Play vs Player",
        font=("Helvetica", 14),
        width=20,
        command=_on_play_vs_player,
    ).pack(pady=8)


def main() -> None:
    root = tk.Tk()
    build_home_screen(root)
    root.mainloop()


if __name__ == "__main__":
    main()
