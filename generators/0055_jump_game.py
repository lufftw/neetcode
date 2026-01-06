"""
Test Case Generator for Problem 55 - Jump Game

LeetCode Constraints:
- 1 <= nums.length <= 10^4
- 0 <= nums[i] <= 10^5
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
        [0],  # Single element, trivially true
        [1],  # Single element
        [2, 3, 1, 1, 4],  # Classic reachable example
        [3, 2, 1, 0, 4],  # Classic unreachable example
        [0, 1],  # Stuck at first position
        [1, 0, 1],  # Can't reach last
        [2, 0, 0],  # Just barely reach
        [1, 1, 1, 1],  # All ones
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
    n = random.randint(1, 1000)

    # Mix of reachable and unreachable cases
    if random.random() < 0.7:
        # Generate reachable case (higher jump values)
        nums = [random.randint(1, min(n, 100)) for _ in range(n)]
    else:
        # Generate potentially unreachable case (include zeros)
        nums = []
        for i in range(n):
            if random.random() < 0.3:
                nums.append(0)
            else:
                nums.append(random.randint(0, 5))

    return json.dumps(nums, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size for complexity estimation."""
    # Generate a reachable case for timing
    nums = [random.randint(1, min(n, 100)) for _ in range(n)]
    return json.dumps(nums, separators=(',', ':'))
