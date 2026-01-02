# generators/0080_remove_duplicates_from_sorted_array_ii.py
"""
Test Case Generator for Problem 0080 - Remove Duplicates from Sorted Array II

LeetCode Constraints:
- 1 <= nums.length <= 3 * 10^4
- -10^4 <= nums[i] <= 10^4
- nums is sorted in non-decreasing order

Time Complexity: O(n) two pointers
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Remove Duplicates II.
    
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
        [1, 1, 1, 2, 2, 3],              # Classic example
        [0, 0, 1, 1, 1, 1, 2, 3, 3],        # Longer example
        [1, 2, 3],                    # No duplicates
        [1, 1],                      # Two elements
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
    """Generate a single sorted test case."""
    nums = []
    current = random.randint(-1000, 1000)
    
    for _ in range(size):
        nums.append(current)
        # Allow up to 2 duplicates, then increment
        if len(nums) >= 2 and nums[-1] == nums[-2] == current:
            current += random.randint(1, 10)
        elif random.random() < 0.6:  # 60% chance to keep same
            if random.random() < 0.4:  # 40% chance to increment
                current += random.randint(1, 10)
    
    return json.dumps(nums, separators=(",",":"))


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

