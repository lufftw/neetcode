# generators/0238_product_of_array_except_self.py
"""
Test Case Generator for Problem 0238 - Product of Array Except Self

LeetCode Constraints:
- 2 <= nums.length <= 10^5
- -30 <= nums[i] <= 30
- The product of any prefix or suffix is guaranteed to fit in 32-bit integer

Time Complexity: O(n) with prefix/suffix products
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Product of Array Except Self.

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
        [1, 2, 3, 4],              # Classic example
        [-1, 1, 0, -3, 3],         # With zero
        [0, 0],                     # Two zeros
        [1, 0],                     # One zero
        [2, 2, 2, 2],              # All same
        [-1, -1, -1, -1],          # All negative same
        [1, -1, 1, -1],            # Alternating signs
        [30, -30, 30],             # Max values
        [1, 1, 1, 1, 1],           # All ones
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
    n = random.randint(2, 1000)
    nums = [random.randint(-30, 30) for _ in range(n)]
    return json.dumps(nums, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size for complexity estimation."""
    nums = [random.randint(-30, 30) for _ in range(n)]
    return json.dumps(nums, separators=(',', ':'))
