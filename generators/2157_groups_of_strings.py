"""
Test Case Generator for Problem 2157 - Groups of Strings

LeetCode Constraints:
- 1 <= words.length <= 2 * 10^4
- 1 <= words[i].length <= 26
- No letter occurs more than once in words[i]
"""
import json
import random
import string
from typing import Iterator, Optional


def _random_word(max_len: int = 10) -> str:
    """Generate a word with unique letters."""
    length = random.randint(1, min(max_len, 26))
    letters = random.sample(string.ascii_lowercase, length)
    return ''.join(letters)


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        (["a", "b", "ab", "cde"],),      # Example 1: 2 groups
        (["a", "ab", "abc"],),           # Example 2: chain, 1 group
        (["a"],),                         # Single word
        (["abc", "def", "ghi"],),         # All isolated
        (["ab", "ba"],),                  # Same letters different order → same mask
        (["ab", "ac", "bc"],),            # All pairwise connected by replace
        (["a", "b", "c", "ab", "bc", "ac", "abc"],),  # All connected
    ]

    for args in edge_cases:
        yield json.dumps(args[0], separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        n = random.randint(2, 20)
        words = [_random_word(8) for _ in range(n)]
        yield json.dumps(words, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    n = max(1, min(n, 200))
    words = [_random_word(min(10, 26)) for _ in range(n)]
    return json.dumps(words, separators=(',', ':'))
