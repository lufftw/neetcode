# generators/0047_permutations_ii.py
"""
Test Case Generator for Problem 0047 - Permutations II

LeetCode Constraints:
- 1 <= nums.length <= 8
- -10 <= nums[i] <= 10
"""
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Permutations II.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility
    
    Yields:
        str: Test input in the format: nums (comma-separated)
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        "1,1,2",           # Classic with duplicates
        "1,2,3",           # No duplicates
        "1,1,1",           # All same
        "1,1,2,2",         # Pairs of duplicates
        "0,0,0,0",         # All zeros
    ]
    
    for edge in edge_cases:
        yield edge
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case with possible duplicates."""
    # Random length 1-8
    n = random.randint(1, 8)
    
    # Generate integers with possible duplicates
    nums = [random.randint(-10, 10) for _ in range(n)]
    
    return ','.join(map(str, nums))

