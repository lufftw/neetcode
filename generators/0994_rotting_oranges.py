# generators/0994_rotting_oranges.py
"""
Test Case Generator for Problem 0994 - Rotting Oranges

LeetCode Constraints:
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 10
- grid[i][j] is 0, 1, or 2
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Rotting Oranges.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: 2D grid in JSON format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [[2, 1, 1], [1, 1, 0], [0, 1, 1]],  # Classic: 4 minutes
        [[2, 1, 1], [0, 1, 1], [1, 0, 1]],  # Unreachable: -1
        [[0, 2]],  # No fresh: 0
        [[2]],  # Only rotten: 0
        [[1]],  # Only fresh, no rotten: -1
        [[0]],  # Only empty: 0
        [[2, 1], [1, 2]],  # 1 minute (all adjacent)
    ]

    for grid in edge_cases:
        yield json.dumps(grid, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case."""
    m = random.randint(1, 10)
    n = random.randint(1, 10)

    # 0=empty, 1=fresh, 2=rotten
    # Weight towards having at least some fresh and rotten
    grid = [[random.choices([0, 1, 2], weights=[0.3, 0.5, 0.2])[0]
             for _ in range(n)] for _ in range(m)]

    # Ensure at least one rotten orange exists (to avoid trivial -1 cases)
    if not any(cell == 2 for row in grid for cell in row):
        r, c = random.randint(0, m - 1), random.randint(0, n - 1)
        grid[r][c] = 2

    return json.dumps(grid, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size.

    Args:
        n: Target total cells (capped at 100 due to constraints)

    Returns:
        str: Grid with approximately n total cells
    """
    n = min(n, 100)  # Max 10x10
    side = max(1, min(10, int(n ** 0.5)))
    m = side
    n_cols = max(1, min(10, n // m))

    grid = [[random.choices([0, 1, 2], weights=[0.3, 0.5, 0.2])[0]
             for _ in range(n_cols)] for _ in range(m)]

    # Ensure at least one rotten
    grid[0][0] = 2

    return json.dumps(grid, separators=(',', ':'))
