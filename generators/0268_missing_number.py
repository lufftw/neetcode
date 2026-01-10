# generators/0268_missing_number.py
"""
Test Case Generator for Problem 0268 - Missing Number

LeetCode Constraints:
- n == nums.length
- 1 <= n <= 10^4
- 0 <= nums[i] <= n
- All numbers are unique
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Missing Number."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        [0],  # Missing 1
        [1],  # Missing 0
        [0, 1],  # Missing 2
        [3, 0, 1],  # Missing 2
        [9, 6, 4, 2, 3, 5, 7, 0, 1],  # Missing 8
    ]

    for nums in edge_cases:
        yield json.dumps(nums)
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random array with one missing number."""
    n = random.randint(5, 100)
    # Generate full sequence and remove one
    missing = random.randint(0, n)
    nums = [i for i in range(n + 1) if i != missing]
    random.shuffle(nums)
    return json.dumps(nums)


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with n elements for complexity estimation.
    """
    n = max(1, min(n, 10000))
    missing = random.randint(0, n)
    nums = [i for i in range(n + 1) if i != missing]
    random.shuffle(nums)
    return json.dumps(nums)


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        nums = json.loads(test)
        print(f"Test {i}: {test[:50]}...")
