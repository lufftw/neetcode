# solutions/0150_evaluate_reverse_polish_notation.py
"""
Problem 0150 - Evaluate Reverse Polish Notation

Evaluate the value of an arithmetic expression in Reverse Polish Notation (RPN).

Valid operators are +, -, *, and /. Each operand may be an integer or
another expression. Division between two integers truncates toward zero.

LeetCode Constraints:
- 1 <= tokens.length <= 10^4
- tokens[i] is either an operator or an integer in range [-200, 200]

Key Insight:
RPN (postfix notation) is naturally evaluated using a stack:
- When we see a number, push it onto the stack
- When we see an operator, pop two operands, apply operator, push result

The stack-based approach is clean and O(n) time.

Note: Division truncates toward zero in Python 3, which requires
int(a/b) rather than a//b (which truncates toward negative infinity).

Solution Approaches:
1. Stack-based evaluation: O(n) time, O(n) space
2. Lambda dispatch: Same complexity but cleaner operator handling
"""
from typing import List
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionStack",
        "method": "evalRPN",
        "complexity": "O(n) time, O(n) space",
        "description": "Stack-based evaluation with explicit operator handling",
    },
    "lambda": {
        "class": "SolutionLambda",
        "method": "evalRPN",
        "complexity": "O(n) time, O(n) space",
        "description": "Lambda dispatch table for operators",
    },
}


class SolutionStack:
    """
    Stack-based evaluation.

    Process tokens left to right:
    - Number: push to stack
    - Operator: pop two operands, compute, push result

    Important: The second popped value is the LEFT operand!
    For "a b -", we want a - b, not b - a.

    Division truncation: Python's // truncates toward negative infinity,
    but the problem wants truncation toward zero. Use int(a/b) instead.
    """

    def evalRPN(self, tokens: List[str]) -> int:
        stack: List[int] = []

        for token in tokens:
            if token in "+-*/":
                b = stack.pop()  # Second operand (right)
                a = stack.pop()  # First operand (left)

                if token == "+":
                    result = a + b
                elif token == "-":
                    result = a - b
                elif token == "*":
                    result = a * b
                else:  # "/"
                    # Truncate toward zero
                    result = int(a / b)

                stack.append(result)
            else:
                stack.append(int(token))

        return stack[0]


class SolutionLambda:
    """
    Lambda dispatch table approach.

    Use a dictionary mapping operators to lambda functions.
    This is cleaner than if-else chains for operator dispatch.

    Same algorithm and complexity as explicit approach.
    """

    def evalRPN(self, tokens: List[str]) -> int:
        operations = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: int(a / b),  # Truncate toward zero
        }

        stack: List[int] = []

        for token in tokens:
            if token in operations:
                b = stack.pop()
                a = stack.pop()
                stack.append(operations[token](a, b))
            else:
                stack.append(int(token))

        return stack[0]


def solve():
    import sys
    import json

    data = sys.stdin.read().strip()
    tokens = json.loads(data)

    solver = get_solver(SOLUTIONS)
    result = solver.evalRPN(tokens)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
