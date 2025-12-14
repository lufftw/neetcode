# solutions/0051_n_queens.py
"""
================================================================================
LeetCode 51: N-Queens
================================================================================

Problem: The n-queens puzzle is the problem of placing n queens on an n x n
         chessboard such that no two queens attack each other.
         Given an integer n, return all distinct solutions to the n-queens puzzle.

API Kernel: Backtracking
Pattern: constraint_satisfaction_backtrack
Family: backtracking

--------------------------------------------------------------------------------
BACKTRACKING PATTERN: CONSTRAINT SATISFACTION
--------------------------------------------------------------------------------

The N-Queens problem is a classic constraint satisfaction problem (CSP).
We use backtracking to systematically explore all possible queen placements
while pruning invalid branches early.

KEY INSIGHT:
- Place queens row by row (one queen per row is guaranteed)
- For each row, try each column and check three constraints:
  1. Column constraint: no two queens in same column
  2. Main diagonal (\): characterized by (row - col) = constant
  3. Anti-diagonal (/): characterized by (row + col) = constant

--------------------------------------------------------------------------------
COMPLEXITY ANALYSIS
--------------------------------------------------------------------------------

Time:  O(N!) - At row 0, we have N choices; at row 1, at most N-1 choices, etc.
Space: O(N) - board array, three constraint sets, and recursion stack

================================================================================
"""
from typing import List, Set
from _runner import get_solver


# ============================================================================
# JUDGE_FUNC - Custom validation for "return in any order" problems
# Uses Decision Problem approach: verify solution validity, not exact match
# ============================================================================
def _is_valid_board(board: List[str], n: int) -> bool:
    """Check if a single board configuration is valid (no queens attacking each other)."""
    if len(board) != n:
        return False
    
    queens = []
    for r, row in enumerate(board):
        if len(row) != n or row.count('Q') != 1:
            return False
        c = row.index('Q')
        queens.append((r, c))
    
    # Check column and diagonal conflicts
    for i, (r1, c1) in enumerate(queens):
        for r2, c2 in queens[i+1:]:
            if c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
                return False
    return True


def judge(actual: List[List[str]], expected, input_data: str) -> bool:
    """
    Custom validation function for N-Queens (Decision Problem approach).
    
    Validation logic:
    1. Each solution must be a valid N-Queens configuration
    2. No duplicate solutions allowed
    3. Number of solutions must be correct (check against expected or known counts)
    
    Args:
        actual: Program output (parsed as list)
        expected: Expected output (parsed as list), or None for generated tests
        input_data: Input data (raw string)
    
    Returns:
        bool: Whether the answer is correct
    """
    n = int(input_data.strip())
    
    # Known solution counts for N-Queens (for judge-only validation)
    KNOWN_COUNTS = {1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 6: 4, 7: 40, 8: 92, 9: 352}
    
    # 1. Verify each solution is valid
    for board in actual:
        if not _is_valid_board(board, n):
            return False
    
    # 2. Check no duplicate solutions
    unique_solutions = set(tuple(row for row in board) for board in actual)
    if len(unique_solutions) != len(actual):
        return False
    
    # 3. Check solution count
    if expected is not None:
        # Has .out file: compare against expected
        if len(actual) != len(expected):
            return False
    else:
        # Judge-only mode (generated tests): use known counts
        expected_count = KNOWN_COUNTS.get(n)
        if expected_count is not None and len(actual) != expected_count:
            return False
    
    return True


JUDGE_FUNC = judge  # Tell test_runner to use custom validation function

# ============================================
# Alternative: COMPARE_MODE (simpler, but less rigorous)
# ============================================
# If you don't need full validation, you can use COMPARE_MODE instead:
#
#   COMPARE_MODE = "sorted"  # Sort lists before comparison
#
# This will sort both actual and expected outputs and compare them.
# Pros: Simple, no custom code needed
# Cons: Only checks if outputs match, doesn't validate solution correctness
#
# For N-Queens, JUDGE_FUNC is recommended because it:
# - Validates each board is a legal N-Queens configuration
# - Checks for duplicate solutions
# - Works even without .out file (judge-only mode)
#
# Use COMPARE_MODE when:
# - Order doesn't matter but exact values do (e.g., Permutations, Subsets)
# - You trust the expected output is correct
# ============================================

# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# Polymorphic pattern: each entry specifies class + method
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionBacktrackSets",
        "method": "solveNQueens",
        "complexity": "O(N!) time, O(N) space",
        "description": "Backtracking with hash sets for O(1) conflict detection",
    },
    "sets": {
        "class": "SolutionBacktrackSets",
        "method": "solveNQueens",
        "complexity": "O(N!) time, O(N) space",
        "description": "Backtracking with hash sets for O(1) conflict detection",
    },
    "bitmask": {
        "class": "SolutionBacktrackBitmask",
        "method": "solveNQueens",
        "complexity": "O(N!) time, O(N) space",
        "description": "Backtracking with bitmask for ultra-fast conflict detection",
    },
}


# ============================================
# Solution 1: Backtracking with Hash Sets
# Time: O(N!), Space: O(N)
# ============================================
#
# ALGORITHM OVERVIEW:
# The N-Queens problem is a classic constraint satisfaction problem (CSP).
# We use backtracking to systematically explore all possible queen placements
# while pruning invalid branches early.
#
# KEY INSIGHT:
# - Place queens row by row (one queen per row is guaranteed)
# - For each row, try each column and check three constraints:
#   1. Column constraint: no two queens in same column
#   2. Main diagonal (\): characterized by (row - col) = constant
#   3. Anti-diagonal (/): characterized by (row + col) = constant
#
# TIME COMPLEXITY: O(N!)
# - At row 0, we have N choices
# - At row 1, we have at most N-1 choices (one column blocked)
# - At row 2, we have at most N-2 choices
# - Total: N × (N-1) × (N-2) × ... × 1 = O(N!)
# - Note: The actual number is much smaller due to diagonal constraints
#
# SPACE COMPLEXITY: O(N)
# - board[]: O(N) to store queen positions
# - Three sets: O(N) each in worst case
# - Recursion stack: O(N) depth
# - Output space is not counted (it's the required output)
#
# WHY THIS APPROACH:
# 1. Clean separation of concerns (constraint checking vs. board building)
# 2. O(1) constraint lookup using hash sets
# 3. Proper backtracking with state restoration
# 4. The "choice-explore-unchoice" pattern essential for backtracking
# ============================================
class SolutionBacktrackSets:
    """
    Backtracking solution using hash sets for O(1) conflict detection.
    
    Recommended approach as it balances readability with efficiency.
    """
    
    def solveNQueens(self, n: int) -> List[List[str]]:
        results: List[List[str]] = []
        
        # board[row] = col means queen at (row, col)
        # Using array instead of 2D grid saves space and simplifies board construction
        board: List[int] = [-1] * n
        
        # Constraint tracking sets for O(1) lookup
        # These sets remember which columns and diagonals are "under attack"
        used_cols: Set[int] = set()      # Columns occupied by queens
        used_diag1: Set[int] = set()     # Main diagonals (\): row - col = constant
        used_diag2: Set[int] = set()     # Anti-diagonals (/): row + col = constant
        
        def backtrack(row: int) -> None:
            """
            Place queens starting from the given row.
            
            Base case: row == n means all queens are placed successfully.
            Recursive case: try each column in the current row.
            """
            # BASE CASE: All N queens have been placed successfully
            if row == n:
                results.append(self._build_board(board))
                return
            
            # RECURSIVE CASE: Try each column in the current row
            for col in range(n):
                # ========== CONSTRAINT CHECK (Pruning) ==========
                # Skip if this column is already occupied
                if col in used_cols:
                    continue
                
                # Calculate diagonal identifiers
                # Main diagonal (\): all cells on same diagonal have same (row - col)
                # Anti-diagonal (/): all cells on same diagonal have same (row + col)
                diag1 = row - col  # Main diagonal identifier
                diag2 = row + col  # Anti-diagonal identifier
                
                # Skip if either diagonal is already under attack
                if diag1 in used_diag1 or diag2 in used_diag2:
                    continue
                
                # ========== MAKE CHOICE ==========
                board[row] = col
                used_cols.add(col)
                used_diag1.add(diag1)
                used_diag2.add(diag2)
                
                # ========== EXPLORE ==========
                backtrack(row + 1)
                
                # ========== UNDO CHOICE (Backtrack) ==========
                # Restore state for the next iteration
                board[row] = -1
                used_cols.discard(col)
                used_diag1.discard(diag1)
                used_diag2.discard(diag2)
        
        # Start backtracking from row 0
        backtrack(0)
        return results
    
    def _build_board(self, board: List[int]) -> List[str]:
        """
        Convert the board array to the required string format.
        
        board[row] = col means queen at position (row, col)
        Output: ["..Q.", "Q...", "...Q", ".Q.."] for n=4
        """
        n = len(board)
        result: List[str] = []
        
        for row in range(n):
            # Create a row of dots, then place 'Q' at the queen's column
            row_chars = ['.'] * n
            row_chars[board[row]] = 'Q'
            result.append(''.join(row_chars))
        
        return result


