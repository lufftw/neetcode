# generators/0081_search_in_rotated_sorted_array_ii.py
"""
Test Case Generator for Problem 0081 - Search in Rotated Sorted Array II

LeetCode Constraints:
- 1 <= nums.length <= 5000
- -10^4 <= nums[i] <= 10^4
- nums is guaranteed to be rotated at some pivot.
- -10^4 <= target <= 10^4

Note: nums may contain duplicates (unlike problem 33)

Time Complexity: O(n) worst case, O(log n) average
"""
import json
import random
from typing import Iterator, Optional


# ============================================
# Random Test Generation (for functional testing)
# ============================================

def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Search in Rotated Sorted Array II.

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
        ([2, 5, 6, 0, 0, 1, 2], 0),   # Example 1: target exists
        ([2, 5, 6, 0, 0, 1, 2], 3),   # Example 2: target not found
        ([1, 0, 1, 1, 1], 0),          # Ambiguous case - many duplicates
        ([1, 1, 1, 1, 1, 1, 1], 2),    # All same, target not found
        ([1], 1),                       # Single element, found
        ([1], 0),                       # Single element, not found
        ([2, 2, 2, 0, 1], 0),          # Duplicates with pivot
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
    Generate a single test case with a rotated sorted array (with duplicates).
    """
    size = random.randint(1, 5000)
    min_val, max_val = -10**4, 10**4

    # Generate sorted array with possible duplicates
    nums = sorted([random.randint(min_val, max_val) for _ in range(size)])

    # Rotate at random pivot
    if len(nums) > 1:
        pivot = random.randint(0, len(nums) - 1)
        nums = nums[pivot:] + nums[:pivot]

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
    n = max(1, min(n, 5000))  # Clamp to valid range

    min_val, max_val = -10**4, 10**4
    nums = sorted([random.randint(min_val, max_val) for _ in range(n)])

    if len(nums) > 1:
        pivot = random.randint(0, len(nums) - 1)
        nums = nums[pivot:] + nums[:pivot]

    target = random.choice(nums)

    return f"{json.dumps(nums, separators=(',', ':'))}\n{target}"
