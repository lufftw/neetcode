# generators/0078_subsets.py
"""
Test Case Generator for Problem 0078 - Subsets

LeetCode Constraints:
- 1 <= nums.length <= 10
- -10 <= nums[i] <= 10
- All the numbers of nums are unique
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Subsets.
    
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
        [1, 2, 3],      # Classic example
        [0],            # Single element
        [1, 2],         # Two elements
        [1, 2, 3, 4],   # Four elements
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
    """Generate a single random test case with unique integers."""
    if n is None:
        n = random.randint(1, 10)
    nums = list(range(n))  # Use sequential integers for larger n
    return json.dumps(nums, separators=(',', ':'))


# ============================================
# Complexity Estimation (controlled size)
# ============================================

def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Subsets:
    - Input size n is the length of nums array
    - Time complexity is O(n × 2^n)
    - 2^n grows exponentially:
      - n=20: 1,048,576 subsets (~1s)
      - n=22: 4,194,304 subsets (~4s)
      - n=24: 16,777,216 subsets (~15s)

    Note: We use smaller n than typical problems (n=5000) because
    exponential growth makes large n infeasible.

    Args:
        n: Size of nums array (will be scaled down for exponential problems)

    Returns:
        str: Test input with nums.length = scaled_n
    """
    # Scale n for exponential (2^n) complexity
    # n=5000 in other problems -> n=22 for subsets (similar runtime ~2-4s)
    if n >= 5000:
        scaled_n = 22  # ~4M subsets, ~2-4 seconds
    elif n >= 1000:
        scaled_n = 20  # ~1M subsets
    elif n >= 500:
        scaled_n = 18  # ~260K subsets
    else:
        scaled_n = max(1, min(n, 18))

    # Generate distinct integers [0, 1, 2, ..., scaled_n-1]
    nums = list(range(scaled_n))

    return json.dumps(nums, separators=(',', ':'))
