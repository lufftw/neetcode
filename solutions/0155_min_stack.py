# solutions/0155_min_stack.py
"""
Problem: Min Stack
https://leetcode.com/problems/min-stack/

Design a stack that supports push, pop, top, and retrieving the minimum
element in constant time.

Implement the MinStack class:
- MinStack() initializes the stack object
- void push(int val) pushes the element val onto the stack
- void pop() removes the element on the top of the stack
- int top() gets the top element of the stack
- int getMin() retrieves the minimum element in the stack

All operations must be O(1) time complexity.

Constraints:
- -2^31 <= val <= 2^31 - 1
- Methods pop, top and getMin will always be called on non-empty stacks
- At most 3 * 10^4 calls to push, pop, top, and getMin
"""
from typing import List, Optional

SOLUTIONS = {
    "default": {
        "class": "MinStackTwoStacks",
        "method": "_run_operations",
        "complexity": "O(1) per operation, O(n) space",
        "description": "Two stacks: values and minimum history",
    },
    "tuple": {
        "class": "MinStackTuple",
        "method": "_run_operations",
        "complexity": "O(1) per operation, O(n) space",
        "description": "Single stack with (value, current_min) pairs",
    },
}


class MinStackTwoStacks:
    """
    Two-stack approach tracking minimum at each level.

    The main stack stores values normally. The auxiliary min_stack stores
    the minimum value at each level of the stack. When pushing, we track
    the minimum of (new_value, current_min). When popping, both stacks pop.

    This provides O(1) access to minimum because min_stack's top always
    contains the current stack's minimum value.
    """

    def __init__(self):
        # Main stack for values
        self.stack: List[int] = []
        # Auxiliary stack tracking minimum at each level
        self.min_stack: List[int] = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        # Track minimum: compare with current min or use val if first element
        if self.min_stack:
            self.min_stack.append(min(val, self.min_stack[-1]))
        else:
            self.min_stack.append(val)

    def pop(self) -> None:
        # Both stacks maintain synchronized sizes
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        # Min stack's top is always current minimum
        return self.min_stack[-1]

    def _run_operations(
        self, operations: List[str], arguments: List[List]
    ) -> List[Optional[int]]:
        """Execute operations and return results."""
        results: List[Optional[int]] = [None]  # Constructor returns null

        for op, args in zip(operations[1:], arguments[1:]):
            if op == "push":
                self.push(args[0])
                results.append(None)
            elif op == "pop":
                self.pop()
                results.append(None)
            elif op == "top":
                results.append(self.top())
            elif op == "getMin":
                results.append(self.getMin())

        return results


class MinStackTuple:
    """
    Single stack storing value-minimum pairs.

    Each element is a tuple (value, current_min_at_this_level). This
    embeds the minimum tracking directly into the data structure,
    eliminating the need for a separate auxiliary stack.

    Trade-off: slightly more memory per element (tuple overhead) but
    simpler synchronization logic since we only manage one stack.
    """

    def __init__(self):
        # Stack of (value, min_at_this_level) tuples
        self.stack: List[tuple] = []

    def push(self, val: int) -> None:
        # Calculate minimum for this level
        if self.stack:
            current_min = min(val, self.stack[-1][1])
        else:
            current_min = val
        self.stack.append((val, current_min))

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]

    def _run_operations(
        self, operations: List[str], arguments: List[List]
    ) -> List[Optional[int]]:
        """Execute operations and return results."""
        results: List[Optional[int]] = [None]  # Constructor returns null

        for op, args in zip(operations[1:], arguments[1:]):
            if op == "push":
                self.push(args[0])
                results.append(None)
            elif op == "pop":
                self.pop()
                results.append(None)
            elif op == "top":
                results.append(self.top())
            elif op == "getMin":
                results.append(self.getMin())

        return results


def judge(actual, expected, input_data: str) -> bool:
    """
    Validate MinStack operations by simulating with reference implementation.
    """
    import json

    # Parse actual if string
    if isinstance(actual, str):
        actual = json.loads(actual)

    lines = input_data.strip().split("\n")
    operations = json.loads(lines[0])
    arguments = json.loads(lines[1])

    # Simulate with two-stack approach
    stack = []
    min_stack = []
    expected_results = [None]

    for op, args in zip(operations[1:], arguments[1:]):
        if op == "push":
            val = args[0]
            stack.append(val)
            if min_stack:
                min_stack.append(min(val, min_stack[-1]))
            else:
                min_stack.append(val)
            expected_results.append(None)
        elif op == "pop":
            stack.pop()
            min_stack.pop()
            expected_results.append(None)
        elif op == "top":
            expected_results.append(stack[-1])
        elif op == "getMin":
            expected_results.append(min_stack[-1])

    return actual == expected_results


JUDGE_FUNC = judge


def solve():
    import sys
    import json

    lines = sys.stdin.read().strip().split("\n")

    # Parse input: operations and arguments
    operations = json.loads(lines[0])
    arguments = json.loads(lines[1])

    # Get the solution class
    import os

    method = os.environ.get("METHOD", "default")
    solution_info = SOLUTIONS.get(method, SOLUTIONS["default"])
    cls = globals()[solution_info["class"]]

    # Instantiate and run operations
    instance = cls()
    result = instance._run_operations(operations, arguments)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
