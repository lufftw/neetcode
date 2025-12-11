# generators/0088_merge_sorted_array.py
"""
Test Case Generator for Problem 0088 - Merge Sorted Array

LeetCode Constraints:
- nums1.length == m + n
- nums2.length == n
- 0 <= m, n <= 200
- 1 <= m + n <= 200
- -10^9 <= nums1[i], nums2[i] <= 10^9
- nums1 and nums2 are sorted in non-decreasing order

Time Complexity: O(m + n) merge from end
"""
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Merge Sorted Array.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Line 1: nums1 with trailing zeros, Line 2: m, Line 3: nums2, Line 4: n
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        "1 2 3 0 0 0\n3\n2 5 6\n3",  # Classic example
        "1\n1\n\n0",                  # nums2 empty
        "0\n0\n1\n1",                 # nums1 empty
    ]
    
    for edge in edge_cases:
        yield edge
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        m = random.randint(0, 50)
        n = random.randint(0, 50)
        yield _generate_case(m, n)


def _generate_case(m: int, n: int) -> str:
    """Generate a single test case."""
    nums1_actual = sorted([random.randint(-1000, 1000) for _ in range(m)])
    nums2 = sorted([random.randint(-1000, 1000) for _ in range(n)])
    
    # nums1 has m + n length, with trailing zeros
    nums1 = nums1_actual + [0] * n
    
    nums1_str = ' '.join(map(str, nums1))
    nums2_str = ' '.join(map(str, nums2)) if nums2 else ''
    
    return f"{nums1_str}\n{m}\n{nums2_str}\n{n}"


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.
    
    Args:
        n: Total size m + n (split roughly in half)
    
    Returns:
        str: Test input
    """
    n = max(1, n)
    m = n // 2
    n2 = n - m
    return _generate_case(m, n2)

