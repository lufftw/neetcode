# generators/0778_swim_in_rising_water.py
"""
Test Case Generator for Problem 0778 - Swim in Rising Water

LeetCode Constraints:
- n == grid.length == grid[i].length
- 1 <= n <= 50
- 0 <= grid[i][j] < n^2
- Each value grid[i][j] is unique
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Swim in Rising Water.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (grid as JSON 2D array)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # LeetCode Example 1: 2x2 grid
        [[0, 2], [1, 3]],
        # LeetCode Example 2: 5x5 spiral-like pattern
        [
            [0, 1, 2, 3, 4],
            [24, 23, 22, 21, 5],
            [12, 13, 14, 15, 16],
            [11, 17, 18, 19, 20],
            [10, 9, 8, 7, 6],
        ],
        # Minimum case: 1x1 grid
        [[0]],
        # Direct path optimal: values increase along diagonal
        [[0, 3, 6], [1, 4, 7], [2, 5, 8]],
        # Start at 0, must wait for high barrier
        [[0, 8, 7], [6, 5, 4], [3, 2, 1]],
    ]

    for grid in edge_cases:
        yield json.dumps(grid, separators=(",", ":"))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random n x n grid with unique values."""
    n = random.randint(2, 15)  # Moderate size for random tests
    return _generate_grid(n)


def _generate_grid(n: int) -> str:
    """Generate an n x n grid with unique values from 0 to n^2-1."""
    values = list(range(n * n))
    random.shuffle(values)

    grid = []
    for i in range(n):
        row = values[i * n : (i + 1) * n]
        grid.append(row)

    return json.dumps(grid, separators=(",", ":"))


# ============================================
# Complexity Estimation
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Swim in Rising Water:
    - n is the grid dimension (n x n grid)
    - Time complexity is O(n^2 log n) for Dijkstra
    - We generate a grid where the optimal path requires visiting many cells

    Args:
        n: Grid dimension (will be clamped to [1, 50])

    Returns:
        str: Test input (grid as JSON)
    """
    # Clamp to LeetCode constraints
    n = max(1, min(n, 50))

    # Generate grid with shuffled values for realistic complexity
    values = list(range(n * n))
    random.shuffle(values)

    grid = []
    for i in range(n):
        row = values[i * n : (i + 1) * n]
        grid.append(row)

    return json.dumps(grid, separators=(",", ":"))


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(5, seed=42), 1):
        grid = json.loads(test)
        n = len(grid)
        print(f"Test {i}: {n}x{n} grid")
        if n <= 5:
            for row in grid:
                print(f"  {row}")
        print()
