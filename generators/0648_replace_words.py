# generators/0648_replace_words.py
"""
Test Case Generator for Problem 0648 - Replace Words

LeetCode Constraints:
- 1 <= dictionary.length <= 1000
- 1 <= dictionary[i].length <= 100
- dictionary[i] consists of only lower-case letters.
- 1 <= sentence.length <= 10^6
- sentence consists of only lower-case letters and spaces.
- The number of words in sentence is in the range [1, 1000]
- The length of each word in sentence is in the range [1, 1000]
- Every two consecutive words in sentence will be separated by exactly one space.
- sentence does not have leading or trailing spaces.
"""
import json
import random
import string
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Replace Words.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Dictionary and sentence in format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # Example 1
        (["cat", "bat", "rat"], "the cattle was rattled by the battery"),
        # Example 2
        (["a", "b", "c"], "aadsfasf absbs bbab cadsfabd"),
        # Single root
        (["cat"], "caterpillar cats cathedral"),
        # No replacements
        (["xyz"], "hello world"),
        # Multiple roots for same word (shortest wins)
        (["a", "ap", "app"], "apple application"),
        # Empty-ish
        (["a"], "a"),
    ]

    for dictionary, sentence in edge_cases:
        yield _format_case(dictionary, sentence)
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _format_case(dictionary: List[str], sentence: str) -> str:
    """Format a test case as input string."""
    return f"{json.dumps(dictionary, separators=(',', ':'))}\n{sentence}"


def _generate_random_case() -> str:
    """Generate a single random test case."""
    # Generate dictionary of roots
    num_roots = random.randint(3, 15)
    roots = [_random_word(random.randint(1, 6)) for _ in range(num_roots)]

    # Generate sentence
    num_words = random.randint(3, 20)
    words = []

    for _ in range(num_words):
        if roots and random.random() < 0.6:
            # Create derivative from a root
            root = random.choice(roots)
            suffix = _random_word(random.randint(0, 8))
            words.append(root + suffix)
        else:
            # Random word
            words.append(_random_word(random.randint(2, 12)))

    sentence = ' '.join(words)

    return _format_case(roots, sentence)


def _random_word(length: int) -> str:
    """Generate a random lowercase word."""
    if length == 0:
        return ""
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    Args:
        n: Target number of words in sentence

    Returns:
        str: Test case with approximately n words
    """
    num_words = max(3, n)
    num_roots = min(100, max(5, n // 10))

    roots = [_random_word(random.randint(2, 5)) for _ in range(num_roots)]

    words = []
    for _ in range(num_words):
        if random.random() < 0.5:
            root = random.choice(roots)
            suffix = _random_word(random.randint(0, 10))
            words.append(root + suffix)
        else:
            words.append(_random_word(random.randint(3, 15)))

    sentence = ' '.join(words)

    return _format_case(roots, sentence)
