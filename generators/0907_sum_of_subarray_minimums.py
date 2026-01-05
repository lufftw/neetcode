# generators/0907_sum_of_subarray_minimums.py
"""
Test Case Generator for Problem 0907 - Sum of Subarray Minimums

LeetCode Constraints:
- 1 <= arr.length <= 3 * 10^4
- 1 <= arr[i] <= 3 * 10^4

Time Complexity: O(n) with monotonic stack contribution counting
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Sum of Subarray Minimums.

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
        [3, 1, 2, 4],        # Classic example
        [11, 81, 94, 43, 3], # Second example
        [1],                  # Single element
        [1, 1],               # Duplicates
        [1, 2, 3],            # Increasing
        [3, 2, 1],            # Decreasing
        [2, 2, 2, 2],         # All equal
        [1, 3, 1],            # Valley pattern
        [3, 1, 3],            # Peak pattern
    ]

    for edge in edge_cases:
        yield json.dumps(edge, separators=(",", ":"))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        size = random.randint(1, 15000)
        yield _generate_case(size)


def _generate_case(size: int) -> str:
    """Generate a single random test case."""
    max_val = 3 * 10**4
    arr = [random.randint(1, max_val) for _ in range(size)]
    return json.dumps(arr, separators=(",", ":"))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific input size for complexity estimation."""
    n = max(1, n)
    return _generate_case(n)
