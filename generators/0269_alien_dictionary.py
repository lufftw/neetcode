# generators/0269_alien_dictionary.py
"""
Test Case Generator for Problem 0269 - Alien Dictionary

LeetCode Constraints:
- 1 <= words.length <= 100
- 1 <= words[i].length <= 100
- words[i] consists of only lowercase English letters
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Alien Dictionary."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        ["wrt", "wrf", "er", "ett", "rftt"],  # Valid ordering
        ["z", "x"],                             # Simple two chars
        ["z", "x", "z"],                        # Invalid: cycle
        ["abc", "ab"],                          # Invalid: prefix after longer
        ["a"],                                   # Single word
        ["a", "b", "c"],                        # Simple chain
    ]

    for words in edge_cases:
        yield json.dumps(words, separators=(",", ":"))
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate random word list (may or may not be valid)."""
    if random.random() < 0.7:
        # Generate valid ordering
        words = _generate_valid_words()
    else:
        # Generate potentially invalid
        words = _generate_random_words()

    return json.dumps(words, separators=(",", ":"))


def _generate_valid_words() -> List[str]:
    """Generate words that follow a valid alien ordering."""
    # Create a random ordering of some letters
    num_chars = random.randint(3, 8)
    chars = random.sample("abcdefghijklmnopqrstuvwxyz", num_chars)
    char_order = {c: i for i, c in enumerate(chars)}

    # Generate words using these chars
    num_words = random.randint(3, 10)
    words = []

    for _ in range(num_words):
        length = random.randint(1, 5)
        word = "".join(random.choices(chars, k=length))
        words.append(word)

    # Sort according to alien order
    def alien_compare(word):
        return [char_order[c] for c in word]

    words.sort(key=alien_compare)

    # Remove duplicates while preserving order
    seen = set()
    result = []
    for w in words:
        if w not in seen:
            seen.add(w)
            result.append(w)

    return result if result else ["a"]


def _generate_random_words() -> List[str]:
    """Generate random words (may create invalid ordering)."""
    chars = random.sample("abcdefghij", random.randint(3, 6))
    num_words = random.randint(3, 8)
    words = []

    for _ in range(num_words):
        length = random.randint(1, 4)
        word = "".join(random.choices(chars, k=length))
        words.append(word)

    return words


def generate_for_complexity(n: int) -> str:
    """Generate test case with n words for complexity estimation."""
    n = max(1, min(n, 100))
    words = _generate_valid_words()
    # Extend if needed
    while len(words) < n:
        words.extend(_generate_valid_words())
    return json.dumps(words[:n], separators=(",", ":"))


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}: {test}")
