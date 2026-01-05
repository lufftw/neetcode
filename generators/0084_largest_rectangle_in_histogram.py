# generators/0084_largest_rectangle_in_histogram.py
"""
Test Case Generator for Problem 0084 - Largest Rectangle in Histogram

LeetCode Constraints:
- 1 <= heights.length <= 10^5
- 0 <= heights[i] <= 10^4

Time Complexity: O(n) with monotonic stack
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Largest Rectangle in Histogram.

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
        [2, 1, 5, 6, 2, 3],  # Classic example
        [2, 4],              # Two bars
        [1],                 # Single bar
        [0],                 # Zero height
        [1, 1, 1, 1, 1],     # All equal
        [1, 2, 3, 4, 5],     # Increasing
        [5, 4, 3, 2, 1],     # Decreasing
        [2, 1, 2],           # Valley
        [1, 2, 1],           # Peak
        [0, 0, 0],           # All zeros
    ]

    for edge in edge_cases:
        yield json.dumps(edge, separators=(",", ":"))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        size = random.randint(1, 50000)
        yield _generate_case(size)


def _generate_case(size: int) -> str:
    """Generate a single random test case."""
    max_height = 10**4
    heights = [random.randint(0, max_height) for _ in range(size)]
    return json.dumps(heights, separators=(",", ":"))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific input size for complexity estimation."""
    n = max(1, n)
    return _generate_case(n)
