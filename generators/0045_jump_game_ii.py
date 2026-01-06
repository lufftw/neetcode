"""
Test Case Generator for Problem 45 - Jump Game II

LeetCode Constraints:
- 1 <= nums.length <= 10^4
- 0 <= nums[i] <= 1000
- It's guaranteed that you can reach nums[n - 1]
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs (guaranteed reachable).

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
        [0],  # Single element, 0 jumps needed
        [1, 0],  # Two elements, 1 jump
        [2, 3, 1, 1, 4],  # Classic example, answer = 2
        [2, 3, 0, 1, 4],  # Another example, answer = 2
        [1, 1, 1, 1],  # All ones, n-1 jumps
        [5, 4, 3, 2, 1, 0],  # Can jump to end from start
        [1, 2, 3],  # Increasing jumps
    ]

    for nums in edge_cases:
        yield json.dumps(nums, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases (guaranteed reachable)
    for _ in range(count):
        yield _generate_reachable_case()


def _generate_reachable_case() -> str:
    """Generate a single reachable test case."""
    n = random.randint(1, 1000)

    # Generate case that's guaranteed to be reachable
    # Strategy: ensure at least one path exists
    nums = [0] * n
    pos = 0
    while pos < n - 1:
        # Determine jump range
        max_jump = min(random.randint(1, 100), n - 1 - pos)
        nums[pos] = max_jump

        # Move forward
        jump = random.randint(1, max_jump)
        pos += jump

    # Fill remaining positions with random values
    for i in range(n):
        if nums[i] == 0 and i < n - 1:
            nums[i] = random.randint(1, min(100, n - 1 - i))

    return json.dumps(nums, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size for complexity estimation."""
    # Generate a reachable case
    nums = []
    for i in range(n):
        if i == n - 1:
            nums.append(0)
        else:
            nums.append(random.randint(1, min(100, n - 1 - i)))
    return json.dumps(nums, separators=(',', ':'))
