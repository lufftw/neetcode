# generators/0525_contiguous_array.py
"""
Test Case Generator for Problem 0525 - Contiguous Array

LeetCode Constraints:
- 1 <= nums.length <= 10^5
- nums[i] is either 0 or 1

Time Complexity: O(n) with prefix sum + hash map
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Contiguous Array.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Test input in JSON format (nums)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [0, 1],                    # Simplest balanced
        [0, 1, 0],                 # Answer is 2
        [0, 0, 1, 1],              # Full array balanced
        [1, 1, 1, 0, 0, 0],        # Two halves
        [0],                       # Single 0
        [1],                       # Single 1
        [0, 1, 1, 0, 1, 1, 1, 0],  # Mixed
        [0, 0, 0, 1, 1, 1],        # Two groups balanced
        [1, 0, 1, 0, 1, 0, 1, 0],  # Alternating
    ]

    for nums in edge_cases:
        yield json.dumps(nums, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a single random test case."""
    n = random.randint(1, 5000)
    nums = [random.randint(0, 1) for _ in range(n)]
    return json.dumps(nums, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size for complexity estimation."""
    nums = [random.randint(0, 1) for _ in range(n)]
    return json.dumps(nums, separators=(',', ':'))
