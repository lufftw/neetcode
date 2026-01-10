"""
Test Case Generator for Problem 0707 - Design Linked List

LeetCode Constraints:
- 0 <= index, val <= 1000
- At most 2000 calls to methods
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        # Example from problem
        (["MyLinkedList", "addAtHead", "addAtTail", "addAtIndex", "get", "deleteAtIndex", "get"],
         [[], [1], [3], [1, 2], [1], [1], [1]]),
        # Get from empty list
        (["MyLinkedList", "get"],
         [[], [0]]),
        # Add and delete single element
        (["MyLinkedList", "addAtHead", "deleteAtIndex", "get"],
         [[], [1], [0], [0]]),
        # Multiple addAtHead
        (["MyLinkedList", "addAtHead", "addAtHead", "addAtHead", "get", "get", "get"],
         [[], [3], [2], [1], [0], [1], [2]]),
    ]

    for ops, args in edge_cases:
        yield f'{json.dumps(ops, separators=(",", ":"))}\n{json.dumps(args, separators=(",", ":"))}'
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        operations = ["MyLinkedList"]
        args = [[]]
        size = 0

        num_ops = random.randint(5, 30)
        for _ in range(num_ops):
            op_type = random.choice(["get", "addAtHead", "addAtTail", "addAtIndex", "deleteAtIndex"])

            if op_type == "get":
                idx = random.randint(-1, max(0, size + 1))
                operations.append("get")
                args.append([idx])
            elif op_type == "addAtHead":
                val = random.randint(0, 100)
                operations.append("addAtHead")
                args.append([val])
                size += 1
            elif op_type == "addAtTail":
                val = random.randint(0, 100)
                operations.append("addAtTail")
                args.append([val])
                size += 1
            elif op_type == "addAtIndex":
                idx = random.randint(0, size + 1)
                val = random.randint(0, 100)
                operations.append("addAtIndex")
                args.append([idx, val])
                if idx <= size:
                    size += 1
            elif op_type == "deleteAtIndex":
                idx = random.randint(-1, max(0, size))
                operations.append("deleteAtIndex")
                args.append([idx])
                if 0 <= idx < size:
                    size -= 1

        yield f'{json.dumps(operations, separators=(",", ":"))}\n{json.dumps(args, separators=(",", ":"))}'


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific number of operations for complexity estimation."""
    n = max(1, min(n, 500))

    operations = ["MyLinkedList"]
    args = [[]]

    # Add n elements, then do various operations
    for i in range(n // 2):
        operations.append("addAtTail")
        args.append([i])

    for i in range(n // 4):
        operations.append("get")
        args.append([random.randint(0, max(0, n // 2 - 1))])

    for i in range(n // 4):
        operations.append("deleteAtIndex")
        args.append([0])

    return f'{json.dumps(operations, separators=(",", ":"))}\n{json.dumps(args, separators=(",", ":"))}'
