# generators/0217_contains_duplicate.py
"""
Test Case Generator for Problem 0217 - Contains Duplicate

LeetCode Constraints:
- 1 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Contains Duplicate."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        [1, 2, 3, 1],                    # Has duplicate
        [1, 2, 3, 4],                    # No duplicate
        [1, 1, 1, 3, 3, 4, 3, 2, 4, 2],  # Multiple duplicates
        [1],                              # Single element
        [1, 1],                           # Two same
        [1, 2],                           # Two different
    ]

    for nums in edge_cases:
        yield json.dumps(nums, separators=(",", ":"))
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate random array with/without duplicates."""
    n = random.randint(5, 50)

    if random.random() < 0.5:
        # With duplicates: sample fewer unique values than n
        unique_count = random.randint(1, n - 1)
        values = [random.randint(-1000, 1000) for _ in range(unique_count)]
        nums = [random.choice(values) for _ in range(n)]
    else:
        # Without duplicates: all unique
        nums = random.sample(range(-10000, 10001), n)

    return json.dumps(nums, separators=(",", ":"))


def generate_for_complexity(n: int) -> str:
    """Generate test case with array of length n for complexity estimation."""
    n = max(1, min(n, 100000))
    # Generate with duplicates to test worst case
    nums = [random.randint(-n, n) for _ in range(n)]
    return json.dumps(nums, separators=(",", ":"))


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}: {test}")
