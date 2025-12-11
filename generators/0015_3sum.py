# generators/0015_3sum.py
"""
Test Case Generator for Problem 0015 - 3Sum

LeetCode Constraints:
- 3 <= nums.length <= 3000
- -10^5 <= nums[i] <= 10^5

Time Complexity: O(n²) sort + two pointers
"""
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for 3Sum.
    
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
        "-1 0 1 2 -1 -4",          # Classic example
        "0 1 1",                     # No solution
        "0 0 0",                     # All zeros
        "-1 0 1",                    # Simple solution
    ]
    
    for edge in edge_cases:
        yield edge
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        size = random.randint(3, 100)
        yield _generate_case(size)


def _generate_case(size: int) -> str:
    """Generate a single test case."""
    nums = [random.randint(-10000, 10000) for _ in range(size)]
    return ' '.join(map(str, nums))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.
    
    Args:
        n: Length of nums array
    
    Returns:
        str: Test input with n integers
    """
    n = max(3, n)
    return _generate_case(n)

