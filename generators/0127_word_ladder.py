# generators/0127_word_ladder.py
"""
Test Case Generator for Problem 0127 - Word Ladder

LeetCode Constraints:
- 1 <= beginWord.length <= 10
- endWord.length == beginWord.length
- 1 <= wordList.length <= 5000
- wordList[i].length == beginWord.length
- beginWord, endWord, and wordList[i] consist of lowercase English letters
- beginWord != endWord
- All words in wordList are unique
"""
import json
import random
import string
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Word Ladder."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        ("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]),  # Classic
        ("hit", "cog", ["hot", "dot", "dog", "lot", "log"]),  # No solution
        ("a", "c", ["a", "b", "c"]),  # Single char
        ("hot", "dog", ["hot", "dog"]),  # No intermediate
    ]

    for begin, end, words in edge_cases:
        yield f'"{begin}"\n"{end}"\n{json.dumps(words)}'
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random word ladder test case."""
    word_len = random.randint(2, 5)
    num_words = random.randint(10, 50)

    # Generate a connected word ladder to ensure solution exists sometimes
    word_list = _generate_word_graph(word_len, num_words)

    if len(word_list) < 2:
        word_list = [_random_word(word_len) for _ in range(num_words)]

    # Pick begin and end words
    begin_word = random.choice(word_list)

    # Remove begin_word from list and pick end_word
    remaining = [w for w in word_list if w != begin_word]
    if not remaining:
        remaining = [_random_word(word_len)]

    end_word = random.choice(remaining)

    # Sometimes include end_word in list, sometimes not
    if random.random() < 0.7 and end_word not in remaining:
        remaining.append(end_word)

    return f'"{begin_word}"\n"{end_word}"\n{json.dumps(remaining)}'


def _random_word(length: int) -> str:
    """Generate a random lowercase word."""
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))


def _generate_word_graph(word_len: int, num_words: int) -> List[str]:
    """
    Generate words with some connectivity (one-letter transformations).
    """
    words = set()
    base_word = _random_word(word_len)
    words.add(base_word)

    queue = [base_word]
    while len(words) < num_words and queue:
        word = queue.pop(0)

        # Generate variations
        for i in range(word_len):
            for c in string.ascii_lowercase:
                if c != word[i]:
                    new_word = word[:i] + c + word[i + 1 :]
                    if new_word not in words and random.random() < 0.3:
                        words.add(new_word)
                        queue.append(new_word)
                        if len(words) >= num_words:
                            break
            if len(words) >= num_words:
                break

    return list(words)


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with approximately n words for complexity estimation.
    """
    n = max(2, min(n, 5000))
    word_len = 4  # Fixed length for consistency

    word_list = _generate_word_graph(word_len, n)

    if len(word_list) < 2:
        word_list = [_random_word(word_len) for _ in range(n)]

    begin_word = word_list[0]
    end_word = word_list[-1] if len(word_list) > 1 else _random_word(word_len)

    return f'"{begin_word}"\n"{end_word}"\n{json.dumps(word_list)}'


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}:\n{test}\n")
