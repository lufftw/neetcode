"""
Test Generator for LeetCode 1979: Find GCD of Array
Pattern: Math / Number Theory - GCD
"""

import json
import random
from typing import Iterator, List, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test cases for Find GCD of Array.

    Constraints:
    - 2 <= nums.length <= 1000
    - 1 <= nums[i] <= 1000
    """
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        [2, 5, 6, 9, 10],             # GCD(2,10) = 2
        [7, 5, 6, 8, 3],              # GCD(3,8) = 1
        [3, 3],                        # Same values
        [1, 1000],                     # Min and max
        [12, 4, 8, 16, 24],           # All divisible by 4
        [7, 14, 21, 28],              # All divisible by 7
        [1, 2, 3, 4, 5],              # Contains 1
    ]

    for nums in edge_cases:
        if count <= 0:
            break
        yield json.dumps(nums, separators=(",", ":"))
        count -= 1

    while count > 0:
        n = random.randint(2, 50)
        nums = [random.randint(1, 1000) for _ in range(n)]
        yield json.dumps(nums, separators=(",", ":"))
        count -= 1


def generate_for_complexity(n: int) -> str:
    nums = [random.randint(1, 1000) for _ in range(max(2, min(n, 1000)))]
    return json.dumps(nums, separators=(",", ":"))


if __name__ == "__main__":
    for case in generate(5, seed=42):
        print(case)
