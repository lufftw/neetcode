# generators/0321_create_maximum_number.py
"""
Test Case Generator for Problem 0321 - Create Maximum Number

LeetCode Constraints:
- m == nums1.length
- n == nums2.length
- 1 <= m, n <= 500
- 0 <= nums1[i], nums2[i] <= 9
- 1 <= k <= m + n

Time Complexity: O(k^2 * (m + n)) with greedy split and merge
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Create Maximum Number.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Test input (nums1, nums2, k on separate lines)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first (nums1, nums2, k)
    edge_cases = [
        ([3, 4, 6, 5], [9, 1, 2, 5, 8, 3], 5),  # Classic example
        ([6, 7], [6, 0, 4], 5),                  # Second example
        ([3, 9], [8, 9], 3),                     # Third example
        ([1], [1], 2),                           # Minimal
        ([9, 9, 9], [9, 9, 9], 3),               # All same
        ([1, 2, 3], [4, 5, 6], 6),               # Merge all
        ([9], [1, 2, 3, 4, 5], 3),               # One short array
    ]

    for nums1, nums2, k in edge_cases:
        yield f"{json.dumps(nums1, separators=(',', ':'))}\n{json.dumps(nums2, separators=(',', ':'))}\n{k}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        m = random.randint(1, 200)
        n = random.randint(1, 200)
        k = random.randint(1, m + n)
        yield _generate_case(m, n, k)


def _generate_case(m: int, n: int, k: int) -> str:
    """Generate a single random test case."""
    nums1 = [random.randint(0, 9) for _ in range(m)]
    nums2 = [random.randint(0, 9) for _ in range(n)]
    return f"{json.dumps(nums1, separators=(',', ':'))}\n{json.dumps(nums2, separators=(',', ':'))}\n{k}"


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific input size for complexity estimation."""
    n = max(2, n)
    half = n // 2
    k = random.randint(1, n)
    return _generate_case(half, n - half, k)
