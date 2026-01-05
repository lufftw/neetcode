# generators/0162_find_peak_element.py
"""
Test Case Generator for Problem 0162 - Find Peak Element

LeetCode Constraints:
- 1 <= nums.length <= 1000
- -2^31 <= nums[i] <= 2^31 - 1
- nums[i] != nums[i + 1] for all valid i.

Note: Adjacent elements are never equal, guaranteeing at least one peak exists.

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
    Generate random test case inputs for Find Peak Element.

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
        [1, 2, 3, 1],             # Example 1: peak in middle
        [1, 2, 1, 3, 5, 6, 4],    # Example 2: multiple peaks
        [1],                       # Single element (is a peak)
        [1, 2],                    # Two elements, peak at end
        [2, 1],                    # Two elements, peak at start
        [1, 2, 3, 4, 5],          # Strictly increasing (peak at end)
        [5, 4, 3, 2, 1],          # Strictly decreasing (peak at start)
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
    """
    Generate a single test case where adjacent elements are never equal.
    """
    size = random.randint(1, 1000)
    min_val, max_val = -10**6, 10**6

    if size == 1:
        return json.dumps([random.randint(min_val, max_val)], separators=(',', ':'))

    # Generate array with no adjacent duplicates
    nums = [random.randint(min_val, max_val)]
    for _ in range(size - 1):
        next_val = random.randint(min_val, max_val)
        # Ensure no adjacent duplicates
        while next_val == nums[-1]:
            next_val = random.randint(min_val, max_val)
        nums.append(next_val)

    return json.dumps(nums, separators=(',', ':'))


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
    n = max(1, min(n, 1000))  # Clamp to valid range

    min_val, max_val = -10**6, 10**6

    if n == 1:
        return json.dumps([random.randint(min_val, max_val)], separators=(',', ':'))

    nums = [random.randint(min_val, max_val)]
    for _ in range(n - 1):
        next_val = random.randint(min_val, max_val)
        while next_val == nums[-1]:
            next_val = random.randint(min_val, max_val)
        nums.append(next_val)

    return json.dumps(nums, separators=(',', ':'))
