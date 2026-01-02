# generators/0027_remove_element.py
"""
Test Case Generator for Problem 0027 - Remove Element

LeetCode Constraints:
- 0 <= nums.length <= 100
- 0 <= nums[i] <= 50
- 0 <= val <= 100

Time Complexity: O(n) two pointers
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Remove Element.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Canonical JSON format - Line 1: nums array, Line 2: val
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases as data structures (nums, val)
    edge_cases = [
        ([3, 2, 2, 3], 3),           # Classic example
        ([0, 1, 2, 2, 3, 0, 4, 2], 2), # Longer example
        ([1], 1),                     # Single element to remove
        ([1, 2, 3], 4),               # Value not in array
        ([], 0),                      # Empty array
    ]
    
    for nums, val in edge_cases:
        yield f"{json.dumps(nums, separators=(',', ':'))}\n{val}"
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        size = random.randint(0, 50)
        val = random.randint(0, 50)
        yield _generate_case(size, val)


def _generate_case(size: int, val: int) -> str:
    """Generate a single test case."""
    nums = [random.randint(0, 50) for _ in range(size)]
    return f"{json.dumps(nums, separators=(',', ':'))}\n{val}"


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.
    
    Args:
        n: Length of nums array
    
    Returns:
        str: Canonical JSON input
    """
    n = max(0, n)
    val = random.randint(0, 50)
    return _generate_case(n, val)
