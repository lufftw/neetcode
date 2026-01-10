# generators/0300_longest_increasing_subsequence.py
"""
Test Case Generator for Problem 0300 - Longest Increasing Subsequence

LeetCode Constraints:
- 1 <= nums.length <= 2500
- -10^4 <= nums[i] <= 10^4
"""
import json
import random
import bisect
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Longest Increasing Subsequence."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        [1],  # Single element
        [1, 2, 3, 4, 5],  # Strictly increasing
        [5, 4, 3, 2, 1],  # Strictly decreasing
        [1, 1, 1, 1, 1],  # All same
        [10, 9, 2, 5, 3, 7, 101, 18],  # LeetCode example
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
    n = random.randint(5, 100)
    nums = [random.randint(-10000, 10000) for _ in range(n)]
    return json.dumps(nums)


def _compute_lis(nums: List[int]) -> int:
    """Reference LIS implementation using binary search."""
    tails = []
    for num in nums:
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    return len(tails)


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with n elements for complexity estimation.
    """
    n = max(1, min(n, 2500))
    nums = [random.randint(-10000, 10000) for _ in range(n)]
    return json.dumps(nums)


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        nums = json.loads(test)
        lis_len = _compute_lis(nums)
        print(f"Test {i}: {test[:50]}... LIS={lis_len}")
