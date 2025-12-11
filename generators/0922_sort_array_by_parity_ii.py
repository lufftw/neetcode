# generators/0922_sort_array_by_parity_ii.py
"""
Test Case Generator for Problem 0922 - Sort Array By Parity II

LeetCode Constraints:
- 2 <= nums.length <= 2 * 10^4
- nums.length is even
- Half of the integers in nums are even, and half are odd
- 0 <= nums[i] <= 1000

Time Complexity: O(n) two pointers
"""
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Sort Array By Parity II.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Space-separated integers (half even, half odd)
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        "4 2 5 7",                  # Classic example
        "2 3",                      # Minimum size
        "1 2 3 4",                  # Simple case
    ]
    
    for edge in edge_cases:
        yield edge
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        size = random.choice([2, 4, 6, 8, 10, 20, 50, 100])  # Even sizes
        yield _generate_case(size)


def _generate_case(size: int) -> str:
    """Generate a single test case with half even, half odd."""
    evens = [random.randint(0, 500) * 2 for _ in range(size // 2)]
    odds = [random.randint(0, 500) * 2 + 1 for _ in range(size // 2)]
    nums = evens + odds
    random.shuffle(nums)
    return ' '.join(map(str, nums))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.
    
    Args:
        n: Length of nums array (will be rounded to even)
    
    Returns:
        str: Test input with n integers (half even, half odd)
    """
    n = max(2, n)
    n = n if n % 2 == 0 else n + 1
    return _generate_case(n)

