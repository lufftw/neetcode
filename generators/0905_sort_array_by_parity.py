# generators/0905_sort_array_by_parity.py
"""
Test Case Generator for Problem 0905 - Sort Array By Parity

LeetCode Constraints:
- 1 <= nums.length <= 5000
- 0 <= nums[i] <= 5000

Time Complexity: O(n) two pointers
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Sort Array By Parity.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Space-separated integers
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        [3, 1, 2, 4],                  # Classic example
        [0],                        # Single element
        [1, 3, 5, 7],                  # All odd
        [2, 4, 6, 8],                  # All even
    ]
    
    for edge in edge_cases:
        yield json.dumps(edge, separators=(",",":"))
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        size = random.randint(1, 100)
        yield _generate_case(size)


def _generate_case(size: int) -> str:
    """Generate a single test case."""
    nums = [random.randint(0, 5000) for _ in range(size)]
    return json.dumps(nums, separators=(",",":"))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.
    
    Args:
        n: Length of nums array
    
    Returns:
        str: Test input with n integers
    """
    n = max(1, n)
    return _generate_case(n)

