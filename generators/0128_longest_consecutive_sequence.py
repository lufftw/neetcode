# generators/0128_longest_consecutive_sequence.py
"""
Test Case Generator for Problem 0128 - Longest Consecutive Sequence

LeetCode Constraints:
- 0 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Longest Consecutive Sequence."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        [],  # Empty
        [1],  # Single element
        [100, 4, 200, 1, 3, 2],  # LeetCode example
        [0, 3, 7, 2, 5, 8, 4, 6, 0, 1],  # Long sequence
        [1, 2, 0, 1],  # Duplicates
    ]

    for nums in edge_cases:
        yield json.dumps(nums)
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random array."""
    n = random.randint(10, 100)
    nums = [random.randint(-1000, 1000) for _ in range(n)]
    return json.dumps(nums)


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with n elements for complexity estimation.
    """
    n = max(0, min(n, 100000))
    if n == 0:
        return "[]"
    nums = [random.randint(-1000000, 1000000) for _ in range(n)]
    return json.dumps(nums)


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        nums = json.loads(test)
        print(f"Test {i}: {len(nums)} elements")
