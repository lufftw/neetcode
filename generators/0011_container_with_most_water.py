# generators/0011_container_with_most_water.py
"""
Test Case Generator for Problem 0011 - Container With Most Water

LeetCode Constraints:
- n == height.length
- 2 <= n <= 10^5
- 0 <= height[i] <= 10^4

Time Complexity: O(n) two pointers
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Container With Most Water.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Canonical JSON array of heights
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases as data structures
    edge_cases = [
        [1, 8, 6, 2, 5, 4, 8, 3, 7],  # Classic example
        [1, 1],                        # Minimum size
        [1, 2, 1],                     # Small case
        [1, 2, 3, 4, 5],               # Increasing
        [5, 4, 3, 2, 1],               # Decreasing
    ]
    
    for heights in edge_cases:
        yield json.dumps(heights, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        size = random.randint(2, 1000)
        yield _generate_case(size)


def _generate_case(size: int) -> str:
    """Generate a single test case."""
    heights = [random.randint(0, 10000) for _ in range(size)]
    return json.dumps(heights, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.
    
    Args:
        n: Number of vertical lines (length of height array)
    
    Returns:
        str: Canonical JSON array
    """
    n = max(2, n)
    return _generate_case(n)
