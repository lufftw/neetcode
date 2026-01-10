# generators/0703_kth_largest_element_in_a_stream.py
"""
Test Case Generator for Problem 0703 - Kth Largest Element in a Stream

LeetCode Constraints:
- 1 <= k <= 10^4
- 0 <= nums.length <= 10^4
- -10^4 <= nums[i] <= 10^4
- -10^4 <= val <= 10^4
- At most 10^4 calls to add
- k <= nums.length + number of add calls
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Kth Largest Element in a Stream."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        # k=1, single element
        (["KthLargest", "add"], [[1, [1]], [2]]),
        # k=2, empty initial
        (["KthLargest", "add", "add"], [[2, []], [1], [2]]),
        # k equals initial length
        (["KthLargest", "add"], [[3, [1, 2, 3]], [0]]),
    ]

    for ops, args in edge_cases:
        yield f"{json.dumps(ops)}\n{json.dumps(args)}"
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random test case."""
    num_adds = random.randint(3, 20)
    initial_len = random.randint(0, 10)
    k = random.randint(1, initial_len + num_adds)

    # Initial array
    nums = [random.randint(-1000, 1000) for _ in range(initial_len)]

    # Build operations
    operations: List[str] = ["KthLargest"]
    arguments: List[List[int]] = [[k, nums]]

    for _ in range(num_adds):
        operations.append("add")
        arguments.append([random.randint(-1000, 1000)])

    return f"{json.dumps(operations)}\n{json.dumps(arguments)}"


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with n add operations for complexity estimation.

    The heap approach should show O(n log k) behavior.
    The sorted list approach should show O(n^2) behavior.
    """
    n = max(1, min(n, 10000))
    k = max(1, n // 2)  # k = n/2 to stress heap operations

    # Start with empty array, then add n elements
    operations: List[str] = ["KthLargest"]
    arguments: List[List[int]] = [[k, []]]

    for i in range(n):
        operations.append("add")
        arguments.append([random.randint(-10000, 10000)])

    return f"{json.dumps(operations)}\n{json.dumps(arguments)}"


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}:")
        print(test)
        print()
