# generators/0295_find_median_from_data_stream.py
"""
Test Case Generator for Problem 295 - Find Median from Data Stream

LeetCode Constraints:
- -10^5 <= num <= 10^5
- There will be at least one element before findMedian
- At most 5 * 10^4 calls to addNum and findMedian
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
        str: Test input in .in file format (operations on line 1, args on line 2)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # Classic example from problem
        (["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"],
         [[], [1], [2], [], [3], []]),

        # Single element
        (["MedianFinder", "addNum", "findMedian"],
         [[], [5], []]),

        # Two elements (even count)
        (["MedianFinder", "addNum", "addNum", "findMedian"],
         [[], [1], [2], []]),

        # Negative numbers
        (["MedianFinder", "addNum", "addNum", "addNum", "findMedian"],
         [[], [-1], [-2], [-3], []]),

        # Same numbers
        (["MedianFinder", "addNum", "addNum", "addNum", "findMedian"],
         [[], [5], [5], [5], []]),
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
    # Random number of operations
    num_ops = random.randint(5, 100)

    operations = ["MedianFinder"]
    arguments = [[]]

    nums_added = 0

    for _ in range(num_ops):
        if nums_added == 0 or random.random() < 0.7:
            # Add number
            num = random.randint(-100000, 100000)
            operations.append("addNum")
            arguments.append([num])
            nums_added += 1
        else:
            # Find median
            operations.append("findMedian")
            arguments.append([])

    return f"{json.dumps(operations, separators=(',', ':'))}\n{json.dumps(arguments, separators=(',', ':'))}"


def generate_for_complexity(n: int) -> str:
    """Generate test case with n addNum operations."""
    operations = ["MedianFinder"]
    arguments = [[]]

    for i in range(n):
        operations.append("addNum")
        arguments.append([random.randint(-100000, 100000)])

        # Occasionally find median
        if i > 0 and random.random() < 0.1:
            operations.append("findMedian")
            arguments.append([])

    # Final findMedian
    operations.append("findMedian")
    arguments.append([])

    return f"{json.dumps(operations, separators=(',', ':'))}\n{json.dumps(arguments, separators=(',', ':'))}"
