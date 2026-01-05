# generators/2104_sum_of_subarray_ranges.py
"""
Test Case Generator for Problem 2104 - Sum of Subarray Ranges

LeetCode Constraints:
- 1 <= nums.length <= 1000
- -10^9 <= nums[i] <= 10^9

Time Complexity: O(n) with dual monotonic stacks (optimal)
               O(n^2) with brute force (acceptable for n <= 1000)
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Sum of Subarray Ranges.

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
        [1, 2, 3],          # Classic example
        [1, 3, 3],          # With duplicates
        [4, -2, -3, 4, 1],  # With negatives
        [1],                # Single element
        [5, 5],             # Two equal
        [1, 5],             # Two different
        [1, 2, 3, 4, 5],    # Increasing
        [5, 4, 3, 2, 1],    # Decreasing
        [3, 1, 2, 4, 1, 3], # Random pattern
    ]

    for edge in edge_cases:
        yield json.dumps(edge, separators=(",", ":"))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        size = random.randint(1, 500)
        yield _generate_case(size)


def _generate_case(size: int) -> str:
    """Generate a single random test case."""
    nums = [random.randint(-10**6, 10**6) for _ in range(size)]
    return json.dumps(nums, separators=(",", ":"))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific input size for complexity estimation."""
    n = max(1, min(n, 1000))
    return _generate_case(n)
