"""
Test Case Generator for Problem 2069 - Walking Robot Simulation II

LeetCode Constraints:
- 2 <= width, height <= 100
- 1 <= num <= 10^5
- At most 10^4 calls
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        # Example 1 from problem
        (
            ["Robot", "step", "step", "getPos", "getDir", "step", "step", "step", "getPos", "getDir"],
            [[6, 3], [2], [2], [], [], [2], [1], [4], [], []]
        ),
        # Simple 2x2 grid
        (
            ["Robot", "step", "getPos", "getDir"],
            [[2, 2], [4], [], []]
        ),
        # Large steps (full perimeter)
        (
            ["Robot", "step", "getPos", "getDir"],
            [[5, 5], [16], [], []]  # perimeter = 16
        ),
        # Origin check after moving
        (
            ["Robot", "step", "getPos", "getDir"],
            [[3, 3], [8], [], []]  # perimeter = 8, back to origin
        ),
    ]

    for methods, args in edge_cases:
        yield f"{json.dumps(methods, separators=(',', ':'))}\n{json.dumps(args, separators=(',', ':'))}"
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        width = random.randint(2, 20)
        height = random.randint(2, 20)

        methods = ["Robot"]
        args = [[width, height]]

        # Generate random operations
        num_ops = random.randint(5, 30)
        for _ in range(num_ops):
            op = random.choice(["step", "getPos", "getDir"])
            methods.append(op)
            if op == "step":
                args.append([random.randint(1, 1000)])
            else:
                args.append([])

        yield f"{json.dumps(methods, separators=(',', ':'))}\n{json.dumps(args, separators=(',', ':'))}"


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    n = max(5, min(n, 10000))
    width = random.randint(2, 100)
    height = random.randint(2, 100)

    methods = ["Robot"]
    args = [[width, height]]

    for _ in range(n):
        op = random.choice(["step", "getPos", "getDir"])
        methods.append(op)
        if op == "step":
            args.append([random.randint(1, 100000)])
        else:
            args.append([])

    return f"{json.dumps(methods, separators=(',', ':'))}\n{json.dumps(args, separators=(',', ':'))}"
