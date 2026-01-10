# generators/0678_valid_parenthesis_string.py
"""
Test Case Generator for Problem 0678 - Valid Parenthesis String

LeetCode Constraints:
- 1 <= s.length <= 100
- s[i] is '(', ')' or '*'
"""
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Valid Parenthesis String."""
    if seed is not None:
        random.seed(seed)

    edge_cases = ["()", "(*)", "(*))", "*", "((*))", "((*)", ")*", "(*", "***"]

    for s in edge_cases:
        yield s
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    length = random.randint(5, 30)
    return "".join(random.choices("()*", k=length))


def generate_for_complexity(n: int) -> str:
    n = max(1, min(n, 100))
    return "".join(random.choices("()*", k=n))


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}: {test}")
