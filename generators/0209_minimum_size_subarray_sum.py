# generators/0209_minimum_size_subarray_sum.py
"""
Test Case Generator for Problem 0209 - Minimum Size Subarray Sum

LeetCode Constraints:
- 1 <= target <= 10^9
- 1 <= nums.length <= 10^5
- 1 <= nums[i] <= 10^4

Time Complexity: O(n) sliding window
"""
import random
from typing import Iterator, Optional, List


# ============================================================================
# Random Test Generation (for functional testing)
# ============================================================================

def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Minimum Size Subarray Sum.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Test input (two lines: target and space-separated nums)
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        (7, [2, 3, 1, 2, 4, 3]),      # Classic example, answer = 2
        (4, [1, 4, 4]),                # Single element >= target
        (11, [1, 1, 1, 1, 1, 1, 1, 1]), # No valid subarray
        (15, [1, 2, 3, 4, 5]),         # Entire array
        (6, [10, 2, 3]),               # First element
        (100, [1, 2, 3, 4, 5]),        # No valid subarray
        (3, [1, 1, 1, 1, 1, 1, 1]),    # Multiple windows of same size
        (1, [1]),                       # Single element exact match
    ]
    
    for target, nums in edge_cases:
        nums_str = ' '.join(map(str, nums))
        yield f"{target}\n{nums_str}"
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        n = random.randint(5, 200)
        nums = [random.randint(1, 100) for _ in range(n)]
        
        total = sum(nums)
        # Target should sometimes be achievable, sometimes not
        if random.random() < 0.8:
            target = random.randint(1, total)
        else:
            target = total + random.randint(1, 100)
        
        nums_str = ' '.join(map(str, nums))
        yield f"{target}\n{nums_str}"


# ============================================================================
# Complexity Estimation (controlled size)
# ============================================================================

def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.
    
    For this problem:
    - Input size n is the length of nums array
    
    Args:
        n: Length of the nums array
    
    Returns:
        str: Two lines (target and space-separated nums)
    """
    n = max(1, n)
    nums = [random.randint(1, 100) for _ in range(n)]
    
    # Set target to roughly half of total to ensure sliding window behavior
    total = sum(nums)
    target = max(1, total // 2)
    
    nums_str = ' '.join(map(str, nums))
    return f"{target}\n{nums_str}"

