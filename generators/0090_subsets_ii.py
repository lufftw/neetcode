# generators/0090_subsets_ii.py
"""
Test Case Generator for Problem 0090 - Subsets II

LeetCode Constraints:
- 1 <= nums.length <= 10
- -10 <= nums[i] <= 10
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Subsets II.
    
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
        "1,2,2",       # Classic with duplicates
        [0],           # Single element
        "1,1,1",       # All same
        "1,2,2,3,3",   # Multiple duplicate groups
    ]
    
    for edge in edge_cases:
        yield json.dumps(edge, separators=(",",":"))
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case with possible duplicates."""
    # Random length 1-10
    n = random.randint(1, 10)
    
    # Generate integers with possible duplicates
    nums = [random.randint(-10, 10) for _ in range(n)]
    
    return json.dumps(nums, separators=(",",":"))

