# generators/0036_valid_sudoku.py
"""
Test Case Generator for Problem 0036 - Valid Sudoku

LeetCode Constraints:
- board.length == 9
- board[i].length == 9
- board[i][j] is a digit 1-9 or '.'.
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Valid Sudoku.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (JSON 2D array)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        _empty_board(),                    # All dots
        _full_valid_board(),               # Complete valid sudoku
        _invalid_row_board(),              # Duplicate in row
        _invalid_col_board(),              # Duplicate in column
        _invalid_box_board(),              # Duplicate in 3x3 box
        _sparse_valid_board(10),           # Few filled cells, valid
        _sparse_valid_board(30),           # Medium filled cells, valid
    ]

    for board in edge_cases:
        yield json.dumps(board, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _empty_board() -> List[List[str]]:
    """Return a board with all empty cells."""
    return [['.' for _ in range(9)] for _ in range(9)]


def _full_valid_board() -> List[List[str]]:
    """Return a complete valid sudoku board."""
    # A known valid sudoku solution
    return [
        ['5', '3', '4', '6', '7', '8', '9', '1', '2'],
        ['6', '7', '2', '1', '9', '5', '3', '4', '8'],
        ['1', '9', '8', '3', '4', '2', '5', '6', '7'],
        ['8', '5', '9', '7', '6', '1', '4', '2', '3'],
        ['4', '2', '6', '8', '5', '3', '7', '9', '1'],
        ['7', '1', '3', '9', '2', '4', '8', '5', '6'],
        ['9', '6', '1', '5', '3', '7', '2', '8', '4'],
        ['2', '8', '7', '4', '1', '9', '6', '3', '5'],
        ['3', '4', '5', '2', '8', '6', '1', '7', '9'],
    ]


def _sparse_valid_board(num_cells: int) -> List[List[str]]:
    """Return a valid board with only some cells filled."""
    full_board = _full_valid_board()
    # Convert some cells to '.'
    positions = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(positions)

    for r, c in positions[num_cells:]:
        full_board[r][c] = '.'

    return full_board


def _invalid_row_board() -> List[List[str]]:
    """Return a board with duplicate in a row."""
    board = _empty_board()
    board[0][0] = '5'
    board[0][4] = '5'  # Duplicate 5 in row 0
    return board


def _invalid_col_board() -> List[List[str]]:
    """Return a board with duplicate in a column."""
    board = _empty_board()
    board[0][0] = '3'
    board[5][0] = '3'  # Duplicate 3 in column 0
    return board


def _invalid_box_board() -> List[List[str]]:
    """Return a board with duplicate in a 3x3 box."""
    board = _empty_board()
    board[0][0] = '8'
    board[2][2] = '8'  # Duplicate 8 in top-left box
    return board


def _generate_case() -> str:
    """Generate a single random test case."""
    # Randomly decide if valid or invalid
    if random.random() < 0.6:
        # Generate valid board
        num_cells = random.randint(17, 40)  # 17 is minimum for unique solution
        board = _sparse_valid_board(num_cells)
    else:
        # Generate invalid board
        board = _generate_invalid_board()

    return json.dumps(board, separators=(',', ':'))


def _generate_invalid_board() -> List[List[str]]:
    """Generate a random invalid board."""
    board = _sparse_valid_board(random.randint(20, 35))

    # Add a duplicate to make it invalid
    invalid_type = random.choice(['row', 'col', 'box'])

    if invalid_type == 'row':
        row = random.randint(0, 8)
        digit = str(random.randint(1, 9))
        cols = [c for c in range(9) if board[row][c] == '.']
        if len(cols) >= 2:
            board[row][cols[0]] = digit
            board[row][cols[1]] = digit

    elif invalid_type == 'col':
        col = random.randint(0, 8)
        digit = str(random.randint(1, 9))
        rows = [r for r in range(9) if board[r][col] == '.']
        if len(rows) >= 2:
            board[rows[0]][col] = digit
            board[rows[1]][col] = digit

    else:  # box
        box_row = random.randint(0, 2) * 3
        box_col = random.randint(0, 2) * 3
        digit = str(random.randint(1, 9))
        cells = [(r, c) for r in range(box_row, box_row + 3)
                 for c in range(box_col, box_col + 3) if board[r][c] == '.']
        if len(cells) >= 2:
            board[cells[0][0]][cells[0][1]] = digit
            board[cells[1][0]][cells[1][1]] = digit

    return board


# ============================================
# Complexity Estimation
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case for complexity estimation.

    For Valid Sudoku, the board size is fixed at 9x9,
    so complexity is constant O(81) = O(1).

    Args:
        n: Ignored (board size is fixed)

    Returns:
        str: Test input
    """
    num_cells = random.randint(17, 40)
    board = _sparse_valid_board(num_cells)
    return json.dumps(board, separators=(',', ':'))


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(3, seed=42), 1):
        board = json.loads(test)
        print(f"Test {i}:")
        for row in board:
            print(f"  {row}")
        print()
