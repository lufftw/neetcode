# generators/0035_search_insert_position.py
"""
Test Case Generator for Problem 0035 - Search Insert Position

LeetCode Constraints:
- 1 <= nums.length <= 10^4
- -10^4 <= nums[i] <= 10^4
- nums contains distinct values sorted in ascending order.
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
    Generate random test case inputs for Search Insert Position.

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
        ([1, 3, 5, 6], 5),   # Example 1: target exists
        ([1, 3, 5, 6], 2),   # Example 2: target between elements
        ([1, 3, 5, 6], 7),   # Example 3: target larger than all
        ([1, 3, 5, 6], 0),   # Target smaller than all
        ([1], 0),            # Single element, insert before
        ([1], 1),            # Single element, found
        ([1], 2),            # Single element, insert after
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
    Generate a single test case with a sorted array of distinct values.
    """
    size = random.randint(1, 10000)
    min_val, max_val = -10**4, 10**4

    # Generate sorted distinct values
    nums = sorted(random.sample(range(min_val, max_val + 1), min(size, max_val - min_val + 1)))

    # Random target (may or may not exist)
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
    n = max(1, min(n, 10000))  # Clamp to valid range

    min_val, max_val = -10**4, 10**4
    nums = sorted(random.sample(range(min_val, max_val + 1), min(n, max_val - min_val + 1)))
    target = random.randint(min_val, max_val)

    return f"{json.dumps(nums, separators=(',', ':'))}\n{target}"
