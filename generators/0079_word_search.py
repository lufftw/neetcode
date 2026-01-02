# generators/0079_word_search.py
"""
Test Case Generator for Problem 0079 - Word Search

LeetCode Constraints:
- m == board.length
- n == board[i].length
- 1 <= m, n <= 6
- 1 <= word.length <= 15
- board and word consists of only lowercase and uppercase English letters
"""
import json
import random
import string
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Word Search.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility
    
    Yields:
        str: Test input in the format: m,n\\nrow1\\nrow2\\n...\\nword
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        "3,4\nA,B,C,E\nS,F,C,S\nA,D,E,E\nABCCED",  # Classic True
        "3,4\nA,B,C,E\nS,F,C,S\nA,D,E,E\nSEE",      # True
        "3,4\nA,B,C,E\nS,F,C,S\nA,D,E,E\nABCB",     # False (reuse)
        "1,1\nA\nA",                                  # Single cell
    ]
    
    for edge in edge_cases:
        yield json.dumps(edge, separators=(",",":"))
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case."""
    m = random.randint(1, 6)
    n = random.randint(1, 6)
    
    # Generate random board
    letters = string.ascii_uppercase
    board = [[random.choice(letters) for _ in range(n)] for _ in range(m)]
    
    # Generate word - sometimes from board path, sometimes random
    if random.random() < 0.5:
        # Create a valid path word
        word_len = random.randint(1, min(8, m * n))
        word = _generate_valid_word(board, m, n, word_len)
    else:
        # Random word (may or may not exist)
        word_len = random.randint(1, 10)
        word = ''.join(random.choice(letters) for _ in range(word_len))
    
    # Format output
    lines = [f"{m},{n}"]
    for row in board:
        lines.append(','.join(row))
    lines.append(word)
    
    return '\n'.join(lines)


def _generate_valid_word(board, m, n, length):
    """Generate a word that exists in the board."""
    r, c = random.randint(0, m-1), random.randint(0, n-1)
    word = [board[r][c]]
    visited = {(r, c)}
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while len(word) < length:
        neighbors = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in visited:
                neighbors.append((nr, nc))
        
        if not neighbors:
            break
        
        r, c = random.choice(neighbors)
        visited.add((r, c))
        word.append(board[r][c])
    
    return ''.join(word)

