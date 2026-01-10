"""
Test Case Generator for Problem 2746 - Decremental String Concatenation

LeetCode Constraints:
- 1 <= words.length <= 1000
- 1 <= words[i].length <= 50
- Lowercase English letters
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
        (["aa", "ab", "bc"],),    # Example 1
        (["ab", "b"],),          # Example 2
        (["aaa", "c", "aba"],),  # Example 3
        (["a"],),                # Single word
        (["ab", "ba"],),         # Can merge both ways
        (["abc", "cde", "efg"],),  # Chain
    ]

    for args in edge_cases:
        yield json.dumps(args[0], separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        n = random.randint(2, 10)
        words = []
        for _ in range(n):
            length = random.randint(1, 10)
            word = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
            words.append(word)
        yield json.dumps(words, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    n = max(2, min(n, 100))
    words = []
    for _ in range(n):
        length = random.randint(1, 10)
        word = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
        words.append(word)
    return json.dumps(words, separators=(',', ':'))
