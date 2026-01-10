"""
Test Case Generator for Problem 0126 - Word Ladder II

LeetCode Constraints:
- 1 <= beginWord.length <= 5
- 1 <= wordList.length <= 500
- All words same length, lowercase letters
- beginWord != endWord
"""
import json
import random
import string
from typing import Iterator, Optional


def _gen_word(length: int) -> str:
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def _one_char_diff(w1: str, w2: str) -> bool:
    return sum(c1 != c2 for c1, c2 in zip(w1, w2)) == 1


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        ("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]),  # Example 1
        ("hit", "cog", ["hot", "dot", "dog", "lot", "log"]),         # No path (cog missing)
        ("a", "c", ["a", "b", "c"]),                                  # Single char
        ("ab", "cd", ["ab", "ad", "cd"]),                            # Short chain
        ("abc", "xyz", ["abc", "xbc", "xyc", "xyz"]),                # Longer chain
    ]

    for begin, end, words in edge_cases:
        yield f'{json.dumps(begin)}\n{json.dumps(end)}\n{json.dumps(words, separators=(",", ":"))}'
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        length = random.randint(2, 4)
        n_words = random.randint(3, 15)
        words = list(set(_gen_word(length) for _ in range(n_words * 2)))[:n_words]
        if len(words) < 2:
            words = [_gen_word(length) for _ in range(3)]
        begin = random.choice(words)
        end = random.choice([w for w in words if w != begin] or [_gen_word(length)])
        if end not in words:
            words.append(end)
        yield f'{json.dumps(begin)}\n{json.dumps(end)}\n{json.dumps(words, separators=(",", ":"))}'


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    n = max(3, min(n, 50))
    length = 3
    words = list(set(_gen_word(length) for _ in range(n * 2)))[:n]
    begin = words[0]
    end = words[-1]
    return f'{json.dumps(begin)}\n{json.dumps(end)}\n{json.dumps(words, separators=(",", ":"))}'
