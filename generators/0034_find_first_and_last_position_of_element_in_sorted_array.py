# generators/0034_find_first_and_last_position_of_element_in_sorted_array.py
"""
Test Case Generator for Problem 0034 - Find First and Last Position of Element in Sorted Array

LeetCode Constraints:
- 0 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9
- nums is a non-decreasing array.
- -10^9 <= target <= 10^9

Time Complexity: O(log n)
"""
import json
import random
from typing import Iterator, Optional


# ============================================
# Random Test Generation (for functional testing)
# ============================================

def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Find First and Last Position.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input in the same format as .in files
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first (matching LeetCode examples)
    edge_cases = [
        ([5, 7, 7, 8, 8, 10], 8),    # Example 1: target exists with duplicates
        ([5, 7, 7, 8, 8, 10], 6),    # Example 2: target not found
        ([], 0),                      # Example 3: empty array
        ([1], 1),                     # Single element, found
        ([1], 0),                     # Single element, not found
        ([2, 2], 2),                  # All same elements
    ]

    for nums, target in edge_cases:
        yield f"{json.dumps(nums, separators=(',', ':'))}\n{target}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """
    Generate a single test case with a sorted array (may have duplicates).
    """
    size = random.randint(0, 10000)

    if size == 0:
        nums = []
        target = random.randint(-10**6, 10**6)
    else:
        min_val, max_val = -10**6, 10**6

        # Generate sorted array with possible duplicates
        nums = sorted([random.randint(min_val, max_val) for _ in range(size)])

        # Decide if target should exist
        if random.random() < 0.7:  # 70% chance target exists
            target = random.choice(nums)
        else:
            target = random.randint(min_val, max_val)

    return f"{json.dumps(nums, separators=(',', ':'))}\n{target}"


# ============================================
# Complexity Estimation (controlled size)
# ============================================

def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    Args:
        n: Size of nums array

    Returns:
        str: Test input with nums.length = n
    """
    n = max(0, min(n, 100000))  # Clamp to valid range

    if n == 0:
        return f"[]\n0"

    min_val, max_val = -10**6, 10**6
    nums = sorted([random.randint(min_val, max_val) for _ in range(n)])
    target = random.choice(nums)

    return f"{json.dumps(nums, separators=(',', ':'))}\n{target}"
