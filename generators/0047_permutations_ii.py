# generators/0047_permutations_ii.py
"""
Test Case Generator for Problem 0047 - Permutations II

LeetCode Constraints:
- 1 <= nums.length <= 8
- -10 <= nums[i] <= 10
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Permutations II.
    
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
        [1, 1, 2],        # Classic with duplicates
        [1, 2, 3],        # No duplicates
        [1, 1, 1],        # All same
        [1, 1, 2, 2],     # Pairs of duplicates
        [0, 0, 0, 0],     # All zeros
    ]
    
    for nums in edge_cases:
        yield json.dumps(nums, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case with possible duplicates."""
    n = random.randint(1, 8)
    nums = [random.randint(-10, 10) for _ in range(n)]
    return json.dumps(nums, separators=(',', ':'))
