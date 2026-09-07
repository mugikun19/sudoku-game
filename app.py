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
    st.session_state.selected_cell = None


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


def render_sudoku_grid():
    """Render interactive Sudoku grid using React"""
    import json
    
    if st.session_state.current_grid is None:
        return
    
    grid_data = st.session_state.current_grid
    original_puzzle = st.session_state.original_puzzle
    
    # Convert ke JSON dengan aman
    grid_json = json.dumps(grid_data)
    original_json = json.dumps(original_puzzle)
    
    # React component untuk grid interaktif
    grid_html = f'''
    <style>
    .sudoku-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 2rem auto;
    }}
    
    .sudoku-grid {{
        display: inline-grid;
        grid-template-columns: repeat(9, 56px);
        grid-template-rows: repeat(9, 56px);
        gap: 0;
        background-color: #000;
        padding: 3px;
        border: 3px solid #000;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }}
    
    .sudoku-cell {{
        width: 56px;
        height: 56px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #fff;
        border: 1px solid #666;
        font-size: 24px;
        font-weight: 600;
        cursor: pointer;
        user-select: none;
        transition: all 0.1s ease;
        color: #000;
        padding: 0;
        margin: 0;
    }}
    
    /* Thick borders untuk 3x3 boxes */
    .sudoku-cell:nth-child(3n) {{
        border-right: 3px solid #000;
    }}
    
    .sudoku-cell:nth-child(9n) {{
        border-right: 1px solid #666;
    }}
    
    /* Borders bawah untuk rows 9, 18, 27 */
    .sudoku-cell:nth-child(n+1):nth-child(-n+9) {{
        border-bottom: 1px solid #666;
    }}
    
    .sudoku-cell:nth-child(n+19):nth-child(-n+27) {{
        border-bottom: 3px solid #000;
    }}
    
    .sudoku-cell:nth-child(n+28):nth-child(-n+36) {{
        border-bottom: 1px solid #666;
    }}
    
    .sudoku-cell:nth-child(n+46):nth-child(-n+54) {{
        border-bottom: 3px solid #000;
    }}
    
    .sudoku-cell:nth-child(n+55):nth-child(-n+63) {{
        border-bottom: 1px solid #666;
    }}
    
    .sudoku-cell:nth-child(n+73):nth-child(-n+81) {{
        border-bottom: 3px solid #000;
    }}
    
    .sudoku-cell:hover:not(.locked) {{
        background-color: #e8f4f8;
    }}
    
    .sudoku-cell.selected {{
        background-color: #cce5ff;
        box-shadow: inset 0 0 0 2px #1f77b4;
    }}
    
    .sudoku-cell.highlighted {{
        background-color: #f0f0f0;
    }}
    
    .sudoku-cell.locked {{
        font-weight: 700;
        color: #000;
        cursor: default;
    }}
    
    .cell-input-modal {{
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: white;
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        z-index: 1000;
        min-width: 320px;
        text-align: center;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }}
    
    .cell-input-modal h3 {{
        margin: 0 0 1.5rem 0;
        font-size: 18px;
        color: #333;
    }}
    
    .cell-input-modal input {{
        width: 80px;
        height: 60px;
        font-size: 36px;
        text-align: center;
        border: 2px solid #1f77b4;
        border-radius: 5px;
        margin-bottom: 1.5rem;
        font-weight: 600;
    }}
    
    .cell-input-modal input:focus {{
        outline: none;
        border-color: #0d47a1;
        box-shadow: 0 0 0 3px rgba(31, 119, 180, 0.1);
    }}
    
    .modal-buttons {{
        display: flex;
        gap: 10px;
        justify-content: center;
    }}
    
    .modal-buttons button {{
        padding: 0.75rem 1.5rem;
        font-size: 14px;
        font-weight: 600;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.2s ease;
    }}
    
    .btn-submit {{
        background: #1f77b4;
        color: white;
    }}
    
    .btn-submit:hover {{
        background: #1563a8;
    }}
    
    .btn-clear {{
        background: #ff6b6b;
        color: white;
    }}
    
    .btn-clear:hover {{
        background: #ee5a52;
    }}
    
    .btn-cancel {{
        background: #e0e0e0;
        color: #333;
    }}
    
    .btn-cancel:hover {{
        background: #d0d0d0;
    }}
    
    .overlay {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        z-index: 999;
        display: none;
    }}
    
    .overlay.active {{
        display: block;
    }}
    </style>
    
    <div class="sudoku-container">
        <div class="sudoku-grid" id="sudokuGrid"></div>
    </div>
    
    <div class="overlay" id="overlay"></div>
    <div class="cell-input-modal" id="inputModal" style="display: none;">
        <h3>Masukkan Angka (1-9)</h3>
        <input type="text" id="cellInput" maxlength="1" inputmode="numeric" autofocus>
        <div class="modal-buttons">
            <button class="btn-submit" onclick="submitCell()">Submit</button>
            <button class="btn-clear" onclick="clearCell()">Clear</button>
            <button class="btn-cancel" onclick="cancelModal()">Cancel</button>
        </div>
    </div>
    
    <script>
    let currentCell = null;
    let gridData = {grid_json};
    let originalData = {original_json};
    
    function initializeGrid() {{
        const grid = document.getElementById('sudokuGrid');
        grid.innerHTML = '';
        
        for (let row = 0; row < 9; row++) {{
            for (let col = 0; col < 9; col++) {{
                const cell = document.createElement('div');
                const value = gridData[row][col];
                const isLocked = originalData[row][col] !== 0;
                
                cell.className = `sudoku-cell ${{isLocked ? 'locked' : ''}}`;
                cell.textContent = value !== 0 ? value : '';
                cell.id = `cell-${{row}}-${{col}}`;
                
                if (!isLocked) {{
                    cell.onclick = () => selectCell(row, col);
                }}
                
                grid.appendChild(cell);
            }}
        }}
    }}
    
    function selectCell(row, col) {{
        // Clear previous selection
        document.querySelectorAll('.sudoku-cell').forEach(c => {{
            c.classList.remove('selected', 'highlighted');
        }});
        
        // Highlight current cell
        const currentCellElem = document.getElementById(`cell-${{row}}-${{col}}`);
        currentCellElem.classList.add('selected');
        
        // Highlight related cells
        for (let i = 0; i < 9; i++) {{
            // Row
            document.getElementById(`cell-${{row}}-${{i}}`).classList.add('highlighted');
            // Column
            document.getElementById(`cell-${{i}}-${{col}}`).classList.add('highlighted');
        }}
        
        // Highlight 3x3 box
        const boxRow = Math.floor(row / 3) * 3;
        const boxCol = Math.floor(col / 3) * 3;
        for (let i = boxRow; i < boxRow + 3; i++) {{
            for (let j = boxCol; j < boxCol + 3; j++) {{
                document.getElementById(`cell-${{i}}-${{j}}`).classList.add('highlighted');
            }}
        }}
        
        currentCellElem.classList.remove('highlighted');
        
        // Show input modal
        currentCell = {{row, col}};
        showInputModal(row, col);
    }}
    
    function showInputModal(row, col) {{
        const modal = document.getElementById('inputModal');
        const overlay = document.getElementById('overlay');
        const input = document.getElementById('cellInput');
        
        const currentValue = gridData[row][col];
        input.value = currentValue !== 0 ? currentValue : '';
        
        modal.style.display = 'block';
        overlay.classList.add('active');
        input.focus();
        
        // Allow Enter key
        input.onkeypress = (e) => {{
            if (e.key === 'Enter') submitCell();
        }};
    }}
    
    function submitCell() {{
        if (!currentCell) return;
        
        const input = document.getElementById('cellInput');
        const value = input.value.trim();
        
        if (value === '') {{
            gridData[currentCell.row][currentCell.col] = 0;
        }} else if (/^[1-9]$/.test(value)) {{
            gridData[currentCell.row][currentCell.col] = parseInt(value);
        }} else {{
            alert('Hanya masukkan angka 1-9');
            return;
        }}
        
        updateGridDisplay();
        updateStreamlit();
        closeModal();
    }}
    
    function clearCell() {{
        if (!currentCell) return;
        gridData[currentCell.row][currentCell.col] = 0;
        updateGridDisplay();
        updateStreamlit();
        closeModal();
    }}
    
    function cancelModal() {{
        closeModal();
    }}
    
    function closeModal() {{
        const modal = document.getElementById('inputModal');
        const overlay = document.getElementById('overlay');
        modal.style.display = 'none';
        overlay.classList.remove('active');
        currentCell = null;
        
        // Clear selection
        document.querySelectorAll('.sudoku-cell').forEach(c => {{
            c.classList.remove('selected', 'highlighted');
        }});
    }}
    
    function updateGridDisplay() {{
        for (let row = 0; row < 9; row++) {{
            for (let col = 0; col < 9; col++) {{
                const cell = document.getElementById(`cell-${{row}}-${{col}}`);
                const value = gridData[row][col];
                cell.textContent = value !== 0 ? value : '';
            }}
        }}
    }}
    
    function updateStreamlit() {{
        // Send data to Streamlit via hidden input
        const hiddenInput = document.getElementById('hiddenGridData');
        if (hiddenInput) {{
            hiddenInput.value = JSON.stringify(gridData);
            hiddenInput.dispatchEvent(new Event('change'));
        }}
    }}
    
    // Initialize on page load
    initializeGrid();
    </script>
    '''
    
    st.markdown(grid_html, unsafe_allow_html=True)
    
    # Hidden input untuk capture grid updates
    st.markdown('<input type="hidden" id="hiddenGridData" />', unsafe_allow_html=True)


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
    
    # Main content
    if not st.session_state.game_started:
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
    else:
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
