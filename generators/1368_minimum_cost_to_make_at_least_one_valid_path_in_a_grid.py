# generators/1368_minimum_cost_to_make_at_least_one_valid_path_in_a_grid.py
"""
Test Case Generator for Problem 1368 - Minimum Cost to Make Valid Path

LeetCode Constraints:
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 100
- 1 <= grid[i][j] <= 4
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Minimum Cost Valid Path.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Grid in JSON format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    # Direction: 1=right, 2=left, 3=down, 4=up
    edge_cases = [
        [[1, 1, 1, 1], [2, 2, 2, 2], [1, 1, 1, 1], [2, 2, 2, 2]],  # Example 1: answer 3
        [[1, 1, 3], [3, 2, 2], [1, 1, 4]],  # Example 2: answer 0
        [[1, 2], [4, 3]],  # Example 3: answer 1
        [[1]],  # Single cell
        [[1, 1], [1, 1]],  # All right (need to go down)
        [[3, 3], [3, 3]],  # All down
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
    rows = random.randint(2, 20)
    cols = random.randint(2, 20)

    # Different generation strategies
    strategy = random.choice(['random', 'path_biased', 'uniform'])

    if strategy == 'random':
        grid = [[random.randint(1, 4) for _ in range(cols)] for _ in range(rows)]
    elif strategy == 'path_biased':
        # Bias toward creating a valid path
        grid = [[0] * cols for _ in range(rows)]
        for r in range(rows):
            for c in range(cols):
                if r == rows - 1 and c < cols - 1:
                    # Last row: prefer right
                    grid[r][c] = 1 if random.random() < 0.7 else random.randint(1, 4)
                elif c == cols - 1 and r < rows - 1:
                    # Last column: prefer down
                    grid[r][c] = 3 if random.random() < 0.7 else random.randint(1, 4)
                else:
                    # Prefer right or down
                    grid[r][c] = random.choice([1, 3]) if random.random() < 0.5 else random.randint(1, 4)
    else:
        # Uniform single direction
        direction = random.randint(1, 4)
        grid = [[direction for _ in range(cols)] for _ in range(rows)]

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

    grid = [[random.randint(1, 4) for _ in range(cols)] for _ in range(rows)]

    return json.dumps(grid, separators=(',', ':'))
