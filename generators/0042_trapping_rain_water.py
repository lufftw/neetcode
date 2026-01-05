# generators/0042_trapping_rain_water.py
"""
Test Case Generator for Problem 0042 - Trapping Rain Water

LeetCode Constraints:
- n == height.length
- 1 <= n <= 2 * 10^4
- 0 <= height[i] <= 10^5

Time Complexity: O(n) with monotonic stack or two pointers
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Trapping Rain Water.

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
        [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1],  # Classic example
        [4, 2, 0, 3, 2, 5],                     # Simple valley
        [1],                                    # Single element
        [1, 2],                                 # Two elements (no trap)
        [2, 1],                                 # Decreasing (no trap)
        [1, 2, 3, 4, 5],                        # Strictly increasing
        [5, 4, 3, 2, 1],                        # Strictly decreasing
        [3, 0, 3],                              # Simple container
        [0, 0, 0],                              # All zeros
        [5, 5, 5, 5],                           # All equal
    ]

    for edge in edge_cases:
        yield json.dumps(edge, separators=(",", ":"))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        size = random.randint(1, 10000)
        yield _generate_case(size)


def _generate_case(size: int) -> str:
    """Generate a single random test case."""
    max_height = 10**5
    heights = [random.randint(0, max_height) for _ in range(size)]
    return json.dumps(heights, separators=(",", ":"))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific input size for complexity estimation."""
    n = max(1, n)
    return _generate_case(n)
