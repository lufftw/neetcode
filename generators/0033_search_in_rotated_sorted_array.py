# generators/0033_search_in_rotated_sorted_array.py
"""
Test Case Generator for Problem 0033 - Search in Rotated Sorted Array

LeetCode Constraints:
- 1 <= nums.length <= 5000
- -10^4 <= nums[i] <= 10^4
- All values of nums are unique.
- nums is an ascending array that is possibly rotated.
- -10^4 <= target <= 10^4

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
    Generate random test case inputs for Search in Rotated Sorted Array.

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
        ([4, 5, 6, 7, 0, 1, 2], 0),   # Example 1: target exists
        ([4, 5, 6, 7, 0, 1, 2], 3),   # Example 2: target not found
        ([1], 0),                      # Example 3: single element, not found
        ([1], 1),                      # Single element, found
        ([3, 1], 1),                   # Two elements, rotated
        ([2, 1], 3),                   # Two elements, not found
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
    Generate a single test case with a rotated sorted array.

    Strategy:
    1. Generate a sorted array with unique values
    2. Rotate it at a random pivot
    3. Either pick target from array (found) or pick value not in array (not found)
    """
    size = random.randint(1, 5000)
    min_val, max_val = -10**4, 10**4

    # Generate sorted unique values
    nums = sorted(random.sample(range(min_val, max_val + 1), min(size, max_val - min_val + 1)))

    # Rotate at random pivot (0 means no rotation)
    if len(nums) > 1:
        pivot = random.randint(0, len(nums) - 1)
        nums = nums[pivot:] + nums[:pivot]

    # Decide if target should exist
    if random.random() < 0.7:  # 70% chance target exists
        target = random.choice(nums)
    else:
        # Pick a value not in array
        target = random.randint(min_val, max_val)
        while target in nums:
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
    nums = sorted(random.sample(range(min_val, max_val + 1), min(n, max_val - min_val + 1)))

    # Rotate
    if len(nums) > 1:
        pivot = random.randint(0, len(nums) - 1)
        nums = nums[pivot:] + nums[:pivot]

    target = random.choice(nums)

    return f"{json.dumps(nums, separators=(',', ':'))}\n{target}"
