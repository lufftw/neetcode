# generators/0075_sort_colors.py
"""
Test Case Generator for Problem 0075 - Sort Colors

LeetCode Constraints:
- n == nums.length
- 1 <= n <= 300
- nums[i] is 0, 1, or 2

Time Complexity: O(n) Dutch National Flag
"""
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Sort Colors.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Space-separated integers (0, 1, or 2)
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        "2 0 2 1 1 0",              # Classic example
        "2 0 1",                    # Small case
        "0",                        # Single element
        "1 1 1",                    # All same
        "0 1 2",                    # Already sorted
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
    """Generate a single test case."""
    nums = [random.choice([0, 1, 2]) for _ in range(size)]
    return ' '.join(map(str, nums))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.
    
    Args:
        n: Length of nums array
    
    Returns:
        str: Test input with n integers (0, 1, or 2)
    """
    n = max(1, n)
    return _generate_case(n)

