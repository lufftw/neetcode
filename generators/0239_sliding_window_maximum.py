# generators/0239_sliding_window_maximum.py
"""
Test Case Generator for Problem 0239 - Sliding Window Maximum

LeetCode Constraints:
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4
- 1 <= k <= nums.length

Time Complexity: O(n) with monotonic deque
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Sliding Window Maximum.

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
        ([1, 3, -1, -3, 5, 3, 6, 7], 3),  # Classic example
        ([1], 1),                          # Single element
        ([1, -1], 1),                       # Two elements, k=1
        ([9, 11], 2),                       # Two elements, k=2
        ([4, 3, 2, 1], 2),                  # Decreasing
        ([1, 2, 3, 4], 2),                  # Increasing
        ([7, 7, 7, 7], 3),                  # All same
        ([-1, -2, -3, -4], 2),              # All negative
        ([1, 3, 1, 2, 0, 5], 3),            # Mixed
    ]

    for nums, k in edge_cases:
        yield f"{json.dumps(nums, separators=(',', ':'))}\n{k}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case."""
    size = random.randint(1, 10000)
    k = random.randint(1, size)
    nums = [random.randint(-10000, 10000) for _ in range(size)]
    return f"{json.dumps(nums, separators=(',', ':'))}\n{k}"


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific input size for complexity estimation."""
    n = max(1, n)
    k = max(1, n // 10) if n >= 10 else 1  # k is roughly 10% of n
    nums = [random.randint(-10000, 10000) for _ in range(n)]
    return f"{json.dumps(nums, separators=(',', ':'))}\n{k}"
