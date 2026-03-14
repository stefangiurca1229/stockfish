// Simple Chess UI with basic move logic (no check/checkmate validation)
const initialBoard = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"]
];

const pieceSymbols = {
    K: "♔", Q: "♕", R: "♖", B: "♗", N: "♘", P: "♙",
    k: "♚", q: "♛", r: "♜", b: "♝", n: "♞", p: "♟"
};

let board = JSON.parse(JSON.stringify(initialBoard));
let selected = null;
let turn = "w"; // 'w' for white, 'b' for black

function renderBoard() {
    const chessboard = document.getElementById("chessboard");
    chessboard.innerHTML = "";
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const square = document.createElement("div");
            square.className = `square ${(row + col) % 2 === 0 ? "light" : "dark"}`;
            square.dataset.row = row;
            square.dataset.col = col;
            if (selected && selected.row === row && selected.col === col) {
                square.classList.add("selected");
            }
            const piece = board[row][col];
            if (piece) {
                square.textContent = pieceSymbols[piece];
            }
            square.addEventListener("click", () => handleSquareClick(row, col));
            chessboard.appendChild(square);
        }
    }
}

function handleSquareClick(row, col) {
    const piece = board[row][col];
    if (selected) {
        if (selected.row === row && selected.col === col) {
            selected = null;
            renderBoard();
            return;
        }
        // Only allow moving correct color
        if (piece && isWhite(piece) === (turn === "w")) {
            selected = { row, col };
            renderBoard();
            return;
        }
        // Try to move
        if (isLegalMove(selected, { row, col })) {
            board[row][col] = board[selected.row][selected.col];
            board[selected.row][selected.col] = "";
            turn = turn === "w" ? "b" : "w";
            selected = null;
            updateStatus();
            renderBoard();
            return;
        } else {
            selected = null;
            renderBoard();
            return;
        }
    } else {
        if (piece && isWhite(piece) === (turn === "w")) {
            selected = { row, col };
            renderBoard();
        }
    }
}

function isWhite(piece) {
    return piece === piece.toUpperCase();
}

function isLegalMove(from, to) {
    // Basic move legality: only allow moving to empty or opponent's square
    const piece = board[from.row][from.col];
    const dest = board[to.row][to.col];
    if (!piece) return false;
    if (dest && isWhite(dest) === isWhite(piece)) return false;
    // No full chess rules, just allow any move to empty or opponent
    return true;
}

function updateStatus() {
    const status = document.getElementById("status");
    status.textContent = turn === "w" ? "White's turn" : "Black's turn";
}

function resetGame() {
    board = JSON.parse(JSON.stringify(initialBoard));
    turn = "w";
    selected = null;
    updateStatus();
    renderBoard();
}

document.getElementById("resetBtn").addEventListener("click", resetGame);

window.onload = () => {
    updateStatus();
    renderBoard();
};
