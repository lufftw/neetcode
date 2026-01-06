# solutions/0212_word_search_ii.py
"""
Problem: Word Search II
Link: https://leetcode.com/problems/word-search-ii/

Given an m x n board of characters and a list of strings words, return all words
on the board. Each word must be constructed from letters of sequentially adjacent
cells, where adjacent cells are horizontally or vertically neighboring. The same
letter cell may not be used more than once in a word.

Example 1:
    Input: board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]],
           words = ["oath","pea","eat","rain"]
    Output: ["eat","oath"]

Example 2:
    Input: board = [["a","b"],["c","d"]], words = ["abcb"]
    Output: []

Constraints:
- m == board.length
- n == board[i].length
- 1 <= m, n <= 12
- board[i][j] is a lowercase English letter.
- 1 <= words.length <= 3 * 10^4
- 1 <= words[i].length <= 10
- words[i] consists of lowercase English letters.
- All the strings of words are unique.

Topics: Array, String, Backtracking, Trie, Matrix
"""
from typing import Dict, Optional, List, Set, Any
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual: Any, expected: Any, input_data: str) -> bool:
    """
    Validate Word Search II solution.
    Order doesn't matter, so compare as sets.
    """
    if isinstance(actual, list) and isinstance(expected, list):
        return set(actual) == set(expected)
    return actual == expected


# ============================================
# SOLUTION: Trie + Backtracking
# ============================================
class TrieNode:
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.word: Optional[str] = None  # Store complete word at end node


class Solution:
    """
    Build a Trie from words, then DFS from each cell in the grid.

    Key optimizations:
    1. Store complete word at end node (avoid reconstructing)
    2. Prune empty branches after finding words
    3. Use in-place marking for visited cells

    Time Complexity: O(M * N * 4^L) where L = max word length
    Space Complexity: O(W * L) for trie where W = number of words
    """

    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        if not board or not board[0] or not words:
            return []

        # Step 1: Build trie from words
        root = TrieNode()
        for word in words:
            node = root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.word = word  # Store complete word at end

        # Step 2: DFS from each cell
        rows, cols = len(board), len(board[0])
        result: List[str] = []

        def dfs(r: int, c: int, node: TrieNode) -> None:
            char = board[r][c]

            # Not a valid trie path
            if char not in node.children:
                return

            next_node = node.children[char]

            # Found a word!
            if next_node.word:
                result.append(next_node.word)
                next_node.word = None  # Avoid duplicates

            # Mark cell as visited
            board[r][c] = '#'

            # Explore 4 directions
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != '#':
                    dfs(nr, nc, next_node)

            # Restore cell
            board[r][c] = char

            # Optimization: prune empty trie branches
            if not next_node.children and not next_node.word:
                del node.children[char]

        # Start DFS from each cell
        for r in range(rows):
            for c in range(cols):
                dfs(r, c, root)

        return result


# ============================================
# SOLUTION 2: Without Trie Pruning (simpler)
# ============================================
class SolutionSimple:
    """
    Simpler version without branch pruning optimization.
    Easier to understand but slightly slower for large inputs.
    """

    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        if not board or not board[0] or not words:
            return []

        # Build trie
        root = TrieNode()
        for word in words:
            node = root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.word = word

        rows, cols = len(board), len(board[0])
        result: Set[str] = set()  # Use set to avoid duplicates

        def dfs(r: int, c: int, node: TrieNode) -> None:
            if r < 0 or r >= rows or c < 0 or c >= cols:
                return
            if board[r][c] == '#':
                return

            char = board[r][c]
            if char not in node.children:
                return

            next_node = node.children[char]
            if next_node.word:
                result.add(next_node.word)

            board[r][c] = '#'
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                dfs(r + dr, c + dc, next_node)
            board[r][c] = char

        for r in range(rows):
            for c in range(cols):
                dfs(r, c, root)

        return list(result)


# ============================================
# SOLUTION METADATA
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "findWords",
    },
    "simple": {
        "class": "SolutionSimple",
        "method": "findWords",
    },
}


def solve(input_data: str, variant: str = "default") -> List[str]:
    """
    Solve Word Search II.

    Input format:
    Line 1: JSON 2D array for board
    Line 2: JSON array of words
    """
    import json

    lines = input_data.strip().split('\n')
    board = json.loads(lines[0])
    words = json.loads(lines[1])

    solver_class = Solution if variant == "default" else SolutionSimple
    solver = solver_class()

    return solver.findWords(board, words)


if __name__ == "__main__":
    test_input = '''[["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]
["oath","pea","eat","rain"]'''

    result = solve(test_input)
    print(f"Result: {sorted(result)}")
    expected = ["eat", "oath"]
    print(f"Expected: {sorted(expected)}")
    print(f"Match: {set(result) == set(expected)}")
