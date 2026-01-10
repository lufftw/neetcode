# generators/0704_binary_search.py
"""
Test Case Generator for Problem 0704 - Binary Search

LeetCode Constraints:
- 1 <= nums.length <= 10^4
- -10^4 < nums[i], target < 10^4
- All integers are unique
- nums is sorted in ascending order
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Binary Search."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        ([1], 1),  # Single element, found
        ([1], 0),  # Single element, not found
        ([-1, 0, 3, 5, 9, 12], 9),  # Found in middle
        ([-1, 0, 3, 5, 9, 12], 2),  # Not found
        ([1, 2, 3, 4, 5], 1),  # Found at start
        ([1, 2, 3, 4, 5], 5),  # Found at end
    ]

    for nums, target in edge_cases:
        yield f"{json.dumps(nums)}\n{target}"
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random sorted array and target."""
    n = random.randint(5, 100)
    # Generate unique sorted values
    nums = sorted(random.sample(range(-10000, 10000), n))

    # 50% chance target exists
    if random.random() < 0.5:
        target = random.choice(nums)
    else:
        target = random.randint(-10000, 10000)
        while target in nums:
            target = random.randint(-10000, 10000)

    return f"{json.dumps(nums)}\n{target}"


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with n elements for complexity estimation.
    """
    n = max(1, min(n, 10000))
    nums = sorted(random.sample(range(-100000, 100000), n))
    target = random.choice(nums)
    return f"{json.dumps(nums)}\n{target}"


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        lines = test.split("\n")
        nums = json.loads(lines[0])
        print(f"Test {i}: {len(nums)} elements")
