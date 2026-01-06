# generators/1499_max_value_of_equation.py
"""
Test Case Generator for Problem 1499 - Max Value of Equation

LeetCode Constraints:
- 2 <= points.length <= 10^5
- points[i].length == 2
- -10^8 <= xi, yi <= 10^8
- 0 <= k <= 2 * 10^8
- xi < xj for all 1 <= i < j <= points.length (strictly increasing x)

Time Complexity: O(n) with monotonic deque
"""
import json
import random
from typing import Iterator, List, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Max Value of Equation.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Test input in JSON format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        ([[1, 3], [2, 0], [5, 10], [6, -10]], 1),   # Classic example
        ([[0, 0], [3, 0], [9, 2]], 3),               # Example 2
        ([[1, 1], [2, 2]], 1),                       # Minimum valid input
        ([[1, 1], [2, 2]], 100),                     # Large k (all pairs valid)
        ([[1, -5], [2, 10], [3, -3]], 2),            # Mixed y values
        ([[0, 0], [1, 0], [2, 0], [3, 0]], 1),       # All y=0
        ([[1, 100], [2, -100], [3, 100]], 1),        # Alternating high/low
        ([[0, 5], [10, 5]], 10),                     # Exactly k apart
        ([[0, 5], [11, 5]], 10),                     # Just over k (invalid pair)
    ]

    for points, k in edge_cases:
        yield f"{json.dumps(points, separators=(',', ':'))}\n{k}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case."""
    size = random.randint(2, 5000)
    points = _generate_points(size)
    # Choose k to make it interesting (some valid, some invalid pairs)
    max_x_diff = points[-1][0] - points[0][0]
    k = random.randint(1, max(1, max_x_diff))
    return f"{json.dumps(points, separators=(',', ':'))}\n{k}"


def _generate_points(size: int) -> List[List[int]]:
    """Generate sorted points with strictly increasing x coordinates."""
    points: List[List[int]] = []
    x = 0
    for _ in range(size):
        x += random.randint(1, 100)  # Ensure strictly increasing
        y = random.randint(-10000, 10000)
        points.append([x, y])
    return points


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific input size for complexity estimation."""
    n = max(2, n)
    points = _generate_points(n)
    max_x_diff = points[-1][0] - points[0][0]
    k = max(1, max_x_diff // 2)
    return f"{json.dumps(points, separators=(',', ':'))}\n{k}"
