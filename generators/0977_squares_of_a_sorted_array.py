# generators/0977_squares_of_a_sorted_array.py
"""
Test Case Generator for Problem 0977 - Squares of a Sorted Array

LeetCode Constraints:
- 1 <= nums.length <= 10^4
- -10^4 <= nums[i] <= 10^4
- nums is sorted in non-decreasing order

Time Complexity: O(n) merge from ends
"""
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Squares of a Sorted Array.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Space-separated sorted integers (can be negative)
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        "-4 -1 0 3 10",             # Classic example
        "-7 -3 2 3 11",             # Another example
        "-5 -3 -2 -1",              # All negative
        "1 2 3 4",                   # All positive
    ]
    
    for edge in edge_cases:
        yield edge
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        size = random.randint(1, 100)
        yield _generate_case(size)


def _generate_case(size: int) -> str:
    """Generate a single sorted test case (can include negatives)."""
    nums = sorted([random.randint(-1000, 1000) for _ in range(size)])
    return ' '.join(map(str, nums))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.
    
    Args:
        n: Length of nums array
    
    Returns:
        str: Test input with n sorted integers
    """
    n = max(1, n)
    return _generate_case(n)

