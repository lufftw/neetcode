# generators/0496_next_greater_element_i.py
"""
Test Case Generator for Problem 0496 - Next Greater Element I

LeetCode Constraints:
- 1 <= nums1.length <= nums2.length <= 1000
- 0 <= nums1[i], nums2[i] <= 10^4
- All integers in nums1 and nums2 are unique
- All integers of nums1 also appear in nums2

Time Complexity: O(n + m) with monotonic stack and hash map
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Next Greater Element I.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Test input in JSON format (two lines: nums1, nums2)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        ([4, 1, 2], [1, 3, 4, 2]),      # Classic example
        ([2, 4], [1, 2, 3, 4]),          # Second example
        ([1], [1]),                       # Single element
        ([1, 2], [1, 2]),                 # nums1 == nums2
        ([3], [1, 2, 3, 4, 5]),           # One query, multiple elements
    ]

    for nums1, nums2 in edge_cases:
        yield f"{json.dumps(nums1, separators=(',', ':'))}\n{json.dumps(nums2, separators=(',', ':'))}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        nums2_size = random.randint(1, 500)
        nums1_size = random.randint(1, nums2_size)
        yield _generate_case(nums1_size, nums2_size)


def _generate_case(nums1_size: int, nums2_size: int) -> str:
    """Generate a single random test case with valid constraints."""
    # Generate unique nums2
    nums2 = random.sample(range(10001), nums2_size)
    # nums1 is a subset of nums2
    nums1 = random.sample(nums2, nums1_size)

    return f"{json.dumps(nums1, separators=(',', ':'))}\n{json.dumps(nums2, separators=(',', ':'))}"


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific input size for complexity estimation."""
    n = max(1, min(n, 1000))
    return _generate_case(n, n)
