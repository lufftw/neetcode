# generators/0739_daily_temperatures.py
"""
Test Case Generator for Problem 0739 - Daily Temperatures

LeetCode Constraints:
- 1 <= temperatures.length <= 10^5
- 30 <= temperatures[i] <= 100

Time Complexity: O(n) with monotonic stack
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Daily Temperatures.

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
        [73, 74, 75, 71, 69, 72, 76, 73],  # Classic example
        [30, 40, 50, 60],                   # Increasing
        [100, 90, 80, 70],                  # Decreasing
        [50],                               # Single element
        [50, 50, 50],                       # All equal
        [30, 100, 30],                      # Peak
        [100, 30, 100],                     # Valley
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
    temps = [random.randint(30, 100) for _ in range(size)]
    return json.dumps(temps, separators=(",", ":"))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific input size for complexity estimation."""
    n = max(1, n)
    return _generate_case(n)
