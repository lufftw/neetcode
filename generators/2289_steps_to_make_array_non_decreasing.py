"""
Test Case Generator for Problem 2289 - Steps to Make Array Non-decreasing

LeetCode Constraints:
- 1 <= nums.length <= 10^5
- 1 <= nums[i] <= 10^9
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        [5,3,4,4,7,3,6,11,8,5,11],  # Example 1
        [4,5,7,7,13],               # Example 2: already sorted
        [1],                         # Single element
        [5,4,3,2,1],                # Strictly decreasing
        [1,2,3,4,5],                # Strictly increasing
        [3,3,3,3],                  # All equal
        [5,1,2,3,4],                # One removal chain
    ]

    for case in edge_cases:
        yield json.dumps(case, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        n = random.randint(2, 50)
        nums = [random.randint(1, 100) for _ in range(n)]
        yield json.dumps(nums, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    n = max(1, min(n, 10000))
    nums = [random.randint(1, 10**6) for _ in range(n)]
    return json.dumps(nums, separators=(',', ':'))
