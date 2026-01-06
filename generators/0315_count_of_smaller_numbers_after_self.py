"""
Test Case Generator for Problem 315 - Count of Smaller Numbers After Self

LeetCode Constraints:
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Test input in .in file format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [5, 2, 6, 1],          # Classic example
        [-1],                   # Single element
        [-1, -1],               # Two same elements
        [1, 2, 3, 4, 5],        # Sorted ascending - all zeros except first
        [5, 4, 3, 2, 1],        # Sorted descending - maximum inversions
        [1, 1, 1, 1],           # All same
        [-10000, 10000],        # Min/max values
        [0, 0, 0],              # All zeros
    ]

    for nums in edge_cases:
        yield json.dumps(nums, separators=(",", ":"))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single valid random test case."""
    n = random.randint(5, 500)
    nums = [random.randint(-10000, 10000) for _ in range(n)]
    return json.dumps(nums, separators=(",", ":"))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    nums = [random.randint(-10000, 10000) for _ in range(n)]
    return json.dumps(nums, separators=(",", ":"))
