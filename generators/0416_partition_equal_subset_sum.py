"""
Test Generator for LeetCode 416: Partition Equal Subset Sum
Pattern: DP Knapsack/Subset - 0/1 Knapsack Boolean
"""

import json
import random
from typing import Iterator, List, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test cases for Partition Equal Subset Sum.

    Constraints:
    - 1 <= nums.length <= 200
    - 1 <= nums[i] <= 100

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        Test case strings (one nums array per line)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [1, 5, 11, 5],                # True: [1,5,5] and [11]
        [1, 2, 3, 5],                 # False: total=11, odd
        [1, 2, 5],                    # False: total=8, can't split
        [1, 1],                       # True: [1] and [1]
        [1],                          # False: single element
        [2, 2, 2, 2],                 # True: [2,2] and [2,2]
        [100, 100],                   # True: [100] and [100]
        [1, 1, 1, 1, 1, 1, 1, 1],     # True: split evenly
    ]

    for nums in edge_cases:
        if count <= 0:
            break
        yield json.dumps(nums, separators=(",", ":"))
        count -= 1

    # Random cases
    while count > 0:
        n = random.randint(1, 50)
        nums = [random.randint(1, 100) for _ in range(n)]
        yield json.dumps(nums, separators=(",", ":"))
        count -= 1


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n."""
    n = max(1, min(n, 200))
    nums = [random.randint(1, 100) for _ in range(n)]
    return json.dumps(nums, separators=(",", ":"))


if __name__ == "__main__":
    for case in generate(5, seed=42):
        print(case)
