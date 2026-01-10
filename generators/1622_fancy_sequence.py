"""
Test Case Generator for Problem 1622 - Fancy Sequence

LeetCode Constraints:
- 1 <= val, inc, m <= 100
- 0 <= idx <= 10^5
- At most 10^5 calls total
"""
import json
import random
from typing import Iterator, Optional, List, Tuple


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Fancy Sequence.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (methods and args on separate lines)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # Example from problem
        (
            ["Fancy", "append", "addAll", "append", "multAll", "getIndex",
             "addAll", "append", "multAll", "getIndex", "getIndex", "getIndex"],
            [[], [2], [3], [7], [2], [0], [3], [10], [2], [0], [1], [2]]
        ),
        # Only appends and getIndex
        (
            ["Fancy", "append", "append", "append", "getIndex", "getIndex", "getIndex"],
            [[], [1], [2], [3], [0], [1], [2]]
        ),
        # Only operations, no elements
        (
            ["Fancy", "addAll", "multAll", "getIndex"],
            [[], [5], [10], [0]]
        ),
        # Large multiplications (test modular arithmetic)
        (
            ["Fancy", "append", "multAll", "multAll", "multAll", "getIndex"],
            [[], [1], [100], [100], [100], [0]]
        ),
    ]

    for methods, args in edge_cases:
        yield _format_case(methods, args)
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _format_case(methods: List[str], args: List[List[int]]) -> str:
    """Format a test case as input string."""
    return f"{json.dumps(methods, separators=(',', ':'))}\n{json.dumps(args, separators=(',', ':'))}"


def _generate_random_case() -> str:
    """Generate a single random test case."""
    num_ops = random.randint(10, 100)

    methods = ["Fancy"]
    args = [[]]

    current_length = 0

    for _ in range(num_ops):
        op = random.choices(
            ["append", "addAll", "multAll", "getIndex"],
            weights=[3, 2, 2, 3],
            k=1
        )[0]

        if op == "append":
            val = random.randint(1, 100)
            methods.append("append")
            args.append([val])
            current_length += 1
        elif op == "addAll":
            inc = random.randint(1, 100)
            methods.append("addAll")
            args.append([inc])
        elif op == "multAll":
            m = random.randint(1, 100)
            methods.append("multAll")
            args.append([m])
        elif op == "getIndex":
            # Sometimes query valid index, sometimes invalid
            if current_length > 0 and random.random() < 0.8:
                idx = random.randint(0, current_length - 1)
            else:
                idx = random.randint(0, max(10, current_length + 5))
            methods.append("getIndex")
            args.append([idx])

    return _format_case(methods, args)


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific number of operations.

    Args:
        n: Target number of operations

    Returns:
        str: Test input
    """
    n = max(1, min(n, 100000))

    methods = ["Fancy"]
    args = [[]]

    current_length = 0

    for _ in range(n):
        op = random.choices(
            ["append", "addAll", "multAll", "getIndex"],
            weights=[3, 2, 2, 3],
            k=1
        )[0]

        if op == "append":
            methods.append("append")
            args.append([random.randint(1, 100)])
            current_length += 1
        elif op == "addAll":
            methods.append("addAll")
            args.append([random.randint(1, 100)])
        elif op == "multAll":
            methods.append("multAll")
            args.append([random.randint(1, 100)])
        elif op == "getIndex" and current_length > 0:
            methods.append("getIndex")
            args.append([random.randint(0, current_length - 1)])

    return _format_case(methods, args)


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(3, seed=42), 1):
        print(f"--- Test {i} ---")
        print(test[:200] + "..." if len(test) > 200 else test)
        print()
