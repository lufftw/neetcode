"""
Test Case Generator for Problem 2202 - Maximize the Topmost Element After K Moves

LeetCode Constraints:
- 1 <= nums.length <= 10^5
- 0 <= nums[i], k <= 10^9
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        ([5,2,2,4,0,6], 4),  # Example 1
        ([2], 1),            # Example 2: single element, odd k
        ([2], 2),            # Single element, even k
        ([1,2,3], 0),        # k = 0
        ([1,2,3], 1),        # k = 1
        ([3,2,1], 2),        # k = 2
        ([1,2,3,4,5], 10),   # k > n
        ([1], 0),            # Single, k = 0
        ([5,1,2,3], 3),      # Various
    ]

    for nums, k in edge_cases:
        yield f"{json.dumps(nums, separators=(',', ':'))}\n{json.dumps(k)}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        n = random.randint(1, 20)
        nums = [random.randint(0, 100) for _ in range(n)]
        k = random.randint(0, 30)
        yield f"{json.dumps(nums, separators=(',', ':'))}\n{json.dumps(k)}"


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific array length n."""
    n = max(1, min(n, 10000))
    nums = [random.randint(0, 10**6) for _ in range(n)]
    k = random.randint(0, n + 10)
    return f"{json.dumps(nums, separators=(',', ':'))}\n{json.dumps(k)}"
