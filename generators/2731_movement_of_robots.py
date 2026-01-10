"""
Test Case Generator for Problem 2731 - Movement of Robots

LeetCode Constraints:
- 2 <= nums.length <= 10^5
- -2 * 10^9 <= nums[i] <= 2 * 10^9
- 0 <= d <= 10^9
- nums[i] are unique
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        ([-2, 0, 2], "RLL", 3),       # Example 1
        ([1, 0], "RL", 2),             # Example 2
        ([0, 1], "RR", 1),             # Same direction
        ([0, 1], "LL", 1),             # Same direction left
        ([-10, 10], "RL", 5),          # Moving apart
        ([0, 10], "RL", 5),            # Moving toward each other
        ([1, 2, 3], "RRR", 0),         # d = 0
    ]

    for nums, s, d in edge_cases:
        yield f'{json.dumps(nums, separators=(",", ":"))}\n{json.dumps(s)}\n{d}'
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        n = random.randint(2, 20)
        nums = random.sample(range(-1000, 1000), n)
        s = ''.join(random.choice('LR') for _ in range(n))
        d = random.randint(0, 100)
        yield f'{json.dumps(nums, separators=(",", ":"))}\n{json.dumps(s)}\n{d}'


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    n = max(2, min(n, 500))
    nums = random.sample(range(-10000, 10000), n)
    s = ''.join(random.choice('LR') for _ in range(n))
    d = random.randint(0, 100)
    return f'{json.dumps(nums, separators=(",", ":"))}\n{json.dumps(s)}\n{d}'
