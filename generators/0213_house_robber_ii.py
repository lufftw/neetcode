"""
Test Generator for LeetCode 213: House Robber II
Pattern: DP 1D Linear - Circular Array Decomposition
"""

import json
import random
from typing import Iterator, List, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test cases for House Robber II.

    Constraints:
    - 1 <= nums.length <= 100
    - 0 <= nums[i] <= 1000

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
        [1],                          # Single house
        [1, 2],                       # Two houses (circular = linear)
        [2, 3, 2],                    # Example 1
        [1, 2, 3, 1],                 # Example 2
        [1, 2, 3],                    # Example 3
        [0, 0, 0, 0],                 # All zeros
        [1000] * 5,                   # All same max values
        [100, 1, 100, 1, 100],        # Alternating high/low (even count)
        [100, 1, 100, 1, 100, 1],     # Alternating high/low (odd count)
    ]

    for nums in edge_cases:
        if count <= 0:
            break
        yield json.dumps(nums, separators=(",", ":"))
        count -= 1

    # Random cases
    while count > 0:
        n = random.randint(1, 50)
        nums = [random.randint(0, 1000) for _ in range(n)]
        yield json.dumps(nums, separators=(",", ":"))
        count -= 1


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific size n for complexity estimation.

    Args:
        n: Size of the nums array

    Returns:
        Test case string
    """
    n = max(1, min(n, 100))
    nums = [random.randint(0, 1000) for _ in range(n)]
    return json.dumps(nums, separators=(",", ":"))


if __name__ == "__main__":
    for case in generate(5, seed=42):
        print(case)
