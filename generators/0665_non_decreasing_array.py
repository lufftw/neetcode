"""
Test Case Generator for Problem 665 - Non-decreasing Array

LeetCode Constraints:
- 1 <= nums.length <= 10^4
- -10^5 <= nums[i] <= 10^5
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        ([4, 2, 3],),                    # Example 1: true (modify 4->1)
        ([4, 2, 1],),                    # Example 2: false (two violations)
        ([1],),                          # Single element
        ([1, 2],),                       # Two elements
        ([2, 1],),                       # Two elements, need fix
        ([1, 2, 3, 4, 5],),              # Already sorted
        ([5, 4, 3, 2, 1],),              # Reversed
        ([1, 4, 2, 3],),                 # Violation in middle, can lower 4
        ([1, 2, 5, 3, 5],),              # Violation in middle, can raise 3
        ([3, 4, 2, 3],),                 # Tricky: 4>2, but 3>2 means can't lower 4
    ]

    for args in edge_cases:
        yield json.dumps(args[0], separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        n = random.randint(3, 50)

        # Generate with different patterns
        pattern = random.choice(['sorted', 'one_violation', 'two_violations', 'random'])

        if pattern == 'sorted':
            nums = sorted([random.randint(-100, 100) for _ in range(n)])
        elif pattern == 'one_violation':
            nums = sorted([random.randint(-100, 100) for _ in range(n)])
            # Introduce one violation
            i = random.randint(0, n - 2)
            nums[i], nums[i + 1] = nums[i + 1] - random.randint(1, 10), nums[i]
        elif pattern == 'two_violations':
            nums = sorted([random.randint(-100, 100) for _ in range(n)])
            # Introduce two violations
            if n >= 4:
                i = random.randint(0, n // 2 - 1)
                j = random.randint(n // 2, n - 2)
                nums[i] = nums[i + 1] + random.randint(1, 10)
                nums[j] = nums[j + 1] + random.randint(1, 10)
        else:
            nums = [random.randint(-100, 100) for _ in range(n)]

        yield json.dumps(nums, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    n = max(1, min(n, 10000))
    # Mostly sorted with one potential violation
    nums = sorted([random.randint(-10000, 10000) for _ in range(n)])
    # Introduce one violation
    if n > 1:
        i = random.randint(0, n - 2)
        nums[i] = nums[i + 1] + random.randint(1, 100)
    return json.dumps(nums, separators=(',', ':'))
