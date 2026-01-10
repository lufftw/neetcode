# generators/0695_max_area_of_island.py
"""
Test Case Generator for Problem 0695 - Max Area of Island

LeetCode Constraints:
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 50
- grid[i][j] is either 0 or 1
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Max Area of Island."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        [[0]],                    # Single water cell
        [[1]],                    # Single land cell
        [[0, 0], [0, 0]],        # All water
        [[1, 1], [1, 1]],        # All land
        [[1, 0], [0, 1]],        # Diagonal (not connected)
    ]

    for grid in edge_cases:
        yield json.dumps(grid)
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random grid."""
    m = random.randint(3, 15)
    n = random.randint(3, 15)

    # Random density of land cells
    density = random.uniform(0.2, 0.6)

    grid = [[1 if random.random() < density else 0 for _ in range(n)] for _ in range(m)]

    return json.dumps(grid)


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with n total cells for complexity estimation.

    Creates a square-ish grid of approximately n cells.
    All solutions should show O(n) behavior where n = m * grid_n.
    """
    n = max(1, min(n, 2500))  # Max 50x50

    # Make grid approximately square
    side = int(n ** 0.5)
    m = max(1, side)
    grid_n = max(1, n // m)

    # Mix of land and water
    density = 0.4
    grid = [[1 if random.random() < density else 0 for _ in range(grid_n)] for _ in range(m)]

    return json.dumps(grid)


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}: {test}")
