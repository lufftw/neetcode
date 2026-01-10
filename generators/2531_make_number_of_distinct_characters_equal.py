"""
Test Case Generator for Problem 2531 - Make Number of Distinct Characters Equal

LeetCode Constraints:
- 1 <= word1.length, word2.length <= 10^5
- Lowercase English letters only
"""
import json
import random
import string
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        ("ac", "b"),            # Example 1: false
        ("abcc", "aab"),        # Example 2: true
        ("abcde", "fghij"),     # Example 3: true (disjoint)
        ("a", "a"),             # Same single char
        ("aa", "bb"),           # Swap same counts
        ("abc", "abc"),         # Identical
        ("ab", "cd"),           # Disjoint pairs
        ("aaa", "bbb"),         # All same char
    ]

    for word1, word2 in edge_cases:
        yield f'{json.dumps(word1)}\n{json.dumps(word2)}'
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        len1 = random.randint(1, 20)
        len2 = random.randint(1, 20)
        chars1 = random.sample(string.ascii_lowercase, random.randint(1, min(len1, 10)))
        chars2 = random.sample(string.ascii_lowercase, random.randint(1, min(len2, 10)))
        word1 = ''.join(random.choice(chars1) for _ in range(len1))
        word2 = ''.join(random.choice(chars2) for _ in range(len2))
        yield f'{json.dumps(word1)}\n{json.dumps(word2)}'


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    n = max(1, min(n, 500))
    chars1 = random.sample(string.ascii_lowercase, random.randint(1, 10))
    chars2 = random.sample(string.ascii_lowercase, random.randint(1, 10))
    word1 = ''.join(random.choice(chars1) for _ in range(n))
    word2 = ''.join(random.choice(chars2) for _ in range(n))
    return f'{json.dumps(word1)}\n{json.dumps(word2)}'
