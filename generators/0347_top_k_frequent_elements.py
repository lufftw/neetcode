# generators/0347_top_k_frequent_elements.py
"""
Test Case Generator for Problem 347 - Top K Frequent Elements

LeetCode Constraints:
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4
- k is in the range [1, the number of unique elements in the array]
- It is guaranteed that the answer is unique
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Test input in .in file format (nums on line 1, k on line 2)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        ([1, 1, 1, 2, 2, 3], 2),           # Classic example
        ([1], 1),                            # Single element
        ([1, 2], 2),                         # All elements in result
        ([1, 1, 1, 1], 1),                   # All same element
        ([1, 2, 3, 4, 5], 3),                # All unique, pick 3
        ([1, 1, 2, 2, 3, 3], 2),             # Tie frequencies (answer unique guaranteed)
    ]

    for nums, k in edge_cases:
        yield f"{json.dumps(nums, separators=(',', ':'))}\n{k}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single valid random test case."""
    # Random size
    n = random.randint(10, 500)

    # Create array with controlled frequency distribution
    # Use fewer unique values to ensure some have higher frequency
    unique_count = random.randint(3, min(n // 2, 50))
    values = random.sample(range(-10000, 10001), unique_count)

    # Assign frequencies (ensure some variation)
    nums = []
    for val in values:
        freq = random.randint(1, n // unique_count + 5)
        nums.extend([val] * freq)

    # Trim or pad to target size
    if len(nums) > n:
        nums = random.sample(nums, n)
    elif len(nums) < n:
        nums.extend(random.choices(values, k=n - len(nums)))

    random.shuffle(nums)

    # k is between 1 and unique count
    k = random.randint(1, len(set(nums)))

    return f"{json.dumps(nums, separators=(',', ':'))}\n{k}"


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size for complexity estimation."""
    unique_count = min(n // 10 + 1, 100)
    values = list(range(unique_count))

    nums = []
    for val in values:
        nums.extend([val] * (n // unique_count))

    # Pad to exact size
    while len(nums) < n:
        nums.append(random.choice(values))

    random.shuffle(nums)
    k = random.randint(1, unique_count)

    return f"{json.dumps(nums, separators=(',', ':'))}\n{k}"
