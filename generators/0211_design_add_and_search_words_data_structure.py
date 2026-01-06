# generators/0211_design_add_and_search_words_data_structure.py
"""
Test Case Generator for Problem 0211 - Design Add and Search Words Data Structure

LeetCode Constraints:
- 1 <= word.length <= 25
- word in addWord consists of lowercase English letters.
- word in search consists of '.' or lowercase English letters.
- There will be at most 2 dots in word for search queries.
- At most 10^4 calls will be made to addWord and search.
"""
import json
import random
import string
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Add and Search Words.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Operations and arguments in JSON format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # Example 1 from problem
        (["WordDictionary", "addWord", "addWord", "addWord", "search", "search", "search", "search"],
         [[], ["bad"], ["dad"], ["mad"], ["pad"], ["bad"], [".ad"], ["b.."]]),
        # Single character with wildcard
        (["WordDictionary", "addWord", "addWord", "search", "search"],
         [[], ["a"], ["b"], ["."], ["c"]]),
        # Double dots
        (["WordDictionary", "addWord", "search", "search"],
         [[], ["abc"], ["a.."], ["..c"]]),
        # No match with wildcard
        (["WordDictionary", "addWord", "search"],
         [[], ["hello"], ["h.x.o"]]),
        # All same length
        (["WordDictionary", "addWord", "addWord", "addWord", "search", "search"],
         [[], ["cat"], ["car"], ["can"], ["c.t"], ["..."]])
    ]

    for ops, args in edge_cases:
        yield _format_case(ops, args)
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _format_case(operations: List[str], arguments: List[List]) -> str:
    """Format a test case as input string."""
    return f"{json.dumps(operations, separators=(',', ':'))}\n{json.dumps(arguments, separators=(',', ':'))}"


def _generate_random_case() -> str:
    """Generate a single random test case."""
    num_ops = random.randint(5, 30)
    operations = ["WordDictionary"]
    arguments = [[]]

    words_added = []

    for _ in range(num_ops - 1):
        op = random.choice(["addWord", "search", "search"])  # More searches

        if op == "addWord":
            word = _random_word(random.randint(1, 15))
            words_added.append(word)
            operations.append("addWord")
            arguments.append([word])
        else:
            # Generate search pattern
            if words_added and random.random() < 0.5:
                # Based on existing word
                base_word = random.choice(words_added)
                pattern = _add_wildcards(base_word)
            else:
                # Random pattern
                pattern = _random_pattern(random.randint(1, 10))

            operations.append("search")
            arguments.append([pattern])

    return _format_case(operations, arguments)


def _random_word(length: int) -> str:
    """Generate a random lowercase word."""
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def _random_pattern(length: int) -> str:
    """Generate a random search pattern with at most 2 dots."""
    chars = list(_random_word(length))
    num_dots = random.randint(0, min(2, length))
    positions = random.sample(range(length), num_dots)
    for pos in positions:
        chars[pos] = '.'
    return ''.join(chars)


def _add_wildcards(word: str) -> str:
    """Add 0-2 wildcards to an existing word."""
    if len(word) == 0:
        return word
    chars = list(word)
    num_dots = random.randint(0, min(2, len(word)))
    positions = random.sample(range(len(word)), num_dots)
    for pos in positions:
        chars[pos] = '.'
    return ''.join(chars)


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    Args:
        n: Target number of operations

    Returns:
        str: Test case with approximately n operations
    """
    num_ops = max(3, n)
    operations = ["WordDictionary"]
    arguments = [[]]

    words = []
    for i in range(num_ops - 1):
        if i < num_ops // 3:
            # First third: addWords
            word = _random_word(random.randint(3, 15))
            words.append(word)
            operations.append("addWord")
            arguments.append([word])
        else:
            # Rest: searches
            operations.append("search")
            if words and random.random() < 0.7:
                pattern = _add_wildcards(random.choice(words))
            else:
                pattern = _random_pattern(random.randint(3, 10))
            arguments.append([pattern])

    return _format_case(operations, arguments)
