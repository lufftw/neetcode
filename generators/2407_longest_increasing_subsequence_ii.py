"""
Test Case Generator for Problem 2407 - Longest Increasing Subsequence II

LeetCode Constraints:
- 1 <= nums.length <= 10^5
- 1 <= nums[i], k <= 10^5
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        ([4, 2, 1, 4, 3, 4, 5, 8, 15], 3),  # Example 1
        ([7, 4, 5, 1, 8, 12, 4, 7], 5),     # Example 2
        ([1, 5], 1),                         # Example 3
        ([1], 1),                            # Single element
        ([1, 2, 3, 4, 5], 1),                # Strictly increasing by 1
        ([5, 4, 3, 2, 1], 1),                # Decreasing
        ([1, 2, 3, 4, 5], 100),              # Large k
        ([1, 1, 1, 1, 1], 1),                # All same (no valid LIS > 1)
    ]

    for nums, k in edge_cases:
        yield f"{json.dumps(nums, separators=(',', ':'))}\n{k}"
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        n = random.randint(5, 50)
        max_val = random.randint(10, 100)
        nums = [random.randint(1, max_val) for _ in range(n)]
        k = random.randint(1, max_val // 2 + 1)
        yield f"{json.dumps(nums, separators=(',', ':'))}\n{k}"


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    n = max(5, min(n, 10000))
    max_val = min(n * 10, 100000)
    nums = [random.randint(1, max_val) for _ in range(n)]
    k = random.randint(1, max_val // 2)
    return f"{json.dumps(nums, separators=(',', ':'))}\n{k}"
