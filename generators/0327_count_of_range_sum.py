"""
Test Case Generator for Problem 327 - Count of Range Sum

LeetCode Constraints:
- 1 <= nums.length <= 10^5
- -2^31 <= nums[i] <= 2^31 - 1
- -10^5 <= lower <= upper <= 10^5
- The answer is guaranteed to fit in a 32-bit integer.
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
        ([-2, 5, -1], -2, 2),          # Classic example
        ([0], 0, 0),                    # Single element, exact match
        ([1], 0, 0),                    # Single element, no match
        ([1, 2, 3], 3, 6),              # Multiple valid ranges
        ([-1, -1, -1], -3, -1),         # All negative
        ([0, 0, 0], 0, 0),              # All zeros
        ([1, -1, 1, -1], 0, 0),         # Alternating
        ([100, -100], -100, 100),       # Wide range
    ]

    for nums, lower, upper in edge_cases:
        yield f"{json.dumps(nums, separators=(',', ':'))}\n{lower}\n{upper}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single valid random test case."""
    n = random.randint(5, 200)
    # Use smaller values to keep prefix sums manageable
    nums = [random.randint(-1000, 1000) for _ in range(n)]

    # Generate reasonable lower/upper bounds
    lower = random.randint(-10000, 0)
    upper = random.randint(lower, 10000)

    return f"{json.dumps(nums, separators=(',', ':'))}\n{lower}\n{upper}"


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    nums = [random.randint(-100, 100) for _ in range(n)]
    lower = random.randint(-1000, 0)
    upper = random.randint(lower, 1000)
    return f"{json.dumps(nums, separators=(',', ':'))}\n{lower}\n{upper}"
