"""
Test Case Generator for Problem 2195 - Append K Integers With Minimal Sum

LeetCode Constraints:
- 1 <= nums.length <= 10^5
- 1 <= nums[i] <= 10^9
- 1 <= k <= 10^8
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        ([1, 4, 25, 10, 25], 2),   # Example 1
        ([5, 6], 6),               # Example 2
        ([1], 1),                  # Single element, k=1
        ([2], 1),                  # Missing 1
        ([1, 2, 3], 3),            # Consecutive blocked
        ([1000000000], 5),         # Large value, small k
    ]

    for nums, k in edge_cases:
        yield f"{json.dumps(nums, separators=(',', ':'))}\n{k}"
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        n = random.randint(1, 20)
        nums = [random.randint(1, 100) for _ in range(n)]
        k = random.randint(1, 50)  # Keep small for reference
        yield f"{json.dumps(nums, separators=(',', ':'))}\n{k}"


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    n = max(1, min(n, 100))
    nums = [random.randint(1, 1000) for _ in range(n)]
    k = random.randint(1, 100)  # Keep small for reference
    return f"{json.dumps(nums, separators=(',', ':'))}\n{k}"
