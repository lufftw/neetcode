# generators/0136_single_number.py
"""
Test Case Generator for Problem 0136 - Single Number

LeetCode Constraints:
- 1 <= nums.length <= 3 * 10^4
- -3 * 10^4 <= nums[i] <= 3 * 10^4
- Each element appears twice except one
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Single Number."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        [1],  # Single element
        [2, 2, 1],  # Single at end
        [4, 1, 2, 1, 2],  # Single at start
        [1, 2, 1],  # Single in middle
    ]

    for nums in edge_cases:
        yield json.dumps(nums)
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random array with one single number."""
    # Generate n pairs + 1 single
    n_pairs = random.randint(2, 50)
    pairs = [random.randint(-30000, 30000) for _ in range(n_pairs)]

    # Single number must be different from all pairs
    single = random.randint(-30000, 30000)
    while single in pairs:
        single = random.randint(-30000, 30000)

    # Build array: each pair number appears twice, single appears once
    nums = []
    for p in pairs:
        nums.extend([p, p])
    nums.append(single)

    random.shuffle(nums)
    return json.dumps(nums)


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with approximately n elements for complexity estimation.
    """
    n = max(1, min(n, 30000))
    if n == 1:
        return json.dumps([random.randint(-30000, 30000)])

    n_pairs = (n - 1) // 2
    pairs = [random.randint(-30000, 30000) for _ in range(n_pairs)]
    single = random.randint(-30000, 30000)
    while single in pairs:
        single = random.randint(-30000, 30000)

    nums = []
    for p in pairs:
        nums.extend([p, p])
    nums.append(single)
    random.shuffle(nums)

    return json.dumps(nums)


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        nums = json.loads(test)
        print(f"Test {i}: {len(nums)} elements")
