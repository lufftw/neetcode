# generators/0016_3sum_closest.py
"""
Test Case Generator for Problem 0016 - 3Sum Closest

LeetCode Constraints:
- 3 <= nums.length <= 1000
- -1000 <= nums[i] <= 1000
- -10^4 <= target <= 10^4

Time Complexity: O(n²) sort + two pointers
"""
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for 3Sum Closest.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Line 1: space-separated integers, Line 2: target
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        "-1 2 1 -4\n1",             # Classic example
        "0 0 0\n1",                  # All zeros
        "1 1 1 0\n-100",            # Large target
    ]
    
    for edge in edge_cases:
        yield edge
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        size = random.randint(3, 100)
        target = random.randint(-10000, 10000)
        yield _generate_case(size, target)


def _generate_case(size: int, target: int) -> str:
    """Generate a single test case."""
    nums = [random.randint(-1000, 1000) for _ in range(size)]
    nums_str = ' '.join(map(str, nums))
    return f"{nums_str}\n{target}"


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.
    
    Args:
        n: Length of nums array
    
    Returns:
        str: Test input with n integers and a random target
    """
    n = max(3, n)
    target = random.randint(-10000, 10000)
    return _generate_case(n, target)

