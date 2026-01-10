# generators/0153_find_minimum_in_rotated_sorted_array.py
"""
Test Case Generator for Problem 0153 - Find Minimum in Rotated Sorted Array

LeetCode Constraints:
- n == nums.length
- 1 <= n <= 5000
- -5000 <= nums[i] <= 5000
- All integers of nums are unique.
- nums is sorted and rotated between 1 and n times.
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Find Minimum in Rotated Sorted Array.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (JSON array)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [3, 4, 5, 1, 2],           # LeetCode example 1
        [4, 5, 6, 7, 0, 1, 2],     # LeetCode example 2
        [11, 13, 15, 17],          # Not rotated (rotated n times)
        [1],                        # Single element
        [2, 1],                     # Two elements rotated
        [1, 2],                     # Two elements not rotated
        [3, 1, 2],                  # Three elements
        [2, 3, 4, 5, 1],            # Rotation at end
        [5, 1, 2, 3, 4],            # Rotation at beginning
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
    """Generate a single random test case."""
    # Random array size
    n = random.randint(1, 100)

    # Generate sorted unique array
    nums = _generate_rotated_sorted_array(n)

    return json.dumps(nums, separators=(',', ':'))


def _generate_rotated_sorted_array(n: int) -> List[int]:
    """Generate a rotated sorted array of size n with unique elements."""
    # Generate n unique values
    start = random.randint(-5000, 5000 - n * 2)
    values = []
    current = start
    for _ in range(n):
        values.append(current)
        current += random.randint(1, 5)

    # Rotate by a random amount (1 to n times)
    k = random.randint(1, n)
    k = k % n  # Normalize
    if k == 0:
        k = n  # Rotate n times = no rotation

    # Rotate: take last k elements and put them at front
    rotated = values[-k:] + values[:-k]
    return rotated


# ============================================
# Complexity Estimation
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Find Minimum in Rotated Sorted Array:
    - n is the array length
    - Binary search is O(log n)

    Args:
        n: Target array size

    Returns:
        str: Test input
    """
    # Clamp to LeetCode constraints
    n = max(1, min(n, 5000))

    nums = _generate_rotated_sorted_array(n)
    return json.dumps(nums, separators=(',', ':'))


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(3, seed=42), 1):
        nums = json.loads(test)
        print(f"Test {i}: {len(nums)} elements, min={min(nums)}")
        print(f"  {nums[:10]}{'...' if len(nums) > 10 else ''}")
        print()
