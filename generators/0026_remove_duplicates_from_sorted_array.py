# generators/0026_remove_duplicates_from_sorted_array.py
"""
Test Case Generator for Problem 0026 - Remove Duplicates from Sorted Array

LeetCode Constraints:
- 1 <= nums.length <= 3 * 10^4
- -100 <= nums[i] <= 100
- nums is sorted in non-decreasing order

Time Complexity: O(n) two pointers
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Remove Duplicates.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Canonical JSON format (single line array)
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first (as data structures, not strings)
    edge_cases = [
        [1, 1, 2],                      # Classic example
        [0, 0, 1, 1, 1, 2, 2, 3, 3, 4], # Longer example
        [1],                             # Single element
        [1, 2, 3],                       # No duplicates
        [1, 1, 1],                       # All same
    ]
    
    for nums in edge_cases:
        yield json.dumps(nums, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        size = random.randint(1, 100)
        yield _generate_case(size)


def _generate_case(size: int) -> str:
    """Generate a single sorted test case with possible duplicates."""
    nums = []
    current = random.randint(-100, 100)
    
    for _ in range(size):
        nums.append(current)
        if random.random() < 0.7:
            if random.random() < 0.3:
                current += random.randint(0, 5)
    
    return json.dumps(nums, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.
    
    Args:
        n: Length of nums array
    
    Returns:
        str: Canonical JSON array
    """
    n = max(1, n)
    return _generate_case(n)
