"""
Test Case Generator for Problem 2029 - Stone Game IX

LeetCode Constraints:
- 1 <= stones.length <= 10^5
- 1 <= stones[i] <= 10^4
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        [2, 1],              # True: min(1,2) > 0 with even zeros
        [2],                 # False: only one stone
        [5, 1, 2, 4, 3],     # False: odd zeros, |cnt1-cnt2| <= 2
        [1, 1, 1, 1, 2, 2],  # True: even zeros, both 1's and 2's
        [3, 3, 3],           # False: only zeros
        [1, 2, 3],           # False: odd zeros, |2-1| <= 2
        [1, 1, 1, 2],        # True: even zeros, min(3,1) > 0
        [1, 1, 1, 1, 1, 2],  # True: even zeros (cnt0=0)
        [3, 1, 1, 1, 1, 2],  # False: odd zeros, |4-1|=3 > 2 -> True!
    ]

    for stones in edge_cases:
        yield json.dumps(stones, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        length = random.randint(1, 50)

        # Generate by controlling remainder distribution
        cnt0 = random.randint(0, length // 3)
        remaining = length - cnt0
        cnt1 = random.randint(0, remaining)
        cnt2 = remaining - cnt1

        stones = []
        for _ in range(cnt0):
            stones.append(random.choice([3, 6, 9, 12, 15]))
        for _ in range(cnt1):
            stones.append(random.choice([1, 4, 7, 10, 13]))
        for _ in range(cnt2):
            stones.append(random.choice([2, 5, 8, 11, 14]))

        random.shuffle(stones)
        if not stones:
            stones = [1]

        yield json.dumps(stones, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    n = max(1, min(n, 10000))

    # Mix of all remainder types
    stones = []
    for i in range(n):
        stones.append(random.randint(1, 10000))

    return json.dumps(stones, separators=(',', ':'))
