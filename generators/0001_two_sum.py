# generators/0001_two_sum.py
"""
Test Case Generator for Problem 0001 - Two Sum

LeetCode Constraints:
- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9
- -10^9 <= target <= 10^9
- Only one valid answer exists.

Time Complexity: O(n) with hash map
"""
import random
from typing import Iterator, Optional


# ============================================
# Random Test Generation (for functional testing)
# ============================================

def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Two Sum.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Test input in the same format as .in files
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        "2,7,11,15\n9",           # Classic example
        "3,2,4\n6",               # Answer not using first element
        "3,3\n6",                 # Duplicate values
    ]
    
    for edge in edge_cases:
        yield edge
        count -= 1
        if count <= 0:
            return
    
    # Random cases with random sizes
    for _ in range(count):
        size = random.randint(2, 5000)  # Random size
        yield _generate_case(size)


def _generate_case(size: int) -> str:
    """
    Generate a single test case with guaranteed solution.
    
    Strategy:
    1. Generate random array
    2. Pick two random indices
    3. Set target = nums[i] + nums[j]
    """
    min_val, max_val = -10**6, 10**6
    
    # Generate random array
    nums = [random.randint(min_val, max_val) for _ in range(size)]
    
    # Pick two random indices for the answer
    i, j = random.sample(range(size), 2)
    
    # Calculate target from these two elements
    target = nums[i] + nums[j]
    
    # Format as .in file content
    nums_str = ','.join(map(str, nums))
    return f"{nums_str}\n{target}"


# ============================================
# Complexity Estimation (controlled size)
# ============================================

def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.
    
    For Two Sum:
    - Input size n is the length of nums array
    - Time complexity is O(n) with hash map
    
    Args:
        n: Size of nums array
    
    Returns:
        str: Test input with nums.length = n
    """
    # Ensure n is at least 2
    n = max(2, n)
    return _generate_case(n)
