# generators/0283_move_zeroes.py
"""
Test Case Generator for Problem 0283 - Move Zeroes

LeetCode Constraints:
- 1 <= nums.length <= 10^4
- -2^31 <= nums[i] <= 2^31 - 1

Time Complexity: O(n) two pointers
"""
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Move Zeroes.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Space-separated integers
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        "0 1 0 3 12",               # Classic example
        "0",                        # Single zero
        "1 2 3 4 5",                # No zeros
        "0 0 0",                    # All zeros
    ]
    
    for edge in edge_cases:
        yield edge
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        size = random.randint(1, 100)
        zero_prob = random.uniform(0.1, 0.5)  # 10-50% zeros
        yield _generate_case(size, zero_prob)


def _generate_case(size: int, zero_prob: float) -> str:
    """Generate a single test case."""
    nums = []
    for _ in range(size):
        if random.random() < zero_prob:
            nums.append(0)
        else:
            nums.append(random.randint(-1000, 1000))
    return ' '.join(map(str, nums))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.
    
    Args:
        n: Length of nums array
    
    Returns:
        str: Test input with n integers
    """
    n = max(1, n)
    return _generate_case(n, 0.3)  # 30% zeros

