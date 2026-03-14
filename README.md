# Chess UI

This project includes a browser-based Chess UI located in the `ui/` directory. The UI is a static web application that allows users to play chess in their browser.

## Features
- Interactive chessboard rendered in the browser
- Click to select and move pieces (basic move legality only; no check/checkmate validation)
- Visual indication of the current player's turn
- Reset button to restart the game

## Usage
1. Open `ui/index.html` in your web browser.
2. Play chess by clicking on pieces and their destination squares.
3. Use the "Reset Game" button to restart the game at any time.

## File Structure
- `ui/index.html`: Main HTML file for the Chess UI
- `ui/style.css`: CSS styles for the UI
- `ui/chess.js`: JavaScript logic for rendering the board and handling user interactions

## Notes
- The UI is fully client-side and does not require a backend or server.
- No integration with the Python codebase is included.
- No automated tests are provided for the static UI files.
