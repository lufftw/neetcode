# generators/1631_path_with_minimum_effort.py
"""
Test Case Generator for Problem 1631 - Path With Minimum Effort

LeetCode Constraints:
- rows == heights.length
- columns == heights[i].length
- 1 <= rows, columns <= 100
- 1 <= heights[i][j] <= 10^6
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Path With Minimum Effort.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: heights grid in JSON format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [[1, 2, 2], [3, 8, 2], [5, 3, 5]],  # Example 1: answer 2
        [[1, 2, 3], [3, 8, 4], [5, 3, 5]],  # Example 2: answer 1
        [[1, 2, 1, 1, 1], [1, 2, 1, 2, 1], [1, 2, 1, 2, 1], [1, 2, 1, 2, 1], [1, 1, 1, 2, 1]],  # answer 0
        [[1]],  # Single cell
        [[1, 2], [3, 4]],  # 2x2 grid
        [[1, 1, 1], [1, 1, 1], [1, 1, 1]],  # All same height (answer 0)
    ]

    for heights in edge_cases:
        yield json.dumps(heights, separators=(',', ':'))
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

    # Different height distributions
    dist_type = random.choice(['uniform', 'gradient', 'random'])

    if dist_type == 'uniform':
        base = random.randint(1, 1000)
        variation = random.randint(0, 10)
        heights = [[base + random.randint(-variation, variation)
                    for _ in range(cols)] for _ in range(rows)]
    elif dist_type == 'gradient':
        heights = [[i * 10 + j * 10 + random.randint(1, 100)
                    for j in range(cols)] for i in range(rows)]
    else:
        heights = [[random.randint(1, 10000) for _ in range(cols)] for _ in range(rows)]

    # Ensure all values are positive
    heights = [[max(1, h) for h in row] for row in heights]

    return json.dumps(heights, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    Args:
        n: Target total cells (rows * cols)

    Returns:
        str: Heights grid with approximately n cells
    """
    side = max(2, int(n ** 0.5))
    rows = side
    cols = max(2, n // side)

    heights = [[random.randint(1, 10000) for _ in range(cols)] for _ in range(rows)]

    return json.dumps(heights, separators=(',', ':'))