# ============================================
# Solution 2: Backtracking with Bitmask
# Time: O(N!), Space: O(N) - slightly better constants
# ============================================
#
# OPTIMIZATION:
# Using bitmasks instead of hash sets provides:
# 1. Better cache locality (integers vs. hash table)
# 2. Faster operations (bitwise AND/OR vs. hash lookup)
# 3. Lower memory overhead (3 integers vs. 3 hash sets)
#
# HOW BITMASK WORKS:
# - Each bit position represents a column or diagonal
# - Bit = 1 means that column/diagonal is under attack
# - To check if column c is free: (cols & (1 << c)) == 0
# - To mark column c as used: cols |= (1 << c)
# - To unmark column c: cols &= ~(1 << c)
#
# NOTE:
# This solution is more performant but harder to understand.
# Recommended after mastering the hash set approach first.
# ============================================
class SolutionBacktrackBitmask:
    """
    Backtracking solution using bitmasks for ultra-fast conflict detection.
    
    This is an optimized version that uses bitwise operations instead of hash sets.
    Preferred for competitive programming or when maximum performance is needed.
    """
    
    def solveNQueens(self, n: int) -> List[List[str]]:
        results: List[List[str]] = []
        board: List[int] = [-1] * n
        
        def backtrack(row: int, cols: int, diag1: int, diag2: int) -> None:
            """
            Place queens using bitmasks for constraint tracking.
            
            Args:
                row: Current row to place a queen
                cols: Bitmask of occupied columns
                diag1: Bitmask of occupied main diagonals (shifted)
                diag2: Bitmask of occupied anti-diagonals (shifted)
            """
            if row == n:
                results.append(self._build_board(board, n))
                return
            
            # available_positions = columns that are not under attack
            # We need to consider all three constraints simultaneously
            # For a column c to be available:
            #   - Column c must not be in cols
            #   - The main diagonal at this row must not be in diag1
            #   - The anti-diagonal at this row must not be in diag2
            
            for col in range(n):
                col_bit = 1 << col
                
                # Check all three constraints using bitwise AND
                if cols & col_bit:
                    continue
                if diag1 & col_bit:
                    continue
                if diag2 & col_bit:
                    continue
                
                # Place queen and recurse
                board[row] = col
                
                # Key insight for diagonal bitmasks:
                # - diag1 shifts LEFT as we go down (main diagonal goes right)
                # - diag2 shifts RIGHT as we go down (anti-diagonal goes left)
                backtrack(
                    row + 1,
                    cols | col_bit,
                    (diag1 | col_bit) << 1,  # Shift left for next row
                    (diag2 | col_bit) >> 1   # Shift right for next row
                )
                
                board[row] = -1
        
        backtrack(0, 0, 0, 0)
        return results
    
    def _build_board(self, board: List[int], n: int) -> List[str]:
        """Convert board array to string format."""
        result: List[str] = []
        for row in range(n):
            row_chars = ['.'] * n
            row_chars[board[row]] = 'Q'
            result.append(''.join(row_chars))
        return result


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================
def solve():
    """
    Input format:
    Line 1: n (board size)

    Example:
    4
    """
    import sys
    
    # Parse input
    lines = sys.stdin.read().strip().split('\n')
    n = int(lines[0])
    
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.solveNQueens(n)
    
    # Output result
    # Note: JUDGE_FUNC handles order-independent validation
    # No need to sort here - the test runner will use JUDGE_FUNC
    print(result)


if __name__ == "__main__":
    solve()

