"""
Test Generator for LeetCode 494: Target Sum
Pattern: DP Knapsack/Subset - 0/1 Knapsack Count with Transformation
"""

import json
import random
from typing import Iterator, List, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test cases for Target Sum.

    Constraints:
    - 1 <= nums.length <= 20
    - 0 <= nums[i] <= 1000
    - 0 <= sum(nums) <= 1000
    - -1000 <= target <= 1000

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        Test case strings (nums on line 1, target on line 2)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        ([1, 1, 1, 1, 1], 3),              # Multiple ways
        ([1], 1),                           # Single element positive
        ([1], -1),                          # Single element negative
        ([0, 0, 0, 0, 0, 1], 1),            # With zeros
        ([1, 2, 1], 0),                     # Target zero
        ([1, 0], 1),                        # With zero
        ([1, 1, 1, 1, 1], 5),               # All positive
        ([2, 2, 2], 2),                     # Some solutions
    ]

    for nums, target in edge_cases:
        if count <= 0:
            break
        yield f"{json.dumps(nums, separators=(',', ':'))}\n{target}"
        count -= 1

    # Random cases
    while count > 0:
        n = random.randint(1, 15)
        nums = [random.randint(0, 50) for _ in range(n)]
        total = sum(nums)
        # Generate target that might be achievable
        target = random.randint(-total, total)
        yield f"{json.dumps(nums, separators=(',', ':'))}\n{target}"
        count -= 1


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n."""
    n = max(1, min(n, 20))
    nums = [random.randint(0, 50) for _ in range(n)]
    target = random.randint(-sum(nums), sum(nums))
    return f"{json.dumps(nums, separators=(',', ':'))}\n{target}"


if __name__ == "__main__":
    for case in generate(5, seed=42):
        print(case)
        print("---")
