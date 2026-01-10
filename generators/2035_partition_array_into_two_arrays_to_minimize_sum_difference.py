"""
Test Case Generator for Problem 2035 - Partition Array Into Two Arrays to Minimize Sum Difference

LeetCode Constraints:
- 1 <= n <= 15
- nums.length == 2 * n
- -10^7 <= nums[i] <= 10^7
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [3, 9, 7, 3],           # Example 1
        [-36, 36],              # Example 2
        [2, -1, 0, 4, -2, -9],  # Example 3: perfect split
        [1, 1],                 # Smallest case
        [0, 0, 0, 0],           # All zeros
        [1, 2, 3, 4],           # Simple increasing
        [-1, 1, -2, 2],         # Symmetric
        [10000000, -10000000, 10000000, -10000000],  # Large values
    ]

    for case in edge_cases:
        yield json.dumps(case, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        n = random.randint(1, 8)  # Keep small for testing speed
        length = 2 * n

        case_type = random.choice(['small', 'mixed', 'large'])

        if case_type == 'small':
            nums = [random.randint(-100, 100) for _ in range(length)]
        elif case_type == 'mixed':
            nums = [random.randint(-10000, 10000) for _ in range(length)]
        else:
            nums = [random.randint(-10**6, 10**6) for _ in range(length)]

        yield json.dumps(nums, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific n (array length = 2n)."""
    n = max(1, min(n, 15))
    length = 2 * n

    nums = [random.randint(-10**6, 10**6) for _ in range(length)]
    return json.dumps(nums, separators=(',', ':'))


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"--- Test {i} ---")
        print(test)
        print()
