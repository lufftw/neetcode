"""
Random test generator for LC 10: Regular Expression Matching

Constraints:
- 1 <= s.length <= 20
- 1 <= p.length <= 20
- s contains only lowercase English letters.
- p contains only lowercase English letters, '.', and '*'.
- It is guaranteed for each appearance of the character '*', there will be
  a previous valid character to match.
"""
import random
import json
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test cases.

    Yields test input strings in the format expected by the solution.
    """
    if seed is not None:
        random.seed(seed)

    for _ in range(count):
        # Random lengths
        s_len = random.randint(1, 15)
        p_len = random.randint(1, 15)

        s = _generate_string(s_len)
        p = _generate_pattern(p_len)

        yield f'{json.dumps(s)}\n{json.dumps(p)}'


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific size n for complexity estimation.
    """
    s = _generate_string(n)
    p = _generate_pattern(n)

    return f'{json.dumps(s)}\n{json.dumps(p)}'


def _generate_string(length: int) -> str:
    """Generate a random lowercase string of given length."""
    return ''.join(
        chr(ord('a') + random.randint(0, 25))
        for _ in range(length)
    )


def _generate_pattern(length: int) -> str:
    """
    Generate a valid regex pattern.
    Rules:
    - '*' must follow a valid character (not another '*')
    - Pattern can contain '.', '*', and lowercase letters
    """
    if length == 0:
        return ""

    result = []
    i = 0

    while i < length:
        if not result:
            # First character cannot be '*'
            char = _random_pattern_char(allow_star=False)
        else:
            # Can add '*' only if previous is not '*'
            allow_star = result[-1] != '*'
            char = _random_pattern_char(allow_star=allow_star)

        result.append(char)
        i += 1

    return ''.join(result)


def _random_pattern_char(allow_star: bool = True) -> str:
    """Generate a random pattern character."""
    choices = list('abcdefghijklmnopqrstuvwxyz') + ['.']
    if allow_star:
        # Add '*' with lower probability
        if random.random() < 0.2:
            return '*'
    return random.choice(choices)


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}:")
        print(test)
        print()
