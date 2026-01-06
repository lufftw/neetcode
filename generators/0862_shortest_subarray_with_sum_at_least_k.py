# generators/0862_shortest_subarray_with_sum_at_least_k.py
"""
Test Case Generator for Problem 0862 - Shortest Subarray with Sum at Least K

LeetCode Constraints:
- 1 <= nums.length <= 10^5
- -10^5 <= nums[i] <= 10^5
- 1 <= k <= 10^9

Time Complexity: O(n) with prefix sum and monotonic deque
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Shortest Subarray with Sum at Least K.

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
        ([1], 1),                        # Single element = k
        ([1, 2], 4),                     # No valid subarray (-1)
        ([2, -1, 2], 3),                 # With negative, sum=3
        ([1, 2, 3], 6),                  # Exact sum
        ([1, 2, 3], 7),                  # No valid subarray
        ([5, -1, 2, 3], 6),              # Mixed with negatives
        ([-1, 2], 1),                    # Negative at start
        ([3, -2, 5], 4),                 # Negative in middle
        ([1, 1, 1, 1, 1], 3),            # Multiple valid
        ([84, -37, 32, 40, 95], 167),    # LeetCode edge case
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
    size = random.randint(1, 5000)
    # Mix of positive and negative to make it interesting
    nums = [random.randint(-1000, 1000) for _ in range(size)]

    # Choose k based on array sum to make it feasible sometimes
    total = sum(nums)
    if total > 0:
        k = random.randint(1, max(1, total))
    else:
        # With negative total, pick a reasonable k
        max_elem = max(nums) if nums else 1
        k = random.randint(1, max(1, max_elem * size // 4))

    return f"{json.dumps(nums, separators=(',', ':'))}\n{k}"


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific input size for complexity estimation."""
    n = max(1, n)
    nums = [random.randint(-100, 100) for _ in range(n)]
    total = sum(nums)
    k = max(1, abs(total) // 2) if total != 0 else n
    return f"{json.dumps(nums, separators=(',', ':'))}\n{k}"
