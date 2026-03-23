## Chess UI for Browser

A new browser-based chess UI is available in the `ui/` directory. This UI allows users to play chess in the browser and receive move suggestions from the Stockfish engine via a backend API.

### How to Run

1. **Install dependencies**
   - Ensure you have Python 3.x installed.
   - Install backend requirements:
     ```
     pip install -r requirements.txt
     ```
2. **Start the backend API**
   - Run the backend server (e.g., Flask or FastAPI):
     ```
     python api.py
     ```
   - By default, the API will listen on `http://localhost:5000` (or as configured).
3. **Open the UI**
   - Open `ui/index.html` in your web browser.
   - The UI will connect to the backend API to request move suggestions.

### Usage
- Make moves on the chessboard in the browser.
- The UI will send the current board state (FEN) to the backend and display Stockfish's suggested move.

### Notes
- Ensure the backend API is running before using the UI.
- For advanced configuration or troubleshooting, see the comments in `api.py` and `agents/stockfish_engine.py`.
