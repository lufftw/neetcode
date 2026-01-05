# generators/0523_continuous_subarray_sum.py
"""
Test Case Generator for Problem 0523 - Continuous Subarray Sum

LeetCode Constraints:
- 1 <= nums.length <= 10^5
- 0 <= nums[i] <= 10^9
- 0 <= sum(nums[i]) <= 2^31 - 1
- 1 <= k <= 2^31 - 1

Time Complexity: O(n) with prefix sum modulo + hash map
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Continuous Subarray Sum.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Test input in JSON format (nums, k)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        ([23, 2, 4, 6, 7], 6),     # Classic: subarray [2,4] sums to 6
        ([23, 2, 6, 4, 7], 6),     # [2,6,4] sums to 12, divisible by 6
        ([23, 2, 6, 4, 7], 13),    # [2,6,4,7]=19, not divisible by 13
        ([5, 0, 0, 0], 3),         # Consecutive zeros
        ([0, 0], 1),               # Two zeros
        ([1, 0], 2),               # False - length 2 but sum 1
        ([0, 1, 0], 1),            # Any subarray size >= 2 works when k=1
        ([1, 2, 3], 6),            # Full array sums to 6
        ([1, 2, 3], 5),            # [2,3] sums to 5
    ]

    for nums, k in edge_cases:
        yield f"{json.dumps(nums, separators=(',', ':'))}\n{k}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a single random test case."""
    n = random.randint(2, 1000)  # Must be at least 2 for valid subarray
    nums = [random.randint(0, 10000) for _ in range(n)]
    k = random.randint(1, 10000)
    return f"{json.dumps(nums, separators=(',', ':'))}\n{k}"


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size for complexity estimation."""
    nums = [random.randint(0, 10000) for _ in range(n)]
    k = random.randint(1, 10000)
    return f"{json.dumps(nums, separators=(',', ':'))}\n{k}"
