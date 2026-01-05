# generators/0560_subarray_sum_equals_k.py
"""
Test Case Generator for Problem 0560 - Subarray Sum Equals K

LeetCode Constraints:
- 1 <= nums.length <= 2 * 10^4
- -1000 <= nums[i] <= 1000
- -10^7 <= k <= 10^7

Time Complexity: O(n) with prefix sum + hash map
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Subarray Sum Equals K.

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
        ([1, 1, 1], 2),                    # Classic example
        ([1, 2, 3], 3),                    # Multiple answers
        ([1], 1),                          # Single element equals k
        ([1], 0),                          # Single element, k=0
        ([0, 0, 0], 0),                    # All zeros, k=0
        ([-1, -1, 1], 0),                  # Negative numbers summing to 0
        ([1, -1, 1, -1], 0),               # Alternating, k=0
        ([3, 4, 7, 2, -3, 1, 4, 2], 7),    # Mixed with target 7
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
    n = random.randint(1, 1000)
    nums = [random.randint(-1000, 1000) for _ in range(n)]

    # Choose k that's likely to have some matches
    if random.random() < 0.3:
        # Use actual sum of some subarray
        left = random.randint(0, n - 1)
        right = random.randint(left, n - 1)
        k = sum(nums[left:right + 1])
    else:
        k = random.randint(-10000, 10000)

    return f"{json.dumps(nums, separators=(',', ':'))}\n{k}"


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size for complexity estimation."""
    nums = [random.randint(-1000, 1000) for _ in range(n)]
    k = random.randint(-10000, 10000)
    return f"{json.dumps(nums, separators=(',', ':'))}\n{k}"
