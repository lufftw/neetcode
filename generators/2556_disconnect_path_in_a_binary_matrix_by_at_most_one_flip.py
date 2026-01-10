"""
Test Case Generator for Problem 2556 - Disconnect Path in Binary Matrix

LeetCode Constraints:
- 1 <= m, n <= 1000
- 1 <= m * n <= 10^5
- grid[0][0] == grid[m-1][n-1] == 1
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        ([[1, 1, 1], [1, 0, 0], [1, 1, 1]],),       # Example 1: true
        ([[1, 1, 1], [1, 0, 1], [1, 1, 1]],),       # Example 2: false
        ([[1, 1], [1, 1]],),                         # Small 2x2
        ([[1]],),                                    # Single cell
        ([[1, 0, 1], [1, 1, 1]],),                  # Only one path
        ([[1, 1], [0, 1]],),                         # Narrow path
    ]

    for args in edge_cases:
        yield json.dumps(args[0], separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        m = random.randint(2, 8)
        n = random.randint(2, 8)
        grid = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
        grid[0][0] = 1
        grid[m-1][n-1] = 1
        yield json.dumps(grid, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    side = max(2, int(n ** 0.5))
    side = min(side, 50)
    grid = [[random.choice([0, 1]) for _ in range(side)] for _ in range(side)]
    grid[0][0] = 1
    grid[side-1][side-1] = 1
    return json.dumps(grid, separators=(',', ':'))
