# 🎮 Sudoku Game - Streamlit Application

Interactive Sudoku game built with Python, featuring puzzle generation, validation, and multiple difficulty levels.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![License](https://img.shields.io/badge/License-MIT-green)

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Game Rules](#game-rules)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

### Core Gameplay
- **9×9 Standard Sudoku** with 3×3 sub-grids
- **Three Difficulty Levels**:
  - 🟢 Easy: 50 starting numbers
  - 🟡 Medium: 40 starting numbers
  - 🔴 Hard: 25 starting numbers

### Interactive Features
- ✅ **Real-time Validation** - Detect conflicts as you play
- 💡 **Hint System** - Up to 5 hints per puzzle
- 🔍 **Solution Checker** - Verify your solution
- 📊 **Progress Tracking** - See your completion percentage
- 🔄 **Reset Option** - Return to the original puzzle

### Technical Features
- 🚀 **Efficient Puzzle Generation** using backtracking algorithm
- 🔐 **Unique Solutions** guaranteed for each puzzle
- 📱 **Responsive UI** built with Streamlit
- 🎨 **Clean, Modern Interface**
- 💾 **Session State Management** for seamless gameplay

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Clone Repository
```bash
git clone https://github.com/yourusername/sudoku-game.git
cd sudoku-game
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Requirements
```
streamlit>=1.28.0
numpy>=1.24.0
```

---

## 💻 Usage

### Run Locally
```bash
streamlit run app.py
```

This will open the app in your default browser at `http://localhost:8501`

### How to Play
1. **Start a Game**: Select difficulty level and click "🆕 New Game"
2. **Fill Cells**: Click on empty cells (shown in white) and enter numbers 1-9
3. **Use Hints**: Click "💡 Get Hint" for help (max 5 per game)
4. **Validate**: Enable "Show validation" to check for conflicts
5. **Submit**: Click "✅ Check Solution" when complete

### Game Controls

| Button | Function |
|--------|----------|
| 🆕 New Game | Start a new puzzle |
| 🔄 Reset | Return to original puzzle |
| 💡 Get Hint | Reveal one cell (max 5) |
| ✅ Check Solution | Verify your answer |
| 👀 Show Solution | Reveal complete solution |

---

## 📁 Project Structure

```
sudoku-game/
├── app.py                    # Main Streamlit application
├── sudoku_generator.py       # Puzzle generator & solver
├── sudoku_validator.py       # Validation logic
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .gitignore               # Git ignore rules
└── assets/                  # (Optional) Images, icons
```

### File Descriptions

#### `app.py`
Main application file containing:
- Streamlit UI components
- Session state management
- Game flow control
- Interactive grid rendering

#### `sudoku_generator.py`
Puzzle generation engine:
- `SudokuGenerator` class with methods:
  - `generate_puzzle()` - Creates puzzle with specified difficulty
  - `solve()` - Solves puzzle using backtracking
  - `is_valid()` - Validates number placement
  - `get_hint()` - Returns hint for current puzzle

#### `sudoku_validator.py`
Validation and checking logic:
- `SudokuValidator` class with methods:
  - `is_grid_valid()` - Checks if grid is valid
  - `get_invalid_cells()` - Identifies conflicts
  - `get_valid_numbers()` - Returns possible numbers for a cell
  - `compare_with_solution()` - Compares current state with solution
  - `get_progress()` - Calculates completion percentage

---

## 🔧 How It Works

### Puzzle Generation Algorithm

1. **Fill Diagonal Boxes**: Start with diagonal 3×3 boxes filled with random valid numbers
2. **Solve with Backtracking**: Complete the grid using backtracking algorithm
3. **Remove Clues**: Randomly remove cells based on difficulty level
4. **Validate**: Ensure puzzle has unique solution

### Difficulty Levels

| Level | Clues | Cells to Fill | Estimated Time |
|-------|-------|---------------|-----------------|
| Easy | 50 | 31 | 10-20 mins |
| Medium | 40 | 41 | 20-40 mins |
| Hard | 25 | 56 | 40-90 mins |

### Validation System

The validator checks three constraints:
1. **Row Constraint**: Each number 1-9 appears once per row
2. **Column Constraint**: Each number 1-9 appears once per column
3. **Box Constraint**: Each number 1-9 appears once per 3×3 box

---

## 🎮 Game Rules

### Objective
Fill the 9×9 grid with numbers 1-9 such that:
- Each row contains all digits 1-9
- Each column contains all digits 1-9
- Each 3×3 box contains all digits 1-9

### Rules
- You can only enter numbers 1-9
- Numbers highlighted in blue are given clues
- You cannot modify the given clues
- Empty cells can be filled or cleared

### Tips
- Start with rows, columns, or boxes that have many given numbers
- Look for cells where only one number is possible
- Use the validation tool to spot conflicts
- Take hints if you're stuck

---

## 📚 API Documentation

### SudokuGenerator Class

```python
from sudoku_generator import SudokuGenerator

# Initialize
gen = SudokuGenerator(size=9, box_size=3)

# Generate puzzle
puzzle, solution = gen.generate_puzzle(difficulty="medium")

# Get hint
hint = gen.get_hint(puzzle, solution)
# Returns: (row, col, value) or None
```

#### Methods

**`generate_puzzle(difficulty: str)`**
- Generates a new puzzle
- `difficulty`: "easy", "medium", or "hard"
- Returns: (puzzle_grid, solution_grid)

**`solve(grid: List[List[int]])`**
- Solves a puzzle using backtracking
- Returns: True if solvable, False otherwise

**`is_valid(grid, row, col, num)`**
- Checks if placing num at (row, col) is valid
- Returns: True if valid, False otherwise

**`get_hint(puzzle, solution)`**
- Returns hint for puzzle
- Returns: (row, col, value) or None

---

### SudokuValidator Class

```python
from sudoku_validator import SudokuValidator

# Initialize
validator = SudokuValidator(size=9, box_size=3)

# Check if grid is valid
is_valid = validator.is_grid_valid(grid)

# Get invalid cells
conflicts = validator.get_invalid_cells(grid)

# Get valid numbers for cell
valid_nums = validator.get_valid_numbers(grid, row, col)

# Compare with solution
result = validator.compare_with_solution(current_grid, solution_grid)

# Get progress
progress = validator.get_progress(puzzle, current_grid)
```

#### Methods

**`is_grid_valid(grid: List[List[int]])`**
- Returns: True if grid is valid and complete

**`get_invalid_cells(grid)`**
- Returns: List of (row, col) with conflicts

**`get_valid_numbers(grid, row, col)`**
- Returns: Set of valid numbers for cell

**`compare_with_solution(current, solution)`**
- Returns: Dictionary with comparison results

**`get_progress(puzzle, current)`**
- Returns: Dictionary with progress metrics

---

## 🌐 Deployment

### Streamlit Cloud

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Click "New app"
   - Select your repository
   - Set main file to `app.py`
   - Click "Deploy"

### Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

Build and run:
```bash
docker build -t sudoku-game .
docker run -p 8501:8501 sudoku-game
```

### Heroku

1. Create `Procfile`:
   ```
   web: streamlit run --server.port=$PORT --server.address=0.0.0.0 app.py
   ```

2. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/AmazingFeature`
3. Commit changes: `git commit -m 'Add AmazingFeature'`
4. Push to branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

### Code Style
- Follow PEP 8 guidelines
- Add docstrings to functions
- Include type hints where possible
- Write clear commit messages

### Ideas for Enhancement
- [ ] Add leaderboard with scoring system
- [ ] Implement different Sudoku variants (irregular, samurai, etc.)
- [ ] Add multiplayer mode
- [ ] Create mobile app
- [ ] Add statistics and game history
- [ ] Implement auto-solver with step-by-step explanation
- [ ] Add keyboard shortcuts
- [ ] Support different languages

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

Created as an educational project to demonstrate:
- Python programming best practices
- Algorithm implementation (backtracking)
- Streamlit web application development
- Game state management
- Input validation and error handling

---

## 🙏 Acknowledgments

- Sudoku puzzle generation algorithm inspired by constraint satisfaction problems
- UI design inspired by popular Sudoku applications
- Special thanks to the Streamlit community

---

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check existing documentation
- Review code comments and docstrings

---

## 🔄 Changelog

### Version 1.0.0 (Initial Release)
- Core Sudoku game with 9×9 grid
- Three difficulty levels (easy, medium, hard)
- Hint system (up to 5 per game)
- Real-time validation
- Progress tracking
- Solution checker

---

**Happy Sudoku Solving! 🎮**
