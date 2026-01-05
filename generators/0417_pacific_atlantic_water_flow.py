# generators/0417_pacific_atlantic_water_flow.py
"""
Test Case Generator for Problem 0417 - Pacific Atlantic Water Flow

LeetCode Constraints:
- m == heights.length
- n == heights[r].length
- 1 <= m, n <= 200
- 0 <= heights[r][c] <= 10^5
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Pacific Atlantic Water Flow.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: 2D heights array in JSON format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1],
         [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]],  # Classic example
        [[1]],  # Single cell (reaches both)
        [[1, 1], [1, 1]],  # All same height
        [[1, 2], [4, 3]],  # 2x2 grid
        [[10, 10, 10], [10, 1, 10], [10, 10, 10]],  # Valley in middle
    ]

    for heights in edge_cases:
        yield json.dumps(heights, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case."""
    m = random.randint(1, 50)
    n = random.randint(1, 50)

    # Generate heights with varying patterns
    pattern = random.choice(['random', 'gradient', 'peaks'])

    if pattern == 'random':
        heights = [[random.randint(0, 1000) for _ in range(n)] for _ in range(m)]
    elif pattern == 'gradient':
        # Gradient from top-left to bottom-right
        heights = [[i + j + random.randint(0, 10) for j in range(n)] for i in range(m)]
    else:  # peaks
        # Random peaks
        heights = [[random.randint(0, 100) for _ in range(n)] for _ in range(m)]
        num_peaks = random.randint(1, 5)
        for _ in range(num_peaks):
            pr, pc = random.randint(0, m - 1), random.randint(0, n - 1)
            heights[pr][pc] = random.randint(500, 1000)

    return json.dumps(heights, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size.

    Args:
        n: Target total cells (m * n)

    Returns:
        str: Heights grid with approximately n total cells
    """
    side = max(1, int(n ** 0.5))
    m = min(200, side)
    n_cols = min(200, max(1, n // m))

    heights = [[random.randint(0, 1000) for _ in range(n_cols)] for _ in range(m)]

    return json.dumps(heights, separators=(',', ':'))
