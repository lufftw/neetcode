# generators/0026_remove_duplicates_from_sorted_array.py
"""
Test Case Generator for Problem 0026 - Remove Duplicates from Sorted Array

LeetCode Constraints:
- 1 <= nums.length <= 3 * 10^4
- -100 <= nums[i] <= 100
- nums is sorted in non-decreasing order

Time Complexity: O(n) two pointers
"""
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Remove Duplicates.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Space-separated sorted integers
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        "1 1 2",                    # Classic example
        "0 0 1 1 1 2 2 3 3 4",     # Longer example
        "1",                        # Single element
        "1 2 3",                    # No duplicates
        "1 1 1",                    # All same
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
    """Generate a single sorted test case with possible duplicates."""
    # Generate sorted array with duplicates
    nums = []
    current = random.randint(-100, 100)
    
    for _ in range(size):
        nums.append(current)
        # Randomly decide to increment or keep same
        if random.random() < 0.7:  # 70% chance to keep same (create duplicates)
            if random.random() < 0.3:  # 30% chance to increment
                current += random.randint(0, 5)
    
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

