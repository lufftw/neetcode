"""
Random test generator for LC 44: Wildcard Matching

Constraints:
- 0 <= s.length, p.length <= 2000
- s contains only lowercase English letters.
- p contains only lowercase English letters, '?' or '*'.
"""
import json
import random
import string
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test cases for Wildcard Matching.

    Strategies:
    1. Edge cases: empty strings, all '*', all '?'
    2. Guaranteed matches: construct pattern from string
    3. Guaranteed non-matches: incompatible patterns
    4. Random cases: mix of characters and wildcards

    Yields test input strings in the format expected by the solution.
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        ("", ""),                    # Both empty -> True
        ("", "*"),                   # Empty matches '*' -> True
        ("", "***"),                 # Empty matches multiple '*' -> True
        ("", "a"),                   # Empty vs non-empty -> False
        ("a", ""),                   # Non-empty vs empty -> False
        ("aa", "*"),                 # '*' matches any -> True
        ("cb", "?a"),                # '?' matches one, but second differs -> False
        ("adceb", "*a*b"),           # Classic case -> True
        ("acdcb", "a*c?b"),          # Mixed wildcards -> False
        ("abc", "abc"),              # Exact match -> True
        ("abc", "???"),              # All '?' -> True
        ("abc", "****"),             # Multiple '*' -> True
        ("", "?"),                   # Empty vs '?' -> False
        ("a", "?"),                  # Single char vs '?' -> True
        ("ab", "?*"),                # '?' then '*' -> True
    ]

    for s, p in edge_cases:
        yield f"{json.dumps(s, separators=(',', ':'))}\n{json.dumps(p, separators=(',', ':'))}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case."""
    # Decide case type
    case_type = random.choice(['match', 'no_match', 'random'])

    if case_type == 'match':
        return _generate_matching_case()
    elif case_type == 'no_match':
        return _generate_non_matching_case()
    else:
        return _generate_random_case()


def _generate_matching_case() -> str:
    """Generate a case that should match."""
    # Generate a random string
    s_length = random.randint(1, 50)
    s = ''.join(random.choices(string.ascii_lowercase, k=s_length))

    # Build pattern that matches s
    # Strategy: randomly insert '?', '*', or keep original chars
    p_chars = []
    i = 0
    while i < len(s):
        choice = random.random()
        if choice < 0.3:
            # Use '?' for single char
            p_chars.append('?')
            i += 1
        elif choice < 0.5:
            # Use '*' to match some chars
            skip = random.randint(0, min(5, len(s) - i))
            p_chars.append('*')
            i += skip
        else:
            # Keep original char
            p_chars.append(s[i])
            i += 1

    # Maybe add trailing '*'
    if random.random() < 0.3:
        p_chars.append('*')

    p = ''.join(p_chars)

    return f"{json.dumps(s, separators=(',', ':'))}\n{json.dumps(p, separators=(',', ':'))}"


def _generate_non_matching_case() -> str:
    """Generate a case that should not match."""
    s_length = random.randint(1, 30)
    s = ''.join(random.choices(string.ascii_lowercase[:5], k=s_length))

    # Build pattern that won't match
    # Strategy: include a character not in s
    excluded_char = random.choice(string.ascii_lowercase[5:10])

    p_length = random.randint(1, 30)
    p_chars = []
    for _ in range(p_length):
        choice = random.random()
        if choice < 0.2:
            p_chars.append('?')
        elif choice < 0.3:
            p_chars.append('*')
        elif choice < 0.5:
            # Add excluded char to ensure mismatch
            p_chars.append(excluded_char)
        else:
            p_chars.append(random.choice(string.ascii_lowercase[:5]))

    p = ''.join(p_chars)

    return f"{json.dumps(s, separators=(',', ':'))}\n{json.dumps(p, separators=(',', ':'))}"


def _generate_random_case() -> str:
    """Generate a completely random case."""
    s_length = random.randint(0, 100)
    s = ''.join(random.choices(string.ascii_lowercase, k=s_length))

    p_length = random.randint(0, 100)
    p_chars = []
    for _ in range(p_length):
        choice = random.random()
        if choice < 0.1:
            p_chars.append('?')
        elif choice < 0.2:
            p_chars.append('*')
        else:
            p_chars.append(random.choice(string.ascii_lowercase))

    p = ''.join(p_chars)

    return f"{json.dumps(s, separators=(',', ':'))}\n{json.dumps(p, separators=(',', ':'))}"


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific size n for complexity estimation.

    For wildcard matching:
    - n is the length of both s and p
    - Worst case: s = "aaaa...a", p = "*a*a*a*...*a" (many '*' causing backtracking)
    """
    n = max(1, n)

    # Generate string of all 'a's
    s = 'a' * n

    # Generate pattern with alternating '*' and 'a' (worst case)
    # This forces many backtracking attempts in greedy approach
    p_parts = []
    remaining = n
    while remaining > 0:
        p_parts.append('*')
        take = min(random.randint(1, 3), remaining)
        p_parts.append('a' * take)
        remaining -= take
    p_parts.append('*')

    p = ''.join(p_parts)

    return f"{json.dumps(s, separators=(',', ':'))}\n{json.dumps(p, separators=(',', ':'))}"


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(10, seed=42), 1):
        lines = test.split('\n')
        s = json.loads(lines[0])
        p = json.loads(lines[1])
        print(f"Test {i}: s={repr(s)}, p={repr(p)}")
