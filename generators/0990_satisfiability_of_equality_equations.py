# generators/0990_satisfiability_of_equality_equations.py
"""
Test Case Generator for Problem 0990 - Satisfiability of Equality Equations

LeetCode Constraints:
- 1 <= equations.length <= 500
- equations[i].length == 4
- equations[i][0] and equations[i][3] are lowercase letters
- equations[i][1] is either '=' or '!'
- equations[i][2] is '='
"""
import json
import random
import string
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate test case inputs for Equality Equations."""
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        ["a==b", "b!=a"],  # False
        ["b==a", "a==b"],  # True
        ["a==b", "b==c", "a==c"],  # True
        ["a==b", "b!=c", "c==a"],  # False (transitive)
        ["a!=a"],  # False (self-inequality)
        ["a==a"],  # True (trivial)
        ["a==b", "c==d", "a!=d"],  # True (disjoint groups)
    ]

    for equations in edge_cases:
        yield json.dumps(equations, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case."""
    num_equations = random.randint(2, 20)
    letters = list(string.ascii_lowercase[:10])  # Use first 10 letters

    equations = []
    for _ in range(num_equations):
        a = random.choice(letters)
        b = random.choice(letters)
        op = random.choice(['==', '!='])
        equations.append(f"{a}{op}{b}")

    return json.dumps(equations, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific input size."""
    letters = list(string.ascii_lowercase)
    equations = []
    for _ in range(n):
        a = random.choice(letters)
        b = random.choice(letters)
        op = random.choice(['==', '!='])
        equations.append(f"{a}{op}{b}")
    return json.dumps(equations, separators=(',', ':'))


if __name__ == "__main__":
    for i, case in enumerate(generate(5)):
        print(f"Case {i + 1}: {case}")
