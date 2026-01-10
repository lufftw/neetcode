"""
Test Case Generator for Problem 2156 - Find Substring With Given Hash Value

LeetCode Constraints:
- 1 <= k <= s.length <= 2 * 10^4
- 1 <= power, modulo <= 10^9
- 0 <= hashValue < modulo
- s consists of lowercase English letters
- Answer always exists
"""
import json
import random
import string
from typing import Iterator, Optional


def _val(c):
    return ord(c) - ord('a') + 1


def _compute_hash(s, power, modulo):
    """Compute hash of string."""
    h = 0
    p = 1
    for c in s:
        h = (h + _val(c) * p) % modulo
        p = (p * power) % modulo
    return h


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        ("leetcode", 7, 20, 2, 0),     # Example 1
        ("fbxzaad", 31, 100, 3, 32),   # Example 2
    ]

    for s, power, modulo, k, hashValue in edge_cases:
        yield f'"{s}"\n{power}\n{modulo}\n{k}\n{hashValue}'
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        n = random.randint(5, 100)
        s = ''.join(random.choice(string.ascii_lowercase) for _ in range(n))
        k = random.randint(1, min(n, 10))
        power = random.randint(2, 100)
        modulo = random.randint(100, 10000)

        # Pick a random valid substring and compute its hash
        start = random.randint(0, n - k)
        sub = s[start:start + k]
        hashValue = _compute_hash(sub, power, modulo)

        yield f'"{s}"\n{power}\n{modulo}\n{k}\n{hashValue}'


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    n = max(5, min(n, 20000))
    s = ''.join(random.choice(string.ascii_lowercase) for _ in range(n))
    k = random.randint(1, min(n, 100))
    power = random.randint(2, 1000)
    modulo = random.randint(1000, 1000000)

    # Compute hash of first substring
    hashValue = _compute_hash(s[:k], power, modulo)

    return f'"{s}"\n{power}\n{modulo}\n{k}\n{hashValue}'
