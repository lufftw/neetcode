"""
Test Case Generator for Problem 2423 - Remove Letter To Equalize Frequency

LeetCode Constraints:
- 2 <= word.length <= 100
- word consists of lowercase English letters only.
"""
import json
import random
import string
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        "abcc",      # True: remove c
        "aazz",      # False
        "aa",        # True: remove one a
        "ab",        # True: remove either
        "abc",       # True: remove any
        "aabb",      # False
        "aaabbb",    # False
        "aaabbbc",   # True: remove c
        "zzzz",      # True: single char
        "abcdef",    # True: all freq 1
    ]

    for case in edge_cases:
        yield json.dumps(case, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        length = random.randint(2, 100)
        num_chars = random.randint(1, min(26, length))
        chars = random.sample(string.ascii_lowercase, num_chars)
        word = ''.join(random.choices(chars, k=length))
        yield json.dumps(word, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific length."""
    n = max(2, min(n, 100))
    num_chars = random.randint(1, min(26, n))
    chars = random.sample(string.ascii_lowercase, num_chars)
    word = ''.join(random.choices(chars, k=n))
    return json.dumps(word, separators=(',', ':'))
