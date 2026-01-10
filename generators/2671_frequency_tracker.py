"""
Generator for 2671 - Frequency Tracker

Generates test cases with:
- Various operation sequences
- Add, deleteOne, hasFrequency operations
"""

import random
from typing import Iterator, Optional
import json


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Frequency Tracker."""
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # Only adds
        (["FrequencyTracker", "add", "add", "add", "hasFrequency"],
         [[], [1], [1], [1], [3]]),
        # Delete non-existent
        (["FrequencyTracker", "deleteOne", "hasFrequency"],
         [[], [5], [1]]),
        # Add and delete same
        (["FrequencyTracker", "add", "deleteOne", "add", "hasFrequency"],
         [[], [1], [1], [1], [1]]),
    ]

    yielded = 0
    for ops, args in edge_cases:
        if yielded >= count:
            return
        yield f"{json.dumps(ops)}\n{json.dumps(args)}"
        yielded += 1

    # Random cases
    while yielded < count:
        num_ops = random.randint(5, 50)
        ops = ["FrequencyTracker"]
        args = [[]]

        for _ in range(num_ops):
            op_type = random.choice(["add", "add", "deleteOne", "hasFrequency"])
            if op_type == "add":
                ops.append("add")
                args.append([random.randint(1, 100)])
            elif op_type == "deleteOne":
                ops.append("deleteOne")
                args.append([random.randint(1, 100)])
            else:
                ops.append("hasFrequency")
                args.append([random.randint(1, 10)])

        yield f"{json.dumps(ops)}\n{json.dumps(args)}"
        yielded += 1


def generate_for_complexity(n: int) -> str:
    """Generate test case with n operations."""
    ops = ["FrequencyTracker"]
    args = [[]]

    for _ in range(n):
        op_type = random.choice(["add", "add", "deleteOne", "hasFrequency"])
        if op_type == "add":
            ops.append("add")
            args.append([random.randint(1, 1000)])
        elif op_type == "deleteOne":
            ops.append("deleteOne")
            args.append([random.randint(1, 1000)])
        else:
            ops.append("hasFrequency")
            args.append([random.randint(1, 100)])

    return f"{json.dumps(ops)}\n{json.dumps(args)}"


if __name__ == "__main__":
    print("Sample test cases:")
    for i, case in enumerate(generate(3, seed=42)):
        print(f"Case {i+1}:")
        print(case)
        print()
