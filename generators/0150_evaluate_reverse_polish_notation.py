# generators/0150_evaluate_reverse_polish_notation.py
"""
Test Case Generator for Problem 0150 - Evaluate Reverse Polish Notation

LeetCode Constraints:
- 1 <= tokens.length <= 10^4
- tokens[i] is either an operator or an integer in range [-200, 200]
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Evaluate Reverse Polish Notation."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        ["3"],                              # Single number
        ["1", "2", "+"],                    # Simple addition
        ["4", "2", "-"],                    # Simple subtraction
        ["3", "4", "*"],                    # Simple multiplication
        ["10", "3", "/"],                   # Division with truncation
    ]

    for tokens in edge_cases:
        yield json.dumps(tokens)
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a valid random RPN expression."""
    # Build expression tree randomly
    num_operands = random.randint(2, 10)
    tokens = _build_rpn_expression(num_operands)
    return json.dumps(tokens)


def _build_rpn_expression(num_operands: int) -> List[str]:
    """Build a valid RPN expression with given number of operands."""
    operators = ["+", "-", "*"]  # Avoid division to prevent divide-by-zero
    tokens: List[str] = []

    # Start with first operand
    tokens.append(str(random.randint(-100, 100)))

    for _ in range(num_operands - 1):
        # Add another operand
        operand = random.randint(-100, 100)
        if operand == 0:
            operand = 1  # Avoid zero for potential division
        tokens.append(str(operand))

        # Add an operator (can add immediately or later)
        if random.random() < 0.7 and len(tokens) >= 2:
            tokens.append(random.choice(operators))

    # Ensure we have enough operators
    while tokens.count("+") + tokens.count("-") + tokens.count("*") + tokens.count("/") < num_operands - 1:
        tokens.append(random.choice(operators))

    return tokens


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with approximately n tokens.
    """
    n = max(1, min(n, 10000))
    num_operands = max(1, n // 2)
    tokens = _build_rpn_expression(num_operands)
    return json.dumps(tokens)


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}: {test}")
