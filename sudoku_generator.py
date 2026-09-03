"""
Sudoku Puzzle Generator and Solver
Menggunakan backtracking algorithm untuk generate dan solve puzzle
"""

import random
import numpy as np
from typing import List, Tuple, Optional


class SudokuGenerator:
    """Generate dan solve Sudoku puzzle dengan berbagai tingkat kesulitan"""
    
    def __init__(self, size: int = 9, box_size: int = 3):
        """
        Initialize Sudoku generator
        
        Args:
            size: Ukuran grid (9 untuk standard)
            box_size: Ukuran sub-grid (3 untuk standard 9x9)
        """
        self.size = size
        self.box_size = box_size
        self.grid = [[0] * size for _ in range(size)]
        self.solution = [[0] * size for _ in range(size)]
    
    def is_valid(self, grid: List[List[int]], row: int, col: int, 
                 num: int) -> bool:
        """
        Check apakah menempatkan num di position (row, col) valid
        
        Args:
            grid: Current puzzle grid
            row: Row index
            col: Column index
            num: Number to place (1-9)
            
        Returns:
            True jika valid, False sebaliknya
        """
        # Check row
        if num in grid[row]:
            return False
        
        # Check column
        if num in [grid[i][col] for i in range(self.size)]:
            return False
        
        # Check box
        box_row, box_col = self.box_size * (row // self.box_size), \
                          self.box_size * (col // self.box_size)
        for i in range(box_row, box_row + self.box_size):
            for j in range(box_col, box_col + self.box_size):
                if grid[i][j] == num:
                    return False
        
        return True
    
    def solve(self, grid: List[List[int]]) -> bool:
        """
        Solve Sudoku puzzle menggunakan backtracking
        
        Args:
            grid: Puzzle grid untuk di-solve
            
        Returns:
            True jika puzzle solvable, False sebaliknya
        """
        for row in range(self.size):
            for col in range(self.size):
                if grid[row][col] == 0:
                    # Coba setiap angka
                    for num in range(1, self.size + 1):
                        if self.is_valid(grid, row, col, num):
                            grid[row][col] = num
                            
                            if self.solve(grid):
                                return True
                            
                            # Backtrack
                            grid[row][col] = 0
                    
                    return False
        
        return True
    
    def generate_complete_grid(self) -> List[List[int]]:
        """
        Generate completed Sudoku grid (valid solution)
        
        Returns:
            Complete 9x9 grid filled dengan valid numbers
        """
        grid = [[0] * self.size for _ in range(self.size)]
        
        # Fill diagonal boxes terlebih dahulu (lebih efisien)
        for i in range(0, self.size, self.box_size):
            self._fill_box(grid, i, i)
        
        # Solve grid
        self.solve(grid)
        
        return grid
    
    def _fill_box(self, grid: List[List[int]], row: int, col: int):
        """Isi 3x3 box dengan random valid numbers"""
        nums = list(range(1, self.size + 1))
        random.shuffle(nums)
        
        idx = 0
        for i in range(row, row + self.box_size):
            for j in range(col, col + self.box_size):
                grid[i][j] = nums[idx]
                idx += 1
    
    def generate_puzzle(self, difficulty: str = "medium") -> Tuple[List[List[int]], List[List[int]]]:
        """
        Generate Sudoku puzzle dengan tingkat kesulitan tertentu
        
        Args:
            difficulty: "easy", "medium", atau "hard"
            
        Returns:
            Tuple (puzzle_grid, solution_grid)
        """
        # Generate complete grid
        self.solution = self.generate_complete_grid()
        puzzle = [row[:] for row in self.solution]
        
        # Tentukan jumlah clues berdasarkan difficulty
        difficulty_levels = {
            "easy": 50,      # Lebih banyak clues
            "medium": 40,    # Medium clues
            "hard": 25       # Lebih sedikit clues
        }
        
        num_clues = difficulty_levels.get(difficulty, 40)
        cells_to_remove = self.size * self.size - num_clues
        
        # Remove cells randomly
        removed = 0
        attempts = 0
        max_attempts = 1000
        
        while removed < cells_to_remove and attempts < max_attempts:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            
            if puzzle[row][col] != 0:
                puzzle[row][col] = 0
                removed += 1
            
            attempts += 1
        
        self.grid = puzzle
        return puzzle, self.solution
    
    def get_hint(self, puzzle: List[List[int]], 
                 solutions: List[List[int]]) -> Optional[Tuple[int, int, int]]:
        """
        Berikan hint dengan mengisi satu cell yang kosong
        
        Args:
            puzzle: Current puzzle grid
            solutions: Solution grid
            
        Returns:
            Tuple (row, col, value) atau None jika puzzle sudah lengkap
        """
        empty_cells = [(i, j) for i in range(self.size) 
                      for j in range(self.size) if puzzle[i][j] == 0]
        
        if not empty_cells:
            return None
        
        row, col = random.choice(empty_cells)
        value = solutions[row][col]
        
        return row, col, value
    
    def count_solutions(self, grid: List[List[int]]) -> int:
        """
        Hitung jumlah solusi yang mungkin (untuk validate uniqueness)
        Berhenti setelah menemukan lebih dari 1 solusi
        
        Args:
            grid: Puzzle grid
            
        Returns:
            Jumlah solusi (0, 1, atau 2+)
        """
        self.solution_count = 0
        self._count_solutions_helper(grid)
        return min(self.solution_count, 2)  # Hanya perlu tahu 0, 1, atau 2+
    
    def _count_solutions_helper(self, grid: List[List[int]]):
        """Helper untuk count solutions dengan optimasi"""
        if self.solution_count > 1:
            return
        
        for row in range(self.size):
            for col in range(self.size):
                if grid[row][col] == 0:
                    for num in range(1, self.size + 1):
                        if self.is_valid(grid, row, col, num):
                            grid[row][col] = num
                            self._count_solutions_helper(grid)
                            grid[row][col] = 0
                    return
        
        self.solution_count += 1
