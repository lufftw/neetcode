# generators/0020_valid_parentheses.py
"""
Test Case Generator for Problem 0020 - Valid Parentheses

LeetCode Constraints:
- 1 <= s.length <= 10^4
- s consists of parentheses only '()[]{}'.
"""
import json
import random
from typing import Iterator, Optional


BRACKETS = '()[]{}'
OPEN_BRACKETS = '([{'
CLOSE_BRACKETS = ')]}'
BRACKET_PAIRS = {'(': ')', '[': ']', '{': '}'}


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Valid Parentheses.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (JSON quoted string)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        "()",           # Simple valid
        "()[]{}",       # Multiple valid
        "(]",           # Simple invalid
        "([)]",         # Interleaved invalid
        "{[]}",         # Nested valid
        "((()))",       # Deep nesting valid
        "(",            # Unclosed
        ")",            # No opener
        "",             # Empty (though constraint says 1 <=)
        "{{{{}}}}",     # All same type
        "([{}])",       # Mixed nested
        "(((((",        # All open
        ")))))",        # All close
        "()()()(){}",   # Alternating
    ]

    for s in edge_cases:
        if s:  # Skip empty per constraint
            yield json.dumps(s, separators=(',', ':'))
            count -= 1
            if count <= 0:
                return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case."""
    # Randomly decide if we want a valid or invalid string
    is_valid = random.random() < 0.5

    if is_valid:
        s = _generate_valid_string()
    else:
        s = _generate_invalid_string()

    return json.dumps(s, separators=(',', ':'))


def _generate_valid_string() -> str:
    """Generate a valid parentheses string."""
    length = random.randint(2, 100)
    # Must be even length for valid string
    if length % 2 == 1:
        length += 1

    result = []
    stack = []

    for _ in range(length):
        if not stack or random.random() < 0.5:
            # Open a new bracket
            open_bracket = random.choice(OPEN_BRACKETS)
            result.append(open_bracket)
            stack.append(open_bracket)
        else:
            # Close the most recent bracket
            open_bracket = stack.pop()
            result.append(BRACKET_PAIRS[open_bracket])

    # Close all remaining open brackets
    while stack:
        open_bracket = stack.pop()
        result.append(BRACKET_PAIRS[open_bracket])

    return ''.join(result)


def _generate_invalid_string() -> str:
    """Generate an invalid parentheses string."""
    strategies = ['mismatch', 'unclosed', 'extra_close', 'interleaved']
    strategy = random.choice(strategies)

    if strategy == 'mismatch':
        # Mismatched brackets
        length = random.randint(2, 20)
        result = []
        for _ in range(length):
            result.append(random.choice(BRACKETS))
        return ''.join(result)

    elif strategy == 'unclosed':
        # More opens than closes
        opens = random.randint(1, 10)
        closes = random.randint(0, opens - 1)
        result = [random.choice(OPEN_BRACKETS) for _ in range(opens)]
        result.extend(random.choice(CLOSE_BRACKETS) for _ in range(closes))
        random.shuffle(result)
        return ''.join(result)

    elif strategy == 'extra_close':
        # More closes than opens
        return ')' + _generate_valid_string()

    else:  # interleaved
        # Classic interleaved case like ([)]
        return '([)]'


# ============================================
# Complexity Estimation (controlled size)
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Valid Parentheses:
    - n is the string length
    - Expected complexity: O(n) for stack solution

    Args:
        n: Target string length

    Returns:
        str: Test input
    """
    # Clamp to constraints
    n = max(2, min(n, 10000))

    # Generate valid string of approximately size n
    s = _generate_valid_string_of_size(n)
    return json.dumps(s, separators=(',', ':'))


def _generate_valid_string_of_size(n: int) -> str:
    """Generate a valid parentheses string of approximately size n."""
    # Ensure even length
    if n % 2 == 1:
        n += 1

    result = []
    stack = []
    remaining = n

    while remaining > 0:
        if not stack or (remaining > len(stack) and random.random() < 0.5):
            open_bracket = random.choice(OPEN_BRACKETS)
            result.append(open_bracket)
            stack.append(open_bracket)
            remaining -= 1
        else:
            open_bracket = stack.pop()
            result.append(BRACKET_PAIRS[open_bracket])
            remaining -= 1

    # Close remaining
    while stack:
        result.append(BRACKET_PAIRS[stack.pop()])

    return ''.join(result)


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}: {test}")
