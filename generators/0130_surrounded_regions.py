# generators/0130_surrounded_regions.py
"""
Test Case Generator for Problem 0130 - Surrounded Regions

LeetCode Constraints:
- m == board.length
- n == board[i].length
- 1 <= m, n <= 200
- board[i][j] is 'X' or 'O'
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Surrounded Regions."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        [["X"]],
        [["O"]],
        [["X", "X"], ["X", "X"]],
        [["O", "O"], ["O", "O"]],
        [["X", "O", "X"], ["O", "X", "O"], ["X", "O", "X"]],
    ]

    for board in edge_cases:
        yield json.dumps(board)
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random board."""
    m = random.randint(3, 10)
    n = random.randint(3, 10)

    # Random density of O's
    density = random.uniform(0.3, 0.6)

    board = [["X" if random.random() > density else "O" for _ in range(n)] for _ in range(m)]

    return json.dumps(board)


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with approximately n total cells.
    """
    n = max(1, min(n, 40000))  # Max 200x200

    side = int(n ** 0.5)
    m = max(1, side)
    board_n = max(1, n // m)

    density = 0.4
    board = [["X" if random.random() > density else "O" for _ in range(board_n)] for _ in range(m)]

    return json.dumps(board)


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}: {test}")
