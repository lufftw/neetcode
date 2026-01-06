# generators/0212_word_search_ii.py
"""
Test Case Generator for Problem 0212 - Word Search II

LeetCode Constraints:
- m == board.length
- n == board[i].length
- 1 <= m, n <= 12
- board[i][j] is a lowercase English letter.
- 1 <= words.length <= 3 * 10^4
- 1 <= words[i].length <= 10
- words[i] consists of lowercase English letters.
- All the strings of words are unique.
"""
import json
import random
import string
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Word Search II.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Board and words in JSON format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # Example 1
        ([["o", "a", "a", "n"], ["e", "t", "a", "e"],
          ["i", "h", "k", "r"], ["i", "f", "l", "v"]],
         ["oath", "pea", "eat", "rain"]),
        # Example 2 - no match
        ([["a", "b"], ["c", "d"]], ["abcb"]),
        # Single cell
        ([["a"]], ["a", "b"]),
        # All same letter
        ([["a", "a"], ["a", "a"]], ["a", "aa", "aaa", "aaaa"]),
        # Long path
        ([["a", "b", "c"], ["d", "e", "f"], ["g", "h", "i"]],
         ["abc", "aei", "adg", "cfi", "ghi"]),
    ]

    for board, words in edge_cases:
        yield _format_case(board, words)
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _format_case(board: List[List[str]], words: List[str]) -> str:
    """Format a test case as input string."""
    return f"{json.dumps(board, separators=(',', ':'))}\n{json.dumps(words, separators=(',', ':'))}"


def _generate_random_case() -> str:
    """Generate a single random test case."""
    rows = random.randint(2, 8)
    cols = random.randint(2, 8)

    # Generate random board
    board = [[random.choice(string.ascii_lowercase) for _ in range(cols)]
             for _ in range(rows)]

    # Generate words - mix of findable and random
    words = set()

    # Add some words that exist in board (with high probability)
    for _ in range(random.randint(1, 5)):
        word = _extract_word_from_board(board, rows, cols)
        if word:
            words.add(word)

    # Add some random words
    for _ in range(random.randint(2, 8)):
        word = _random_word(random.randint(2, 6))
        words.add(word)

    return _format_case(board, list(words))


def _extract_word_from_board(board: List[List[str]], rows: int, cols: int) -> Optional[str]:
    """Extract a random valid word from the board via DFS."""
    start_r = random.randint(0, rows - 1)
    start_c = random.randint(0, cols - 1)
    length = random.randint(2, min(6, rows * cols))

    word = []
    visited = set()

    def dfs(r: int, c: int) -> bool:
        if len(word) == length:
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if (r, c) in visited:
            return False

        word.append(board[r][c])
        visited.add((r, c))

        # Try random direction
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)

        for dr, dc in directions:
            if dfs(r + dr, c + dc):
                return True

        word.pop()
        visited.remove((r, c))
        return False

    if dfs(start_r, start_c):
        return ''.join(word)
    return None


def _random_word(length: int) -> str:
    """Generate a random lowercase word."""
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    Args:
        n: Target board size (n = rows * cols)

    Returns:
        str: Test case with approximately n cells
    """
    side = max(2, int(n ** 0.5))
    rows = side
    cols = max(2, n // side)

    board = [[random.choice(string.ascii_lowercase) for _ in range(cols)]
             for _ in range(rows)]

    # Generate some words
    words = [_random_word(random.randint(2, 6)) for _ in range(min(10, n // 2))]

    return _format_case(board, words)
