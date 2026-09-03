"""
Sudoku Game Application
Streamlit-based Sudoku game dengan multiple difficulty levels
"""

import streamlit as st
import numpy as np
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

# Custom CSS
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
    }
    .stats-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
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


def render_grid_with_inputs():
    """Render Sudoku grid with input fields"""
    if st.session_state.current_grid is None:
        return
    
    size = 9
    
    # Create a grid of 9x9 cells
    grid_container = st.container()
    
    for row in range(size):
        cols = st.columns(9, gap="small")
        
        for col in range(size):
            with cols[col]:
                is_original = st.session_state.original_puzzle[row][col] != 0
                value = st.session_state.current_grid[row][col]
                
                if is_original:
                    # Display original clue as disabled input
                    st.text_input(
                        label="cell",
                        value=str(value),
                        disabled=True,
                        key=f"cell_{row}_{col}",
                        label_visibility="collapsed"
                    )
                else:
                    # Editable input field
                    new_value = st.text_input(
                        label="cell",
                        value=str(value) if value != 0 else "",
                        max_chars=1,
                        key=f"cell_{row}_{col}",
                        label_visibility="collapsed"
                    )
                    
                    if new_value:
                        try:
                            num = int(new_value)
                            if 1 <= num <= 9:
                                st.session_state.current_grid[row][col] = num
                            else:
                                st.error("Enter 1-9")
                        except ValueError:
                            st.error("Invalid")
                    elif new_value == "":
                        st.session_state.current_grid[row][col] = 0


def render_grid_display():
    """Render Sudoku grid as visual display"""
    if st.session_state.current_grid is None:
        return
    
    size = 9
    html_grid = """
    <div style="
        display: grid;
        grid-template-columns: repeat(9, 1fr);
        grid-gap: 1px;
        background-color: #333;
        padding: 5px;
        max-width: 450px;
        margin: auto;
    ">
    """
    
    for row in range(size):
        for col in range(size):
            value = st.session_state.current_grid[row][col]
            is_original = st.session_state.original_puzzle[row][col] != 0
            
            # Highlight original clues
            bg_color = "#e3f2fd" if is_original else "#fff"
            font_weight = "bold" if is_original else "normal"
            
            cell_value = str(value) if value != 0 else ""
            
            html_grid += f"""
            <div style="
                background-color: {bg_color};
                display: flex;
                align-items: center;
                justify-content: center;
                width: 50px;
                height: 50px;
                font-weight: {font_weight};
                font-size: 18px;
                border-right: 2px solid #333 if {col % 3 == 2} else 1px solid #ccc;
                border-bottom: 2px solid #333 if {row % 3 == 2} else 1px solid #ccc;
            ">
                {cell_value}
            </div>
            """
    
    html_grid += "</div>"
    st.markdown(html_grid, unsafe_allow_html=True)


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
            
            ### Tips
            - Numbers in the blue-highlighted cells are given clues
            - Use the hint button if you get stuck (max 5 hints)
            - Check your solution to see if it's correct
            
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
            render_grid_with_inputs()
        
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
