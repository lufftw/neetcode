# generators/0215_kth_largest_element_in_an_array.py
"""
Test Case Generator for Problem 0215 - Kth Largest Element in an Array

LeetCode Constraints:
- 1 <= k <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4

Time Complexity: O(n) average with quickselect, O(n log n) worst case
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Kth Largest Element.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Canonical JSON format - Line 1: nums array, Line 2: k
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases as (nums, k) tuples
    edge_cases = [
        ([3, 2, 1, 5, 6, 4], 2),            # Classic example
        ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4),   # With duplicates
        ([1], 1),                            # Single element
    ]
    
    for nums, k in edge_cases:
        yield f"{json.dumps(nums, separators=(',', ':'))}\n{k}"
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        size = random.randint(1, 100)
        k = random.randint(1, size)
        yield _generate_case(size, k)


def _generate_case(size: int, k: int) -> str:
    """Generate a single test case."""
    nums = [random.randint(-10000, 10000) for _ in range(size)]
    return f"{json.dumps(nums, separators=(',', ':'))}\n{k}"


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.
    
    Args:
        n: Length of nums array
    
    Returns:
        str: Test input with n integers and k = n//2
    """
    n = max(1, n)
    k = n // 2 if n > 1 else 1
    return _generate_case(n, k)
