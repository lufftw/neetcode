# generators/0208_implement_trie_prefix_tree.py
"""
Test Case Generator for Problem 0208 - Implement Trie (Prefix Tree)

LeetCode Constraints:
- 1 <= word.length, prefix.length <= 2000
- word and prefix consist only of lowercase English letters.
- At most 3 * 10^4 calls in total will be made to insert, search, and startsWith.
"""
import json
import random
import string
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Implement Trie.

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
        (["Trie", "insert", "search", "search", "startsWith", "insert", "search"],
         [[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]),
        # Single character
        (["Trie", "insert", "search", "startsWith"],
         [[], ["a"], ["a"], ["a"]]),
        # Long word
        (["Trie", "insert", "search", "startsWith"],
         [[], ["abcdefghij"], ["abcdefghij"], ["abcde"]]),
        # Multiple words with common prefix
        (["Trie", "insert", "insert", "insert", "search", "search", "startsWith"],
         [[], ["app"], ["apple"], ["application"], ["app"], ["appl"], ["appl"]]),
        # No match
        (["Trie", "insert", "search", "startsWith"],
         [[], ["hello"], ["world"], ["wor"]]),
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
    operations = ["Trie"]
    arguments = [[]]

    words_inserted = []

    for _ in range(num_ops - 1):
        op = random.choice(["insert", "search", "startsWith"])

        if op == "insert":
            word = _random_word(random.randint(1, 20))
            words_inserted.append(word)
            operations.append("insert")
            arguments.append([word])
        else:
            # Sometimes use inserted word, sometimes random
            if words_inserted and random.random() < 0.6:
                word = random.choice(words_inserted)
                if op == "startsWith" and len(word) > 1:
                    # Use prefix
                    word = word[:random.randint(1, len(word))]
            else:
                word = _random_word(random.randint(1, 15))

            operations.append(op)
            arguments.append([word])

    return _format_case(operations, arguments)


def _random_word(length: int) -> str:
    """Generate a random lowercase word."""
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    Args:
        n: Target number of operations

    Returns:
        str: Test case with approximately n operations
    """
    num_ops = max(3, n)
    operations = ["Trie"]
    arguments = [[]]

    for i in range(num_ops - 1):
        if i < num_ops // 2:
            # First half: inserts
            operations.append("insert")
            arguments.append([_random_word(random.randint(5, 20))])
        else:
            # Second half: searches
            op = random.choice(["search", "startsWith"])
            operations.append(op)
            arguments.append([_random_word(random.randint(3, 15))])

    return _format_case(operations, arguments)
