"""
Sudoku Validator
Menvalidasi input pemain dan memberikan feedback
"""

from typing import List, Tuple, Dict, Set


class SudokuValidator:
    """Validasi Sudoku puzzle dan input pemain"""
    
    def __init__(self, size: int = 9, box_size: int = 3):
        """
        Initialize validator
        
        Args:
            size: Ukuran grid (9 untuk standard)
            box_size: Ukuran sub-grid (3 untuk standard 9x9)
        """
        self.size = size
        self.box_size = box_size
    
    def is_grid_complete(self, grid: List[List[int]]) -> bool:
        """
        Check apakah grid sudah lengkap (tidak ada cell kosong)
        
        Args:
            grid: Puzzle grid
            
        Returns:
            True jika grid lengkap, False sebaliknya
        """
        for row in grid:
            if 0 in row:
                return False
        return True
    
    def is_grid_valid(self, grid: List[List[int]]) -> bool:
        """
        Check apakah grid yang sudah lengkap adalah valid
        
        Args:
            grid: Completed puzzle grid
            
        Returns:
            True jika valid, False sebaliknya
        """
        if not self.is_grid_complete(grid):
            return False
        
        # Check semua rows
        for row in grid:
            if len(set(row)) != self.size or 0 in row:
                return False
        
        # Check semua columns
        for col in range(self.size):
            column = [grid[row][col] for row in range(self.size)]
            if len(set(column)) != self.size or 0 in column:
                return False
        
        # Check semua boxes
        for box_row in range(0, self.size, self.box_size):
            for box_col in range(0, self.size, self.box_size):
                box = []
                for i in range(box_row, box_row + self.box_size):
                    for j in range(box_col, box_col + self.box_size):
                        box.append(grid[i][j])
                
                if len(set(box)) != self.size or 0 in box:
                    return False
        
        return True
    
    def get_invalid_cells(self, grid: List[List[int]]) -> List[Tuple[int, int]]:
        """
        Identifikasi cell yang invalid (conflict)
        
        Args:
            grid: Current puzzle grid (mungkin belum lengkap)
            
        Returns:
            List of (row, col) yang memiliki conflict
        """
        invalid_cells = []
        
        for row in range(self.size):
            for col in range(self.size):
                if grid[row][col] != 0:
                    num = grid[row][col]
                    
                    # Check row
                    row_counts = [grid[row].count(num)]
                    if row_counts[0] > 1:
                        invalid_cells.append((row, col))
                        continue
                    
                    # Check column
                    col_counts = sum(1 for i in range(self.size) if grid[i][col] == num)
                    if col_counts > 1:
                        invalid_cells.append((row, col))
                        continue
                    
                    # Check box
                    box_row, box_col = self.box_size * (row // self.box_size), \
                                      self.box_size * (col // self.box_size)
                    box_count = 0
                    for i in range(box_row, box_row + self.box_size):
                        for j in range(box_col, box_col + self.box_size):
                            if grid[i][j] == num:
                                box_count += 1
                    
                    if box_count > 1:
                        invalid_cells.append((row, col))
        
        return list(set(invalid_cells))  # Remove duplicates
    
    def get_valid_numbers(self, grid: List[List[int]], 
                         row: int, col: int) -> Set[int]:
        """
        Dapatkan list valid numbers untuk cell tertentu
        
        Args:
            grid: Current puzzle grid
            row: Row index
            col: Column index
            
        Returns:
            Set of valid numbers (1-9) untuk cell tersebut
        """
        if grid[row][col] != 0:
            return set()
        
        valid_nums = set(range(1, self.size + 1))
        
        # Remove numbers di row yang sama
        valid_nums -= set(grid[row])
        
        # Remove numbers di column yang sama
        valid_nums -= set(grid[i][col] for i in range(self.size))
        
        # Remove numbers di box yang sama
        box_row = self.box_size * (row // self.box_size)
        box_col = self.box_size * (col // self.box_size)
        
        for i in range(box_row, box_row + self.box_size):
            for j in range(box_col, box_col + self.box_size):
                valid_nums.discard(grid[i][j])
        
        return valid_nums
    
    def get_conflicts_for_cell(self, grid: List[List[int]], 
                              row: int, col: int) -> Dict[str, List[Tuple[int, int]]]:
        """
        Dapatkan detail conflict untuk cell tertentu
        
        Args:
            grid: Current puzzle grid
            row: Row index
            col: Column index
            
        Returns:
            Dictionary dengan conflict locations
        """
        conflicts = {
            "row": [],
            "column": [],
            "box": []
        }
        
        if grid[row][col] == 0:
            return conflicts
        
        num = grid[row][col]
        
        # Check row conflicts
        for j in range(self.size):
            if j != col and grid[row][j] == num:
                conflicts["row"].append((row, j))
        
        # Check column conflicts
        for i in range(self.size):
            if i != row and grid[i][col] == num:
                conflicts["column"].append((i, col))
        
        # Check box conflicts
        box_row = self.box_size * (row // self.box_size)
        box_col = self.box_size * (col // self.box_size)
        
        for i in range(box_row, box_row + self.box_size):
            for j in range(box_col, box_col + self.box_size):
                if (i, j) != (row, col) and grid[i][j] == num:
                    conflicts["box"].append((i, j))
        
        return conflicts
    
    def compare_with_solution(self, current_grid: List[List[int]], 
                             solution: List[List[int]]) -> Dict:
        """
        Bandingkan current grid dengan solution
        
        Args:
            current_grid: Current puzzle grid
            solution: Solution grid
            
        Returns:
            Dictionary dengan comparison results
        """
        result = {
            "is_complete": self.is_grid_complete(current_grid),
            "is_correct": True,
            "wrong_cells": [],
            "empty_cells": 0
        }
        
        for row in range(self.size):
            for col in range(self.size):
                if current_grid[row][col] == 0:
                    result["empty_cells"] += 1
                elif current_grid[row][col] != solution[row][col]:
                    result["is_correct"] = False
                    result["wrong_cells"].append((row, col))
        
        return result
    
    def get_progress(self, puzzle: List[List[int]], 
                    current: List[List[int]]) -> Dict:
        """
        Hitung progress pemain
        
        Args:
            puzzle: Original puzzle (dengan clues)
            current: Current puzzle state
            
        Returns:
            Dictionary dengan progress info
        """
        total_cells = self.size * self.size
        clue_cells = sum(1 for row in puzzle for cell in row if cell != 0)
        filled_cells = sum(1 for row in current for cell in row if cell != 0)
        
        return {
            "total_cells": total_cells,
            "clue_cells": clue_cells,
            "filled_cells": filled_cells,
            "cells_to_fill": total_cells - filled_cells,
            "progress_percentage": round((filled_cells / total_cells) * 100, 1)
        }
