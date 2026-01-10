"""
Test Case Generator for Problem 0220 - Contains Duplicate III

LeetCode Constraints:
- 2 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9
- 1 <= indexDiff <= nums.length
- 0 <= valueDiff <= 10^9
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        ([1,2,3,1], 3, 0),      # Example 1: true
        ([1,5,9,1,5,9], 2, 3),  # Example 2: false
        ([1,2], 1, 0),          # Small true
        ([1,2], 1, 1),          # Small true
        ([1,3], 1, 0),          # Small false
        ([1,1], 1, 0),          # Duplicates
        ([-1,0,1], 2, 1),       # Negative numbers
    ]

    for nums, indexDiff, valueDiff in edge_cases:
        yield f"{json.dumps(nums, separators=(',', ':'))}\n{indexDiff}\n{valueDiff}"
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        n = random.randint(2, 50)
        nums = [random.randint(-1000, 1000) for _ in range(n)]
        indexDiff = random.randint(1, n)
        valueDiff = random.randint(0, 100)
        yield f"{json.dumps(nums, separators=(',', ':'))}\n{indexDiff}\n{valueDiff}"


def generate_for_complexity(n: int) -> str:
    n = max(2, min(n, 10000))
    nums = [random.randint(-10**6, 10**6) for _ in range(n)]
    indexDiff = random.randint(1, n)
    valueDiff = random.randint(0, 10**6)
    return f"{json.dumps(nums, separators=(',', ':'))}\n{indexDiff}\n{valueDiff}"
