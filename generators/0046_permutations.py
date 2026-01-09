# generators/0046_permutations.py
"""
Test Case Generator for Problem 0046 - Permutations

LeetCode Constraints:
- 1 <= nums.length <= 6
- -10 <= nums[i] <= 10
- All the integers of nums are unique
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Permutations.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility
    
    Yields:
        str: Canonical JSON array
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases as lists
    edge_cases = [
        [1],              # Single element
        [1, 2],           # Two elements
        [1, 2, 3],        # Classic example
        [0, -1, 1],       # With negatives
        [1, 2, 3, 4, 5, 6],  # Maximum length
    ]
    
    for nums in edge_cases:
        yield json.dumps(nums, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case(n: Optional[int] = None) -> str:
    """Generate a single random test case with distinct integers."""
    # Random length 1-6 if not specified
    if n is None:
        n = random.randint(1, 6)
    nums = random.sample(range(-10, 11), min(n, 21))  # Cap at available range
    return json.dumps(nums, separators=(',', ':'))


# ============================================
# Complexity Estimation (controlled size)
# ============================================

def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Permutations:
    - Input size n is the length of nums array
    - Time complexity is O(n! × n)
    - n! grows extremely fast:
      - n=8:  40,320 permutations
      - n=9:  362,880 permutations
      - n=10: 3,628,800 permutations
      - n=11: 39,916,800 permutations

    Note: We use much smaller n than typical problems (n=5000) because
    factorial growth makes large n infeasible.

    Args:
        n: Size of nums array (will be scaled down for factorial problems)

    Returns:
        str: Test input with nums.length = scaled_n
    """
    # Scale n for factorial complexity
    # n=5000 in other problems -> n=10 for permutations (similar runtime)
    # This gives meaningful comparison without timeout
    if n >= 5000:
        scaled_n = 10  # ~3.6M permutations, ~1-2 seconds
    elif n >= 1000:
        scaled_n = 9   # ~360K permutations
    elif n >= 500:
        scaled_n = 8   # ~40K permutations
    else:
        scaled_n = max(1, min(n, 8))

    # Generate distinct integers [0, 1, 2, ..., scaled_n-1]
    nums = list(range(scaled_n))

    return json.dumps(nums, separators=(',', ':'))
