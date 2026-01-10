"""
Test Case Generator for Problem 1909 - Remove One Element to Make Array Strictly Increasing

LeetCode Constraints:
- 2 <= nums.length <= 1000
- 1 <= nums[i] <= 10^9
"""
import json
import random
from typing import Iterator, Optional


def _is_strictly_increasing(nums: list) -> bool:
    """Check if array is strictly increasing."""
    for i in range(len(nums) - 1):
        if nums[i] >= nums[i + 1]:
            return False
    return True


def _can_be_increasing(nums: list) -> bool:
    """Reference check."""
    n = len(nums)
    for skip in range(n):
        remaining = nums[:skip] + nums[skip+1:]
        if _is_strictly_increasing(remaining):
            return True
    return False


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        [1, 2, 10, 5, 7],    # True: remove 10
        [2, 3, 1, 2],        # False: no single removal works
        [1, 1, 1],           # False: equal elements
        [1, 2, 3],           # True: already increasing
        [1, 2],              # True: minimal, already increasing
        [2, 1],              # True: remove either
        [1, 1],              # False: equal elements
        [1, 3, 2, 4, 5],     # True: remove 3 or 2
        [5, 4, 3, 2, 1],     # False: fully decreasing
        [1, 2, 3, 2, 5],     # True: remove second 2
    ]

    for nums in edge_cases:
        yield json.dumps(nums, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        length = random.randint(2, 30)

        if random.random() < 0.4:
            # Generate a strictly increasing array (True case)
            nums = sorted(random.sample(range(1, length * 3), length))
            # Maybe add one violation
            if random.random() < 0.5 and length > 2:
                i = random.randint(0, length - 2)
                nums[i + 1] = nums[i]  # Create violation
        elif random.random() < 0.5:
            # Generate array with single fixable violation
            nums = sorted(random.sample(range(1, length * 3), length))
            i = random.randint(1, length - 2)
            nums[i] = nums[i - 1] + nums[i + 1]  # Insert element out of order
        else:
            # Random array (might be True or False)
            nums = [random.randint(1, 100) for _ in range(length)]

        yield json.dumps(nums, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    n = max(2, min(n, 1000))

    # Strictly increasing with one violation in the middle
    nums = list(range(1, n + 1))
    if n > 2:
        mid = n // 2
        nums[mid] = nums[mid - 1]  # Create violation

    return json.dumps(nums, separators=(',', ':'))
