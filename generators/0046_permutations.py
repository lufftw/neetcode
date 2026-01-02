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


def _generate_case() -> str:
    """Generate a single random test case with distinct integers."""
    # Random length 1-6
    n = random.randint(1, 6)
    nums = random.sample(range(-10, 11), n)
    return json.dumps(nums, separators=(',', ':'))
