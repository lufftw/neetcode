# solutions/0052_n_queens_ii.py
"""
Problem: N-Queens II
Link: https://leetcode.com/problems/n-queens-ii/

Return the number of distinct solutions to the n-queens puzzle.

Sub-Pattern: Constraint satisfaction counting (optimized N-Queens)
Key Insight: Same algorithm as N-Queens, but only count solutions
instead of building board representations. Uses hash sets for O(1)
constraint checking.

Delta from N-Queens (LeetCode 51):
- Only count solutions, don't build board strings
- More memory efficient (no need to store board state)
"""
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionSets",
        "method": "totalNQueens",
        "complexity": "O(n!) time, O(n) space",
        "description": "Backtracking with hash sets for constraint tracking",
    },
    "bitmask": {
        "class": "SolutionBitmask",
        "method": "totalNQueens",
        "complexity": "O(n!) time, O(n) space",
        "description": "Backtracking with bitmasks for ultra-fast constraint checking",
    },
}


class SolutionSets:
    def totalNQueens(self, n: int) -> int:
        """
        Count all solutions to the N-Queens puzzle using hash sets.
        
        Algorithm:
        - Place queens row by row (one queen per row guaranteed)
        - Track three constraints with hash sets:
          1. Columns: No two queens in same column
          2. Main diagonals (↘): Cells where row - col is constant
          3. Anti-diagonals (↙): Cells where row + col is constant
        
        Why Row-by-Row Works:
        - Each row must have exactly one queen
        - By placing row by row, row conflicts are impossible by construction
        - Only need to check column and diagonal conflicts
        
        Constraint Identification:
        - Column: Just the column index
        - Main diagonal: row - col (constant for cells on same ↘ diagonal)
        - Anti-diagonal: row + col (constant for cells on same ↙ diagonal)
        
        Time Complexity: O(n!)
            - At row 0: n choices
            - At row 1: at most n-1 valid choices
            - ... and so on (pruning reduces this further)
        
        Space Complexity: O(n) for constraint sets and recursion
        """
        count = 0
        
        # Constraint sets for O(1) conflict checking
        used_cols: set[int] = set()
        used_diag_main: set[int] = set()   # row - col
        used_diag_anti: set[int] = set()   # row + col
        
        def backtrack(row: int) -> None:
            nonlocal count
            
            # BASE CASE: All queens placed successfully
            if row == n:
                count += 1
                return
            
            # Try each column in the current row
            for col in range(n):
                # Calculate diagonal identifiers for this cell
                diag_main = row - col
                diag_anti = row + col
                
                # === CONSTRAINT CHECK (Pruning) ===
                # Skip if this column or either diagonal is already attacked
                if col in used_cols:
                    continue
                if diag_main in used_diag_main:
                    continue
                if diag_anti in used_diag_anti:
                    continue
                
                # === CHOOSE: Place queen ===
                used_cols.add(col)
                used_diag_main.add(diag_main)
                used_diag_anti.add(diag_anti)
                
                # === EXPLORE: Move to next row ===
                backtrack(row + 1)
                
                # === UNCHOOSE: Remove queen ===
                used_cols.discard(col)
                used_diag_main.discard(diag_main)
                used_diag_anti.discard(diag_anti)
        
        backtrack(0)
        return count


class SolutionBitmask:
    def totalNQueens(self, n: int) -> int:
        """
        Count N-Queens solutions using bitmasks for constraint tracking.
        
        Optimization over hash sets:
        - Use integers as bitmasks (each bit = one column/diagonal)
        - Bitwise operations are faster than hash lookups
        - Better cache locality
        
        Bitmask Operations:
        - Check if column c is free: (cols & (1 << c)) == 0
        - Mark column c: cols |= (1 << c)
        - Unmark column c: cols &= ~(1 << c)
        
        Diagonal Shifting:
        - Main diagonal (↘): Shift LEFT when moving down (diag1 << 1)
        - Anti-diagonal (↙): Shift RIGHT when moving down (diag2 >> 1)
        
        Time Complexity: O(n!) with smaller constants
        Space Complexity: O(n) for recursion (O(1) for bitmasks)
        """
        count = 0
        
        def backtrack(row: int, cols: int, diag1: int, diag2: int) -> None:
            nonlocal count
            
            if row == n:
                count += 1
                return
            
            for col in range(n):
                col_bit = 1 << col
                
                # Check all three constraints using bitwise AND
                if cols & col_bit:
                    continue
                if diag1 & col_bit:
                    continue
                if diag2 & col_bit:
                    continue
                
                # Recurse with updated bitmasks
                # Shift diagonals for the next row
                backtrack(
                    row + 1,
                    cols | col_bit,
                    (diag1 | col_bit) << 1,  # Main diagonal shifts left
                    (diag2 | col_bit) >> 1   # Anti-diagonal shifts right
                )
        
        backtrack(0, 0, 0, 0)
        return count


def solve():
    """
    Input format:
    Line 1: n (board size)
    
    Example:
    4
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')
    
    n = int(lines[0])
    
    solver = get_solver(SOLUTIONS)
    result = solver.totalNQueens(n)
    
    print(result)


if __name__ == "__main__":
    solve()

