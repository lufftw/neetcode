# generators/1438_longest_continuous_subarray_with_absolute_diff_limit.py
"""
Test Case Generator for Problem 1438 - Longest Continuous Subarray With Absolute Diff Limit

LeetCode Constraints:
- 1 <= nums.length <= 10^5
- 1 <= nums[i] <= 10^9
- 0 <= limit <= 10^9

Time Complexity: O(n) with two monotonic deques
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Longest Continuous Subarray.

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
        ([8, 2, 4, 7], 4),                  # Classic example
        ([10, 1, 2, 4, 7, 2], 5),            # Example 2
        ([4, 2, 2, 2, 4, 4, 2, 2], 0),       # limit = 0
        ([1], 0),                            # Single element
        ([1, 2, 3, 4, 5], 10),               # All valid (large limit)
        ([1, 100, 1, 100, 1], 0),            # Alternating, limit=0
        ([1, 1, 1, 1], 0),                   # All same, limit=0
        ([5, 4, 3, 2, 1], 2),                # Decreasing
        ([1, 2, 3, 4, 5], 2),                # Increasing
    ]

    for nums, limit in edge_cases:
        yield f"{json.dumps(nums, separators=(',', ':'))}\n{limit}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case."""
    size = random.randint(1, 10000)
    # Use smaller values for testing to ensure some valid subarrays exist
    nums = [random.randint(1, 1000) for _ in range(size)]
    # Choose a limit that makes the problem interesting
    if nums:
        max_val = max(nums)
        min_val = min(nums)
        limit = random.randint(0, max(1, (max_val - min_val) // 2))
    else:
        limit = 0
    return f"{json.dumps(nums, separators=(',', ':'))}\n{limit}"


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific input size for complexity estimation."""
    n = max(1, n)
    nums = [random.randint(1, 1000) for _ in range(n)]
    limit = random.randint(0, 100)
    return f"{json.dumps(nums, separators=(',', ':'))}\n{limit}"
