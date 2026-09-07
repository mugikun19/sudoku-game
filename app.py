"""
Sudoku Game Application - Clean React Version
Streamlit-based Sudoku game dengan clean professional grid UI
"""

import streamlit as st
from sudoku_generator import SudokuGenerator
from sudoku_validator import SudokuValidator


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Sudoku Game",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def initialize_session_state():
    """Initialize all session state variables"""
    if "puzzle" not in st.session_state:
        st.session_state.puzzle = None
    if "current_grid" not in st.session_state:
        st.session_state.current_grid = None
    if "solution" not in st.session_state:
        st.session_state.solution = None
    if "original_puzzle" not in st.session_state:
        st.session_state.original_puzzle = None
    if "hints_used" not in st.session_state:
        st.session_state.hints_used = 0
    if "game_started" not in st.session_state:
        st.session_state.game_started = False
    if "game_won" not in st.session_state:
        st.session_state.game_won = False
    if "selected_cell" not in st.session_state:
        st.session_state.selected_cell = None
    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    if "elapsed_time" not in st.session_state:
        st.session_state.elapsed_time = 0
    if "completion_time" not in st.session_state:
        st.session_state.completion_time = None
    if "difficulty_level" not in st.session_state:
        st.session_state.difficulty_level = "medium"


initialize_session_state()

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def generate_new_puzzle(difficulty: str, size: int = 9):
    """Generate a new Sudoku puzzle"""
    import time
    
    generator = SudokuGenerator(size=size, box_size=3)
    puzzle, solution = generator.generate_puzzle(difficulty)
    
    st.session_state.puzzle = puzzle
    st.session_state.solution = solution
    st.session_state.current_grid = [row[:] for row in puzzle]
    st.session_state.original_puzzle = [row[:] for row in puzzle]
    st.session_state.hints_used = 0
    st.session_state.game_started = True
    st.session_state.game_won = False
    st.session_state.selected_cell = None
    st.session_state.start_time = time.time()
    st.session_state.elapsed_time = 0
    st.session_state.completion_time = None
    st.session_state.difficulty_level = difficulty


def reset_puzzle():
    """Reset to original puzzle state"""
    if st.session_state.original_puzzle:
        st.session_state.current_grid = [row[:] for row in st.session_state.original_puzzle]
        st.session_state.hints_used = 0
        st.session_state.game_won = False
        st.session_state.selected_cell = None


def check_solution():
    """Check if current grid matches solution"""
    validator = SudokuValidator()
    result = validator.compare_with_solution(st.session_state.current_grid, st.session_state.solution)
    
    # Track completion time if solved
    if result["is_complete"] and result["is_correct"]:
        if st.session_state.completion_time is None:
            st.session_state.completion_time = get_elapsed_time()
        st.session_state.game_won = True
    
    return result


def format_time(seconds):
    """Format seconds to MM:SS format"""
    minutes = int(seconds) // 60
    secs = int(seconds) % 60
    return f"{minutes:02d}:{secs:02d}"


def get_elapsed_time():
    """Get current elapsed time"""
    import time
    if st.session_state.start_time is None:
        return 0
    return time.time() - st.session_state.start_time


def get_hint():
    """Get a hint for the puzzle"""
    if st.session_state.hints_used >= 5:
        return None, "Maximum hints reached!"
    
    generator = SudokuGenerator()
    hint = generator.get_hint(st.session_state.current_grid, st.session_state.solution)
    
    if hint:
        row, col, value = hint
        st.session_state.current_grid[row][col] = value
        st.session_state.hints_used += 1
        return (row, col, value), "Hint provided!"
    else:
        return None, "No empty cells left!"


