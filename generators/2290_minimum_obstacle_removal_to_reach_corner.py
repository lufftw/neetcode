# generators/2290_minimum_obstacle_removal_to_reach_corner.py
"""
Test Case Generator for Problem 2290 - Minimum Obstacle Removal to Reach Corner

LeetCode Constraints:
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 10^5
- 2 <= m * n <= 10^5
- grid[i][j] is either 0 or 1
- grid[0][0] == grid[m - 1][n - 1] == 0
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Minimum Obstacle Removal.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Grid in JSON format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [[0, 1, 1], [1, 1, 0], [1, 1, 0]],  # Example 1: answer 2
        [[0, 1, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0]],  # Example 2: answer 0
        [[0, 0], [0, 0]],  # No obstacles
        [[0, 1], [1, 0]],  # Diagonal obstacles
        [[0, 0, 0], [0, 0, 0], [0, 0, 0]],  # All clear
        [[0, 1, 1, 0], [1, 1, 1, 1], [0, 1, 1, 0]],  # Dense obstacles
    ]

    for grid in edge_cases:
        yield json.dumps(grid, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a single random test case."""
    rows = random.randint(2, 30)
    cols = random.randint(2, 30)

    # Different obstacle densities
    density = random.uniform(0.1, 0.6)

    grid = [[1 if random.random() < density else 0 for _ in range(cols)] for _ in range(rows)]

    # Ensure start and end are clear (constraint)
    grid[0][0] = 0
    grid[rows - 1][cols - 1] = 0

    return json.dumps(grid, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    Args:
        n: Target total cells (rows * cols)

    Returns:
        str: Grid with approximately n cells
    """
    side = max(2, int(n ** 0.5))
    rows = side
    cols = max(2, n // side)

    density = 0.3
    grid = [[1 if random.random() < density else 0 for _ in range(cols)] for _ in range(rows)]

    # Ensure start and end are clear
    grid[0][0] = 0
    grid[rows - 1][cols - 1] = 0

    return json.dumps(grid, separators=(',', ':'))
