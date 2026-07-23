let puzzle = [];
let solution = [];
let userBoard = [];
let selectedCell = null;

const boardEl = document.getElementById('board');
const messageEl = document.getElementById('message');
const difficultyEl = document.getElementById('difficulty');
const generateBtn = document.getElementById('generate');
const validateBtn = document.getElementById('validate');
const hintBtn = document.getElementById('hint');

function createBoard() {
    boardEl.innerHTML = '';
    for (let r = 0; r < 9; r++) {
        for (let c = 0; c < 9; c++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.dataset.row = r;
            cell.dataset.col = c;
            cell.addEventListener('click', () => selectCell(r, c));
            boardEl.appendChild(cell);
        }
    }
}

function renderBoard() {
    const cells = boardEl.children;
    let counts = Array(10).fill(0);
    for (let i = 0; i < 81; i++) {
        const r = Math.floor(i / 9);
        const c = i % 9;
        const val = userBoard[r][c];
        cells[i].textContent = val || '';
        cells[i].className = 'cell';
        if (puzzle[r][c] !== 0) {
            cells[i].classList.add('given');
        } else if (val !== 0) {
            cells[i].classList.add('user-input');
            counts[val]++;
        }
        if (selectedCell) {
            const [sr, sc] = selectedCell;
            if (r === sr || c === sc) cells[i].classList.add('highlighted');
            if (Math.floor(r/3) === Math.floor(sr/3) && Math.floor(c/3) === Math.floor(sc/3))
                cells[i].classList.add('highlighted');
            if (r === sr && c === sc) cells[i].classList.add('selected');
        }
    }
    document.querySelectorAll('.num').forEach(btn => {
        const val = parseInt(btn.dataset.val);
        if (val > 0 && counts[val] >= 9) btn.classList.add('used');
        else btn.classList.remove('used');
    });
}

function selectCell(r, c) {
    selectedCell = [r, c];
    renderBoard();
}

async function newGame() {
    const difficulty = difficultyEl.value;
    messageEl.textContent = 'Generating...';
    messageEl.className = '';
    const res = await fetch('/api/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({difficulty})
    });
    const data = await res.json();
    puzzle = data.puzzle;
    solution = data.solution;
    userBoard = puzzle.map(r => [...r]);
    selectedCell = null;
    messageEl.textContent = '';
    messageEl.className = '';
    renderBoard();
}

async function checkSolution() {
    const res = await fetch('/api/validate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({board: userBoard, solution})
    });
    const data = await res.json();
    messageEl.textContent = data.message;
    if (data.valid) {
        messageEl.className = 'success';
        const cells = boardEl.children;
        for (let i = 0; i < 81; i++) {
            cells[i].classList.add('correct');
        }
    } else {
        messageEl.className = 'error';
        const cells = boardEl.children;
        data.errors.forEach(({row, col}) => {
            cells[row * 9 + col].classList.add('error');
        });
    }
}

function giveHint() {
    if (!selectedCell) {
        messageEl.textContent = 'Select a cell first';
        messageEl.className = 'error';
        return;
    }
    const [r, c] = selectedCell;
    if (puzzle[r][c] !== 0) {
        messageEl.textContent = 'Cannot hint on given cells';
        messageEl.className = 'error';
        return;
    }
    userBoard[r][c] = solution[r][c];
    messageEl.textContent = '';
    messageEl.className = '';
    renderBoard();
}

document.addEventListener('keydown', (e) => {
    if (!selectedCell) return;
    const [r, c] = selectedCell;
    const key = e.key;
    if (key >= '1' && key <= '9') {
        if (puzzle[r][c] === 0) {
            userBoard[r][c] = parseInt(key);
            messageEl.textContent = '';
            messageEl.className = '';
            renderBoard();
        }
    } else if (key === 'Backspace' || key === 'Delete' || key === '0') {
        if (puzzle[r][c] === 0) {
            userBoard[r][c] = 0;
            renderBoard();
        }
    } else if (key === 'ArrowUp' && r > 0) selectCell(r - 1, c);
    else if (key === 'ArrowDown' && r < 8) selectCell(r + 1, c);
    else if (key === 'ArrowLeft' && c > 0) selectCell(r, c - 1);
    else if (key === 'ArrowRight' && c < 8) selectCell(r, c + 1);
});

document.querySelectorAll('.num').forEach(btn => {
    btn.addEventListener('click', () => {
        if (!selectedCell) return;
        const [r, c] = selectedCell;
        if (puzzle[r][c] !== 0) return;
        userBoard[r][c] = parseInt(btn.dataset.val);
        messageEl.textContent = '';
        messageEl.className = '';
        renderBoard();
    });
});

generateBtn.addEventListener('click', newGame);
validateBtn.addEventListener('click', checkSolution);
hintBtn.addEventListener('click', giveHint);

createBoard();
newGame();
