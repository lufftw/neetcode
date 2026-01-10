# generators/0031_next_permutation.py
"""
Test Case Generator for Problem 0031 - Next Permutation

LeetCode Constraints:
- 1 <= nums.length <= 100
- 0 <= nums[i] <= 100
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Next Permutation."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        [1, 2, 3],       # Ascending - has next
        [3, 2, 1],       # Descending - wraps to start
        [1, 1, 5],       # Duplicates
        [1],             # Single element
        [1, 2],          # Two elements ascending
        [2, 1],          # Two elements descending
        [1, 5, 1],       # Duplicates in middle
        [1, 3, 2],       # Pivot in middle
    ]

    for nums in edge_cases:
        yield json.dumps(nums, separators=(",", ":"))
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate random permutation array."""
    n = random.randint(3, 20)

    # Generate array with some duplicates allowed
    nums = [random.randint(0, 20) for _ in range(n)]

    return json.dumps(nums, separators=(",", ":"))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with array of length n for complexity estimation.
    """
    n = max(1, min(n, 100))
    nums = [random.randint(0, 100) for _ in range(n)]
    return json.dumps(nums, separators=(",", ":"))


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}: {test}")