def render_completion_screen():
    """Render completion/results screen like sudoku.com"""
    completion_time = st.session_state.completion_time or 0
    difficulty_emoji = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}
    difficulty_text = {"easy": "Easy", "medium": "Medium", "hard": "Hard"}
    
    st.markdown("""
        <style>
        .completion-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.7);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        }
        
        .completion-card {
            background: white;
            border-radius: 12px;
            padding: 40px 30px;
            text-align: center;
            max-width: 500px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        }
        
        .completion-title {
            font-size: 32px;
            font-weight: 700;
            color: #1f77b4;
            margin-bottom: 10px;
        }
        
        .completion-subtitle {
            font-size: 16px;
            color: #666;
            margin-bottom: 30px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 30px 0;
        }
        
        .stat-item {
            padding: 20px;
            background: #f5f5f5;
            border-radius: 8px;
        }
        
        .stat-label {
            font-size: 12px;
            color: #999;
            text-transform: uppercase;
            margin-bottom: 8px;
            font-weight: 600;
        }
        
        .stat-value {
            font-size: 28px;
            font-weight: 700;
            color: #1f77b4;
        }
        
        .completion-buttons {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-top: 30px;
        }
        
        .btn-large {
            padding: 12px 24px;
            font-size: 16px;
            font-weight: 600;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .btn-primary {
            background: #1f77b4;
            color: white;
            flex: 1;
        }
        
        .btn-primary:hover {
            background: #1563a8;
        }
        
        .btn-secondary {
            background: #e0e0e0;
            color: #333;
            flex: 1;
        }
        
        .btn-secondary:hover {
            background: #d0d0d0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
            <div class="completion-card">
                <div class="completion-title">🎉 Puzzle Solved!</div>
                <div class="completion-subtitle">Congratulations!</div>
                
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-label">Time</div>
                        <div class="stat-value">{format_time(completion_time)}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Difficulty</div>
                        <div class="stat-value">{difficulty_emoji.get(st.session_state.difficulty_level, '❓')} {difficulty_text.get(st.session_state.difficulty_level, 'Unknown')}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Hints Used</div>
                        <div class="stat-value">{st.session_state.hints_used}/5</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Mistakes</div>
                        <div class="stat-value">0/3</div>
                    </div>
                </div>
                
                <div class="completion-buttons">
        """, unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔄 New Game", key="new_game_completion", use_container_width=True):
                reset_completion_state()
                st.rerun()
        
        with col_btn2:
            if st.button("📊 Stats", key="stats_btn", use_container_width=True):
                st.info("Stats feature coming soon!")
        
        st.markdown("</div></div>", unsafe_allow_html=True)


def reset_completion_state():
    """Reset state after completion to start new game"""
    st.session_state.game_started = False
    st.session_state.game_won = False
    st.session_state.puzzle = None
    st.session_state.current_grid = None
    st.session_state.solution = None
    st.session_state.original_puzzle = None
    st.session_state.hints_used = 0
    st.session_state.start_time = None
    st.session_state.elapsed_time = 0
    st.session_state.completion_time = None


def render_sudoku_grid():
    """Render interactive Sudoku grid"""
    import json
    
    if st.session_state.current_grid is None:
        return
    
    grid_data = st.session_state.current_grid
    original_puzzle = st.session_state.original_puzzle
    
    # Convert to JSON
    grid_json = json.dumps(grid_data)
    original_json = json.dumps(original_puzzle)
    
    # Build HTML dengan SVG-style borders
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{ margin: 0; padding: 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }}
        
        .sudoku-container {{
            display: flex;
            justify-content: center;
            margin: 20px auto;
        }}
        
        .sudoku-grid {{
            display: inline-grid;
            grid-template-columns: repeat(9, 50px);
            grid-template-rows: repeat(9, 50px);
            gap: 0;
            background-color: #000;
            padding: 2px;
            border: 2px solid #000;
        }}
        
        .sudoku-cell {{
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #ffffff;
            border: 1px solid #999999;
            font-size: 20px;
            font-weight: 600;
            cursor: pointer;
            user-select: none;
            box-sizing: border-box;
        }}
        
        /* 3x3 box borders */
        .sudoku-cell:nth-child(3n) {{
            border-right: 2px solid #000;
        }}
        
        .sudoku-cell:nth-child(9n) {{
            border-right: 1px solid #999;
        }}
        
        .sudoku-cell:nth-child(-n+9) {{
            border-top: 1px solid #999;
        }}
        
        .sudoku-cell:nth-child(n+19):nth-child(-n+27) {{
            border-bottom: 2px solid #000;
        }}
        
        .sudoku-cell:nth-child(n+46):nth-child(-n+54) {{
            border-bottom: 2px solid #000;
        }}
        
        .sudoku-cell:nth-child(n+73) {{
            border-bottom: 1px solid #999;
        }}
        
        .sudoku-cell:hover {{
            background-color: #f5f5f5;
        }}
        
        .sudoku-cell.editable {{
            cursor: pointer;
        }}
        
        .sudoku-cell.locked {{
            font-weight: 700;
            background-color: #ffffff;
            cursor: default;
        }}
        
        .sudoku-cell.selected {{
            background-color: #b3d9ff;
            box-shadow: inset 0 0 0 2px #0066cc;
        }}
        
        .sudoku-cell.highlight {{
            background-color: #e8e8e8;
        }}
        
        .modal {{
            display: none;
            position: fixed;
            z-index: 1;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
        }}
        
        .modal.show {{
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .modal-content {{
            background-color: #ffffff;
            padding: 30px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }}
        
        .modal-content h3 {{
            margin: 0 0 20px 0;
            font-size: 18px;
        }}
        
        .modal-content input {{
            width: 80px;
            height: 50px;
            font-size: 32px;
            text-align: center;
            border: 2px solid #0066cc;
            border-radius: 4px;
            margin: 0 0 20px 0;
            font-weight: 600;
        }}
        
        .modal-buttons {{
            display: flex;
            gap: 10px;
            justify-content: center;
        }}
        
        button {{
            padding: 8px 16px;
            font-size: 14px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 600;
        }}
        
        .btn-ok {{
            background-color: #0066cc;
            color: white;
        }}
        
        .btn-ok:hover {{
            background-color: #0052a3;
        }}
        
        .btn-delete {{
            background-color: #ff4444;
            color: white;
        }}
        
        .btn-delete:hover {{
            background-color: #cc0000;
        }}
        
        .btn-cancel {{
            background-color: #cccccc;
            color: #333;
        }}
        
        .btn-cancel:hover {{
            background-color: #aaaaaa;
        }}
    </style>
    </head>
    <body>
    <div class="sudoku-container">
        <div class="sudoku-grid" id="grid"></div>
    </div>
    
    <div id="modal" class="modal">
        <div class="modal-content">
            <h3>Masukkan Angka</h3>
            <input type="text" id="input" maxlength="1" inputmode="numeric">
            <div class="modal-buttons">
                <button class="btn-ok" onclick="submitInput()">OK</button>
                <button class="btn-delete" onclick="deleteInput()">Delete</button>
                <button class="btn-cancel" onclick="cancelModal()">Cancel</button>
            </div>
        </div>
    </div>
    
    <script>
        let gridData = {grid_json};
        let originalData = {original_json};
        let currentCell = null;
        
        function renderGrid() {{
            const gridContainer = document.getElementById('grid');
            gridContainer.innerHTML = '';
            
            for (let r = 0; r < 9; r++) {{
                for (let c = 0; c < 9; c++) {{
                    const cell = document.createElement('div');
                    cell.className = 'sudoku-cell';
                    cell.id = 'cell-' + r + '-' + c;
                    cell.textContent = gridData[r][c] === 0 ? '' : gridData[r][c];
                    
                    if (originalData[r][c] === 0) {{
                        cell.classList.add('editable');
                        cell.onclick = () => openModal(r, c);
                    }} else {{
                        cell.classList.add('locked');
                    }}
                    
                    gridContainer.appendChild(cell);
                }}
            }}
        }}
        
        function openModal(r, c) {{
            currentCell = {{r, c}};
            const modal = document.getElementById('modal');
            const input = document.getElementById('input');
            
            input.value = gridData[r][c] === 0 ? '' : gridData[r][c];
            modal.classList.add('show');
            input.focus();
            input.select();
        }}
        
        function submitInput() {{
            if (!currentCell) return;
            const input = document.getElementById('input');
            const value = input.value.trim();
            
            if (value === '') {{
                gridData[currentCell.r][currentCell.c] = 0;
            }} else if (/^[1-9]$/.test(value)) {{
                gridData[currentCell.r][currentCell.c] = parseInt(value);
            }} else {{
                alert('Hanya 1-9');
                return;
            }}
            
            closeModal();
            renderGrid();
        }}
        
        function deleteInput() {{
            if (!currentCell) return;
            gridData[currentCell.r][currentCell.c] = 0;
            closeModal();
            renderGrid();
        }}
        
        function cancelModal() {{
            closeModal();
        }}
        
        function closeModal() {{
            const modal = document.getElementById('modal');
            modal.classList.remove('show');
            currentCell = null;
        }}
        
        // Enter key submit
        document.addEventListener('keypress', (e) => {{
            if (e.key === 'Enter' && currentCell) {{
                submitInput();
            }}
        }});
        
        // Initial render
        renderGrid();
    </script>
    </body>
    </html>
    """
    
    # Render using components.html
    st.components.v1.html(html_content, height=600)


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    st.markdown("""
        <h1 style="text-align: center; margin-bottom: 2rem; font-size: 2.5rem;">
            🎮 Sudoku Game
        </h1>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Game Settings")
        
        difficulty = st.selectbox(
            "Select Difficulty",
            options=["easy", "medium", "hard"],
            index=1,
            help="Easy: 50 clues | Medium: 40 clues | Hard: 25 clues"
        )
        
        st.markdown("---")
        
        if st.button("🆕 New Game", use_container_width=True):
            generate_new_puzzle(difficulty, 9)
            st.rerun()
        
        if st.button("🔄 Reset", use_container_width=True, disabled=not st.session_state.game_started):
            reset_puzzle()
            st.rerun()
        
        st.markdown("---")
        
        if st.session_state.game_started:
            st.subheader("📊 Game Info")
            
            # Show timer
            elapsed = get_elapsed_time()
            st.metric("⏱️ Time", format_time(elapsed))
            
            validator = SudokuValidator()
            progress = validator.get_progress(
                st.session_state.original_puzzle,
                st.session_state.current_grid
            )
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Filled", f"{progress['filled_cells']}/{progress['total_cells']}")
            with col2:
                st.metric("Progress", f"{progress['progress_percentage']}%")
            
            st.metric("Hints Used", f"{st.session_state.hints_used}/5")
            
            if st.button("💡 Get Hint", use_container_width=True, disabled=st.session_state.hints_used >= 5):
                hint, message = get_hint()
                if hint:
                    st.success(message)
                    st.rerun()
                else:
                    st.info(message)
    
    # Add auto-refresh for timer updates
    if st.session_state.game_started and not st.session_state.game_won:
        st.markdown("""
            <script>
            setTimeout(function() {
                location.reload();
            }, 1000);
            </script>
        """, unsafe_allow_html=True)
    
    # Main content - flow logic
    if not st.session_state.game_started:
        # Initial state - show instructions
        st.info("👈 Select difficulty and click 'New Game' to start!")
        
        with st.expander("📖 How to Play Sudoku", expanded=True):
            st.markdown("""
            ### Rules
            - Fill each row with numbers 1-9 (no repeats)
            - Fill each column with numbers 1-9 (no repeats)
            - Fill each 3×3 box with numbers 1-9 (no repeats)
            
            ### How to Use
            - **Click** any empty cell to input a number
            - **Type** 1-9, or leave empty to clear
            - **Highlighted cells** show related row, column, and 3×3 box
            
            ### Tips
            - Use hints if stuck (max 5 per game)
            - Check your solution when done
            """)
    
    elif st.session_state.game_won:
        # Completion state - show results screen
        render_completion_screen()
    
    else:
        # Game playing state
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Game Board")
            render_sudoku_grid()
        
        with col2:
            st.subheader("Actions")
            
            if st.button("✅ Check Solution", use_container_width=True):
                result = check_solution()
                
                if result["is_complete"]:
                    if result["is_correct"]:
                        st.session_state.game_won = True
                        st.success("🎉 Congratulations! You solved it!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"❌ {len(result['wrong_cells'])} cell(s) incorrect")
                else:
                    empty = result["empty_cells"]
                    st.warning(f"⏳ {empty} cell(s) still empty")
            
            if st.button("👀 Show Solution", use_container_width=True):
                st.session_state.current_grid = [row[:] for row in st.session_state.solution]
                st.info("Solution revealed!")
                st.rerun()
            
            st.markdown("---")
            
            if st.checkbox("Show validation"):
                validator = SudokuValidator()
                invalid_cells = validator.get_invalid_cells(st.session_state.current_grid)
                
                if invalid_cells:
                    st.warning(f"⚠️ {len(invalid_cells)} conflict(s)")
                    for row, col in invalid_cells[:5]:
                        st.write(f"Row {row+1}, Col {col+1}")
                else:
                    st.success("✅ No conflicts")


if __name__ == "__main__":
    main()
