"""
Problem: Valid Sudoku
Link: https://leetcode.com/problems/valid-sudoku/

Determine if a 9x9 Sudoku board is valid. Only the filled cells need to be
validated according to the following rules:

1. Each row must contain the digits 1-9 without repetition.
2. Each column must contain the digits 1-9 without repetition.
3. Each of the nine 3x3 sub-boxes must contain the digits 1-9 without repetition.

Note:
- A Sudoku board (partially filled) could be valid but is not necessarily solvable.
- Only the filled cells need to be validated.

Example 1:
    Input: board = [valid 9x9 board]
    Output: true

Example 2:
    Input: board = [invalid 9x9 board with duplicate 8 in top-left box]
    Output: false

Constraints:
- board.length == 9
- board[i].length == 9
- board[i][j] is a digit 1-9 or '.'.

Topics: Array, Hash Table, Matrix
"""
import json
from typing import List, Set
from _runner import get_solver


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionHashSet",
        "method": "isValidSudoku",
        "complexity": "O(81) = O(1) time, O(81) = O(1) space",
        "description": "Hash sets for rows, columns, and boxes",
    },
    "hashset": {
        "class": "SolutionHashSet",
        "method": "isValidSudoku",
        "complexity": "O(81) = O(1) time, O(81) = O(1) space",
        "description": "Hash sets for rows, columns, and boxes",
    },
    "bitmask": {
        "class": "SolutionBitmask",
        "method": "isValidSudoku",
        "complexity": "O(81) = O(1) time, O(27) = O(1) space",
        "description": "Bitmask for compact storage",
    },
}


# ============================================================================
# Solution 1: Hash Sets
# Time: O(81) = O(1), Space: O(81) = O(1)
#   - Fixed 9x9 board means constant time and space
#   - Track seen digits in each row, column, and 3x3 box
# ============================================================================
class SolutionHashSet:
    """
    Hash set approach - clear and maintainable.

    Use sets to track which digits have been seen in each row, column,
    and 3x3 box. The key insight is mapping (row, col) to box index:
        box_index = (row // 3) * 3 + (col // 3)

    This formula groups cells into the 9 boxes numbered 0-8.
    """

    def isValidSudoku(self, board: List[List[str]]) -> bool:
        # Track seen digits for each row, column, and box
        rows: List[Set[str]] = [set() for _ in range(9)]
        cols: List[Set[str]] = [set() for _ in range(9)]
        boxes: List[Set[str]] = [set() for _ in range(9)]

        for row in range(9):
            for col in range(9):
                digit = board[row][col]

                # Skip empty cells
                if digit == '.':
                    continue

                # Calculate which 3x3 box this cell belongs to
                # Box indices:
                # 0 1 2
                # 3 4 5
                # 6 7 8
                box_idx = (row // 3) * 3 + (col // 3)

                # Check if digit already exists in row, column, or box
                if digit in rows[row]:
                    return False
                if digit in cols[col]:
                    return False
                if digit in boxes[box_idx]:
                    return False

                # Mark digit as seen
                rows[row].add(digit)
                cols[col].add(digit)
                boxes[box_idx].add(digit)

        return True


# ============================================================================
# Solution 2: Bitmask
# Time: O(81) = O(1), Space: O(27) = O(1)
#   - Use integers as bitmasks instead of sets
#   - Bit i represents whether digit (i+1) has been seen
# ============================================================================
class SolutionBitmask:
    """
    Bitmask approach - more compact storage.

    Instead of sets, use integers where bit i represents digit (i+1).
    For example, if we've seen digits 1, 3, 5, the bitmask is:
        0b10101 = 21

    Operations:
    - Check if seen: (mask & (1 << digit)) != 0
    - Mark as seen: mask |= (1 << digit)
    """

    def isValidSudoku(self, board: List[List[str]]) -> bool:
        # Bitmasks for rows, columns, and boxes (27 integers total)
        rows = [0] * 9
        cols = [0] * 9
        boxes = [0] * 9

        for row in range(9):
            for col in range(9):
                char = board[row][col]

                if char == '.':
                    continue

                # Convert char '1'-'9' to bit position 0-8
                bit = 1 << (ord(char) - ord('1'))
                box_idx = (row // 3) * 3 + (col // 3)

                # Check for duplicates using bitwise AND
                if rows[row] & bit:
                    return False
                if cols[col] & bit:
                    return False
                if boxes[box_idx] & bit:
                    return False

                # Mark as seen using bitwise OR
                rows[row] |= bit
                cols[col] |= bit
                boxes[box_idx] |= bit

        return True


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        9 lines, each containing a JSON array of 9 strings

    Example:
        ["5","3",".",".","7",".",".",".","."]
        ["6",".",".","1","9","5",".",".","."]
        ...
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')

    # Parse 9x9 board - can be single JSON array or 9 separate lines
    if len(lines) == 1:
        # Single line JSON array
        board = json.loads(lines[0])
    else:
        # 9 separate lines
        board = [json.loads(line) for line in lines[:9]]

    solver = get_solver(SOLUTIONS)
    result = solver.isValidSudoku(board)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
