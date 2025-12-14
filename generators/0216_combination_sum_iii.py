# generators/0216_combination_sum_iii.py
"""
Test Case Generator for Problem 0216 - Combination Sum III

LeetCode Constraints:
- 2 <= k <= 9
- 1 <= n <= 60
"""
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Combination Sum III.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility
    
    Yields:
        str: Test input in the format: k\\nn
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        "3\n7",    # Classic example (1+2+4=7)
        "3\n9",    # Multiple solutions
        "4\n1",    # Impossible (min sum with 4 nums is 1+2+3+4=10)
        "2\n18",   # 9+9 not allowed (unique), but 9+8=17
        "9\n45",   # Maximum possible (1+2+...+9=45)
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
    """Generate a single random test case."""
    k = random.randint(2, 9)
    # n should be reasonable for k numbers from 1-9
    # Min sum with k nums: 1+2+...+k = k*(k+1)/2
    # Max sum with k nums: (10-k)+...+9 = (9+10-k)*k/2
    min_sum = k * (k + 1) // 2
    max_sum = (19 - k) * k // 2
    
    n = random.randint(min_sum, min(60, max_sum))
    
    return f"{k}\n{n}"

