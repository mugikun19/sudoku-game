"""
Sudoku Game Application - Interactive Version
Streamlit-based Sudoku game dengan clean grid UI seperti Sudoku konvensional
"""

import streamlit as st
from sudoku_generator import SudokuGenerator
from sudoku_validator import SudokuValidator


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Sudoku Solver",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk layout dan styling yang clean
st.markdown("""
    <style>
    .main { padding: 2rem; }
    .stButton>button {
        width: 100%;
        padding: 0.5rem;
        font-size: 1rem;
    }
    .game-title {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    
    /* Sudoku Grid Styling - CLEAN PROFESSIONAL VERSION */
    .sudoku-grid-wrapper {
        display: flex;
        justify-content: center;
        margin: 2rem 0;
    }
    
    .sudoku-grid {
        display: inline-grid;
        grid-template-columns: repeat(9, 50px);
        grid-template-rows: repeat(9, 50px);
        gap: 0;
        background-color: #000;
        padding: 3px;
        border: 3px solid #000;
        box-shadow: 0 0 10px rgba(0,0,0,0.2);
    }
    
    .sudoku-cell {
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #fff;
        border: 1px solid #999;
        font-size: 22px;
        font-weight: 600;
        cursor: pointer;
        user-select: none;
        transition: background-color 0.15s ease;
        padding: 0;
        margin: 0;
    }
    
    .sudoku-cell:hover {
        background-color: #f5f5f5;
    }
    
    .sudoku-cell.selected {
        background-color: #cce5ff;
        box-shadow: inset 0 0 0 2px #1f77b4;
    }
    
    .sudoku-cell.highlighted {
        background-color: #e8f4f8;
    }
    
    /* Thick borders untuk 3x3 boxes */
    .sudoku-cell:nth-child(3n) {
        border-right: 3px solid #000;
    }
    
    .sudoku-cell:nth-child(9n) {
        border-right: 1px solid #999;
    }
    
    /* Rows 9, 18, 27, dst */
    .sudoku-cell:nth-child(n+1):nth-child(-n+9):nth-child(9n+1) { }
    
    .sudoku-row-3 .sudoku-cell,
    .sudoku-row-6 .sudoku-cell {
        border-bottom: 3px solid #000;
    }
    
    .input-overlay {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.5);
        z-index: 999;
        align-items: center;
        justify-content: center;
    }
    
    .input-overlay.active {
        display: flex;
    }
    
    .input-modal {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        text-align: center;
        min-width: 300px;
    }
    
    .input-modal h3 {
        margin: 0 0 1.5rem 0;
        color: #333;
    }
    
    .input-modal input {
        width: 80px;
        height: 50px;
        font-size: 32px;
        text-align: center;
        border: 2px solid #1f77b4;
        border-radius: 5px;
        margin-bottom: 1.5rem;
    }
    
    .input-modal-buttons {
        display: flex;
        gap: 10px;
        justify-content: center;
    }
    
    .input-modal-buttons button {
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .btn-submit {
        background: #1f77b4;
        color: white;
    }
    
    .btn-submit:hover {
        background: #1563a8;
    }
    
    .btn-delete {
        background: #ff6b6b;
        color: white;
    }
    
    .btn-delete:hover {
        background: #ee5a52;
    }
    
    .btn-cancel {
        background: #ccc;
        color: #333;
    }
    
    .btn-cancel:hover {
        background: #bbb;
    }
    
    .cells-container {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

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


initialize_session_state()

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def generate_new_puzzle(difficulty: str, size: int = 9):
    """Generate a new Sudoku puzzle"""
    generator = SudokuGenerator(size=size, box_size=3)
    puzzle, solution = generator.generate_puzzle(difficulty)
    
    st.session_state.puzzle = puzzle
    st.session_state.solution = solution
    st.session_state.current_grid = [row[:] for row in puzzle]
    st.session_state.original_puzzle = [row[:] for row in puzzle]
    st.session_state.hints_used = 0
    st.session_state.game_started = True
    st.session_state.game_won = False


def reset_puzzle():
    """Reset to original puzzle state"""
    if st.session_state.original_puzzle:
        st.session_state.current_grid = [row[:] for row in st.session_state.original_puzzle]
        st.session_state.hints_used = 0
        st.session_state.game_won = False


def check_solution():
    """Check if current grid matches solution"""
    validator = SudokuValidator()
    result = validator.compare_with_solution(st.session_state.current_grid, st.session_state.solution)
    return result


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


def render_interactive_grid():
    """Render interactive Sudoku grid dengan HTML + JavaScript yang smooth"""
    if st.session_state.current_grid is None:
        return
    
    size = 9
    grid_data = st.session_state.current_grid
    original_puzzle = st.session_state.original_puzzle
    
    # Container untuk update input (hidden)
    input_container = st.container()
    
    with input_container:
        st.markdown(f'<div class="cells-container" id="cellsContainer"></div>', 
                   unsafe_allow_html=True)
        
        # Create hidden inputs for all cells
        for row in range(size):
            cols = st.columns(9, gap="small")
            for col in range(size):
                with cols[col]:
                    is_original = original_puzzle[row][col] != 0
                    value = grid_data[row][col]
                    
                    # Input tersembunyi untuk capture perubahan
                    if not is_original:
                        st.text_input(
                            label="cell",
                            value=str(value) if value != 0 else "",
                            max_chars=1,
                            key=f"cell_{row}_{col}",
                            label_visibility="collapsed",
                            disabled=False,
                            type="password"
                        )
    
    # Build grid HTML
    grid_html = '<div class="sudoku-grid-wrapper"><div class="sudoku-grid" id="sudokuGrid">'
    
    for row in range(size):
        for col in range(size):
            value = grid_data[row][col]
            is_original = original_puzzle[row][col] != 0
            cell_class = "sudoku-cell"
            
            cell_value = str(value) if value != 0 else ""
            
            grid_html += f'''
                <div class="{cell_class}" 
                     data-row="{row}" 
                     data-col="{col}" 
                     data-clue="{'true' if is_original else 'false'}"
                     onclick="handleCellClick(this, {row}, {col}, {'true' if is_original else 'false'})"
                     id="cell-{row}-{col}">
                    {cell_value}
                </div>
            '''
    
    grid_html += '</div></div>'
    
    # JavaScript untuk interaksi yang smooth
    grid_html += '''
    <script>
    function handleCellClick(element, row, col, isClue) {
        if (isClue === 'true') return;
        
        // Clear previous selection
        document.querySelectorAll(".sudoku-cell").forEach(cell => {
            cell.classList.remove("selected", "highlighted");
        });
        
        element.classList.add("selected");
        highlightRelated(row, col);
        
        // Get current value
        const currentValue = element.textContent.trim();
        
        // Show input prompt
        const input = prompt("Masukkan angka (1-9) atau delete untuk kosongkan:", currentValue);
        
        if (input !== null) {
            if (input === "" || input.toLowerCase() === "delete" || input === "0") {
                element.textContent = "";
                updateCellInput(row, col, "");
            } else if (/^[1-9]$/.test(input)) {
                element.textContent = input;
                updateCellInput(row, col, input);
            } else {
                alert("Hanya masukkan angka 1-9");
            }
        }
        
        // Clear highlight
        document.querySelectorAll(".sudoku-cell").forEach(cell => {
            cell.classList.remove("selected", "highlighted");
        });
    }
    
    function highlightRelated(row, col) {
        const cells = document.querySelectorAll(".sudoku-cell");
        
        cells.forEach(cell => {
            const cellRow = parseInt(cell.dataset.row);
            const cellCol = parseInt(cell.dataset.col);
            
            // Highlight row, column, dan 3x3 box
            if (cellRow === row || cellCol === col) {
                cell.classList.add("highlighted");
            }
            
            // Highlight 3x3 box
            const boxRow = Math.floor(row / 3);
            const boxCol = Math.floor(col / 3);
            const cellBoxRow = Math.floor(cellRow / 3);
            const cellBoxCol = Math.floor(cellCol / 3);
            
            if (boxRow === cellBoxRow && boxCol === cellBoxCol) {
                cell.classList.add("highlighted");
            }
        });
    }
    
    function updateCellInput(row, col, value) {
        const inputKey = `cell_${row}_${col}`;
        const inputElement = document.querySelector(`input[value="${value}"][data-testid="textinput-${inputKey}"]`);
        if (inputElement) {
            inputElement.value = value;
        }
        // Trigger Streamlit state update
        window.sudokuUpdated = true;
    }
    </script>
    '''
    
    st.markdown(grid_html, unsafe_allow_html=True)


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # Header
    st.markdown("<h1 class='game-title'>🎮 Sudoku Game</h1>", unsafe_allow_html=True)
    
    # Sidebar for controls
    with st.sidebar:
        st.header("⚙️ Game Settings")
        
        # Difficulty selection
        difficulty = st.selectbox(
            "Select Difficulty",
            options=["easy", "medium", "hard"],
            index=1,
            help="Easy: 50 clues | Medium: 40 clues | Hard: 25 clues"
        )
        
        st.markdown("---")
        
        # Game controls
        if st.button("🆕 New Game", use_container_width=True):
            generate_new_puzzle(difficulty, 9)
            st.rerun()
        
        if st.button("🔄 Reset", use_container_width=True, disabled=not st.session_state.game_started):
            reset_puzzle()
            st.rerun()
        
        st.markdown("---")
        
        # Game info
        if st.session_state.game_started:
            st.subheader("📊 Game Info")
            
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
            
            # Hint button
            if st.button("💡 Get Hint", use_container_width=True, disabled=st.session_state.hints_used >= 5):
                hint, message = get_hint()
                if hint:
                    st.success(message)
                    st.rerun()
                else:
                    st.info(message)
    
    # Main content area
    if not st.session_state.game_started:
        st.info("👈 Select difficulty and click 'New Game' to start!")
        
        # Show game instructions
        with st.expander("📖 How to Play Sudoku", expanded=True):
            st.markdown("""
            ### Rules
            - Fill each row with numbers 1-9 (no repeats)
            - Fill each column with numbers 1-9 (no repeats)
            - Fill each 3×3 box with numbers 1-9 (no repeats)
            
            ### How to Use
            - **Click** pada kotak kosong untuk memasukkan angka
            - **Type** angka 1-9, atau kosongkan untuk delete
            - **Blue highlight** menunjukkan row, column, dan box yang terkait
            
            ### Tips
            - Use the hint button jika stuck (max 5 hints)
            - Check your solution untuk verify
            
            ### Difficulty Levels
            - **Easy**: 50 starting numbers
            - **Medium**: 40 starting numbers
            - **Hard**: 25 starting numbers
            """)
    
    else:
        # Game board
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Game Board")
            render_interactive_grid()
        
        with col2:
            st.subheader("Actions")
            
            # Check solution button
            if st.button("✅ Check Solution", use_container_width=True):
                result = check_solution()
                
                if result["is_complete"]:
                    if result["is_correct"]:
                        st.session_state.game_won = True
                        st.success("🎉 Congratulations! You solved it!")
                        st.balloons()
                    else:
                        st.error(f"❌ {len(result['wrong_cells'])} cell(s) are incorrect")
                else:
                    empty = result["empty_cells"]
                    st.warning(f"⏳ {empty} cell(s) still empty")
            
            # Show solution button
            if st.button("👀 Show Solution", use_container_width=True):
                st.session_state.current_grid = [row[:] for row in st.session_state.solution]
                st.info("Solution revealed!")
                st.rerun()
            
            st.markdown("---")
            
            # Validation info
            if st.checkbox("Show validation"):
                validator = SudokuValidator()
                invalid_cells = validator.get_invalid_cells(st.session_state.current_grid)
                
                if invalid_cells:
                    st.warning(f"⚠️ {len(invalid_cells)} conflict(s) detected")
                    for row, col in invalid_cells[:5]:  # Show first 5
                        st.write(f"Cell Row {row+1}, Col {col+1}")
                else:
                    st.success("✅ No conflicts detected")


if __name__ == "__main__":
    main()
