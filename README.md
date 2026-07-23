# OpenCode Sandbox

A collection of small Python projects including a CLI calculator, a Snake game, and a Sudoku browser game.

## Projects

### CLI Calculator (`calc.py`)
A minimal command-line calculator that evaluates arithmetic expressions.

```bash
python3 calc.py 2 + 3
python3 calc.py "(2 + 3) * 4"
```

### Snake Game (`snake.py`)
A classic Snake game built with pygame.

**Controls:** Arrow keys to move, R to restart after game over.

```bash
pip install pygame
python3 snake.py
```

### Sudoku Browser Game (`sudoku/`)
A full-stack Sudoku game with Python/Flask backend and HTML/CSS/JS frontend. Features a custom Sudoku generator, solver, and validator with no external Sudoku packages.

**Features:**
- Generate new puzzles with Easy/Medium/Hard difficulty
- Click cells or use arrow keys to navigate
- Number pad or keyboard (1-9) to fill cells
- Check button validates your solution
- Hint button reveals correct values
- Highlights related rows, columns, and boxes

```bash
pip install flask
cd sudoku
python3 app.py
```
Then open http://127.0.0.1:5000 in your browser.

## Getting Started

### Prerequisites
- Python 3.6+
- pip (for dependencies)

### Installation
1. Clone the repository:
```bash
git clone https://github.com/JuliusAngwenyi/opencode-sandbox.git
cd opencode-sandbox
```

2. Install dependencies:
```bash
pip install pygame flask
```

### Running
**Calculator:**
```bash
python3 calc.py <expression>
```

**Snake Game:**
```bash
python3 snake.py
```

**Sudoku Game:**
```bash
cd sudoku
python3 app.py
```
Then open http://127.0.0.1:5000 in your browser.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
