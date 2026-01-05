# generators/0503_next_greater_element_ii.py
"""
Test Case Generator for Problem 0503 - Next Greater Element II

LeetCode Constraints:
- 1 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9

Time Complexity: O(n) with monotonic stack (circular)
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Next Greater Element II.

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
        [1, 2, 1],            # Classic example
        [1, 2, 3, 4, 3],      # Second example
        [1],                  # Single element
        [5, 4, 3, 2, 1],      # Decreasing (circular NGE is largest)
        [1, 2, 3, 4, 5],      # Increasing
        [3, 3, 3],            # All equal
        [1, 5, 1],            # Peak
        [5, 1, 5],            # Valley
    ]

    for edge in edge_cases:
        yield json.dumps(edge, separators=(",", ":"))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        size = random.randint(1, 5000)
        yield _generate_case(size)


def _generate_case(size: int) -> str:
    """Generate a single random test case."""
    nums = [random.randint(-10**6, 10**6) for _ in range(size)]
    return json.dumps(nums, separators=(",", ":"))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific input size for complexity estimation."""
    n = max(1, n)
    return _generate_case(n)
