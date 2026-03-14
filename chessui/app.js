// Simple static chessboard with piece drag and drop
const boardElement = document.getElementById('chessboard');
const initialBoard = [
    ['r','n','b','q','k','b','n','r'],
    ['p','p','p','p','p','p','p','p'],
    [null,null,null,null,null,null,null,null],
    [null,null,null,null,null,null,null,null],
    [null,null,null,null,null,null,null,null],
    [null,null,null,null,null,null,null,null],
    ['P','P','P','P','P','P','P','P'],
    ['R','N','B','Q','K','B','N','R']
];
const pieceUnicode = {
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
};
let board = JSON.parse(JSON.stringify(initialBoard));
let selected = null;

function renderBoard() {
    boardElement.innerHTML = '';
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const square = document.createElement('div');
            square.className = 'square ' + ((row + col) % 2 === 0 ? 'light' : 'dark');
            square.dataset.row = row;
            square.dataset.col = col;
            if (selected && selected.row === row && selected.col === col) {
                square.classList.add('selected');
            }
            const piece = board[row][col];
            if (piece) {
                square.textContent = pieceUnicode[piece];
            }
            square.addEventListener('click', () => onSquareClick(row, col));
            boardElement.appendChild(square);
        }
    }
}

function onSquareClick(row, col) {
    if (selected) {
        // Move piece
        if (selected.row !== row || selected.col !== col) {
            board[row][col] = board[selected.row][selected.col];
            board[selected.row][selected.col] = null;
        }
        selected = null;
    } else if (board[row][col]) {
        selected = { row, col };
    }
    renderBoard();
}

renderBoard();
