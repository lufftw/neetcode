# generators/0155_min_stack.py
"""
Test Case Generator for Problem 0155 - Min Stack

LeetCode Constraints:
- -2^31 <= val <= 2^31 - 1
- Methods pop, top and getMin will always be called on non-empty stacks
- At most 3 * 10^4 calls to push, pop, top, and getMin
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Min Stack."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        # Simple operations
        (
            ["MinStack", "push", "push", "push", "getMin", "pop", "top", "getMin"],
            [[], [-2], [0], [-3], [], [], [], []],
        ),
        # Decreasing values
        (
            ["MinStack", "push", "push", "push", "getMin"],
            [[], [3], [2], [1], []],
        ),
        # Increasing values
        (
            ["MinStack", "push", "push", "push", "getMin"],
            [[], [1], [2], [3], []],
        ),
    ]

    for ops, args in edge_cases:
        yield f"{json.dumps(ops)}\n{json.dumps(args)}"
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random sequence of valid operations."""
    num_ops = random.randint(10, 50)

    operations = ["MinStack"]
    arguments = [[]]

    stack_size = 0

    for _ in range(num_ops):
        # Choose operation based on current stack state
        if stack_size == 0:
            # Must push when empty
            op = "push"
        else:
            # Random operation
            op = random.choice(["push", "push", "pop", "top", "getMin"])

        if op == "push":
            val = random.randint(-1000, 1000)
            operations.append("push")
            arguments.append([val])
            stack_size += 1
        elif op == "pop":
            operations.append("pop")
            arguments.append([])
            stack_size -= 1
        elif op == "top":
            operations.append("top")
            arguments.append([])
        elif op == "getMin":
            operations.append("getMin")
            arguments.append([])

    return f"{json.dumps(operations)}\n{json.dumps(arguments)}"


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with approximately n operations for complexity estimation.
    """
    n = max(1, min(n, 30000))

    operations = ["MinStack"]
    arguments = [[]]

    stack_size = 0

    for _ in range(n):
        if stack_size == 0:
            op = "push"
        else:
            op = random.choice(["push", "push", "pop", "top", "getMin"])

        if op == "push":
            val = random.randint(-1000, 1000)
            operations.append("push")
            arguments.append([val])
            stack_size += 1
        elif op == "pop":
            operations.append("pop")
            arguments.append([])
            stack_size -= 1
        elif op == "top":
            operations.append("top")
            arguments.append([])
        elif op == "getMin":
            operations.append("getMin")
            arguments.append([])

    return f"{json.dumps(operations)}\n{json.dumps(arguments)}"


if __name__ == "__main__":
    for i, test in enumerate(generate(3, seed=42), 1):
        lines = test.split("\n")
        ops = json.loads(lines[0])
        print(f"Test {i}: {len(ops)} operations")
