"""
Test Case Generator for Problem 307 - Range Sum Query - Mutable

LeetCode Constraints:
- 1 <= nums.length <= 3 * 10^4
- -100 <= nums[i] <= 100
- 0 <= index < nums.length
- -100 <= val <= 100
- 0 <= left <= right < nums.length
- At most 3 * 10^4 calls will be made to update and sumRange.
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
        str: Test input in .in file format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # Single element
        (["NumArray", "sumRange", "update", "sumRange"],
         [[[1]], [0, 0], [0, 5], [0, 0]]),
        # Two elements
        (["NumArray", "sumRange", "update", "sumRange"],
         [[[1, 2]], [0, 1], [0, 3], [0, 1]]),
        # All same values
        (["NumArray", "sumRange", "update", "sumRange"],
         [[[5, 5, 5, 5]], [0, 3], [2, 10], [0, 3]]),
        # Negative values
        (["NumArray", "sumRange", "update", "sumRange"],
         [[[-1, -2, -3]], [0, 2], [1, 5], [0, 2]]),
    ]

    for ops, args in edge_cases:
        yield f"{json.dumps(ops, separators=(',', ':'))}\n{json.dumps(args, separators=(',', ':'))}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single valid random test case."""
    n = random.randint(5, 100)
    nums = [random.randint(-100, 100) for _ in range(n)]

    num_ops = random.randint(5, 50)
    ops = ["NumArray"]
    args = [[nums]]

    for _ in range(num_ops):
        if random.random() < 0.5:
            # Update
            index = random.randint(0, n - 1)
            val = random.randint(-100, 100)
            ops.append("update")
            args.append([index, val])
        else:
            # sumRange
            left = random.randint(0, n - 1)
            right = random.randint(left, n - 1)
            ops.append("sumRange")
            args.append([left, right])

    return f"{json.dumps(ops, separators=(',', ':'))}\n{json.dumps(args, separators=(',', ':'))}"


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    nums = [random.randint(-100, 100) for _ in range(n)]

    num_ops = n
    ops = ["NumArray"]
    args = [[nums]]

    for _ in range(num_ops):
        if random.random() < 0.5:
            index = random.randint(0, n - 1)
            val = random.randint(-100, 100)
            ops.append("update")
            args.append([index, val])
        else:
            left = random.randint(0, n - 1)
            right = random.randint(left, n - 1)
            ops.append("sumRange")
            args.append([left, right])

    return f"{json.dumps(ops, separators=(',', ':'))}\n{json.dumps(args, separators=(',', ':'))}"
