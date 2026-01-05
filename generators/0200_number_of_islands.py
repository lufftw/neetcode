# generators/0200_number_of_islands.py
"""
Test Case Generator for Problem 0200 - Number of Islands

LeetCode Constraints:
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 300
- grid[i][j] is '0' or '1'
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Number of Islands.

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
        [["1", "1", "1", "1", "0"], ["1", "1", "0", "1", "0"],
         ["1", "1", "0", "0", "0"], ["0", "0", "0", "0", "0"]],  # 1 island
        [["1", "1", "0", "0", "0"], ["1", "1", "0", "0", "0"],
         ["0", "0", "1", "0", "0"], ["0", "0", "0", "1", "1"]],  # 3 islands
        [["1"]],  # Single cell island
        [["0"]],  # Single cell water
        [["1", "0", "1", "0", "1"]],  # Single row alternating
        [["1"], ["0"], ["1"], ["0"], ["1"]],  # Single column alternating
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
    m = random.randint(1, 50)  # Keep smaller for stress tests
    n = random.randint(1, 50)

    # Vary density of 1s
    density = random.uniform(0.2, 0.7)
    grid = [[random.choices(['0', '1'], weights=[1 - density, density])[0]
             for _ in range(n)] for _ in range(m)]

    return json.dumps(grid, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    Args:
        n: Target total cells (m * n)

    Returns:
        str: Grid with approximately n total cells
    """
    side = max(1, int(n ** 0.5))
    m = side
    n_cols = max(1, n // m)

    density = 0.5
    grid = [[random.choices(['0', '1'], weights=[1 - density, density])[0]
             for _ in range(n_cols)] for _ in range(m)]

    return json.dumps(grid, separators=(',', ':'))
