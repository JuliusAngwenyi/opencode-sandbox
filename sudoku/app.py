import random
import copy
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num:
            return False
        if board[i][col] == num:
            return False
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False
    return True

def solve(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_full():
    board = [[0]*9 for _ in range(9)]
    solve(board)
    return board

def count_solutions(board, limit=2):
    count = [0]
    def solve_count(b):
        if count[0] >= limit:
            return
        for row in range(9):
            for col in range(9):
                if b[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(b, row, col, num):
                            b[row][col] = num
                            solve_count(b)
                            b[row][col] = 0
                    return
        count[0] += 1
    solve_count(board)
    return count[0]

def remove_cells(full_board, difficulty):
    clues = {"easy": 45, "medium": 35, "hard": 25}
    target = clues.get(difficulty, 35)
    board = copy.deepcopy(full_board)
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    removed = 0
    for r, c in cells:
        if removed >= 81 - target:
            break
        backup = board[r][c]
        board[r][c] = 0
        test = copy.deepcopy(board)
        if count_solutions(test) == 1:
            removed += 1
        else:
            board[r][c] = backup
    return board

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/generate", methods=["POST"])
def generate():
    difficulty = request.json.get("difficulty", "medium")
    full = generate_full()
    puzzle = remove_cells(full, difficulty)
    solution = copy.deepcopy(full)
    return jsonify({"puzzle": puzzle, "solution": solution})

@app.route("/api/validate", methods=["POST"])
def validate():
    board = request.json.get("board")
    solution = request.json.get("solution")
    if board == solution:
        return jsonify({"valid": True, "message": "Congratulations! You solved it!"})
    errors = []
    for r in range(9):
        for c in range(9):
            if board[r][c] != 0 and board[r][c] != solution[r][c]:
                errors.append({"row": r, "col": c})
    return jsonify({"valid": False, "errors": errors, "message": "Not quite right. Check highlighted cells."})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
