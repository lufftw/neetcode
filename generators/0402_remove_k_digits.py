# generators/0402_remove_k_digits.py
"""
Test Case Generator for Problem 0402 - Remove K Digits

LeetCode Constraints:
- 1 <= k <= num.length <= 10^5
- num consists of only digits
- num does not have any leading zeros except for the zero itself

Time Complexity: O(n) with monotonic stack
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Remove K Digits.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Test input (num on line 1, k on line 2)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first (num, k)
    edge_cases = [
        ("1432219", 3),  # Classic example -> "1219"
        ("10200", 1),    # Leading zero case -> "200"
        ("10", 2),       # Remove all -> "0"
        ("9", 1),        # Single digit remove
        ("10", 1),       # Remove to get "0"
        ("112", 1),      # Equal digits
        ("123456789", 0),  # Remove nothing
        ("987654321", 8),  # Remove almost all
        ("1111111", 3),    # All same digits
    ]

    for num, k in edge_cases:
        yield f"{json.dumps(num)}\n{k}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        length = random.randint(1, 10000)
        yield _generate_case(length)


def _generate_case(length: int) -> str:
    """Generate a single random test case."""
    # First digit 1-9, rest 0-9 (no leading zeros)
    if length == 1:
        num = str(random.randint(0, 9))
    else:
        first = str(random.randint(1, 9))
        rest = "".join(str(random.randint(0, 9)) for _ in range(length - 1))
        num = first + rest

    k = random.randint(1, length)
    return f"{json.dumps(num)}\n{k}"


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific input size for complexity estimation."""
    n = max(1, n)
    return _generate_case(n)
