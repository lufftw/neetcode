"""
Problem: Word Break
Link: https://leetcode.com/problems/word-break/

Given a string s and a dictionary of strings wordDict, return true if s can be
segmented into a space-separated sequence of one or more dictionary words.

Note that the same word in the dictionary may be reused multiple times.

Example 1:
    Input: s = "leetcode", wordDict = ["leet","code"]
    Output: true
    Explanation: Return true because "leetcode" can be segmented as "leet code".

Example 2:
    Input: s = "applepenapple", wordDict = ["apple","pen"]
    Output: true
    Explanation: "applepenapple" can be segmented as "apple pen apple".

Example 3:
    Input: s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
    Output: false

Constraints:
- 1 <= s.length <= 300
- 1 <= wordDict.length <= 1000
- 1 <= wordDict[i].length <= 20
- s and wordDict[i] consist of only lowercase English letters.

Topics: Array, Hash Table, String, Dynamic Programming, Trie, Memoization
"""
import json
from collections import deque
from functools import lru_cache
from typing import List
from _runner import get_solver


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionDP",
        "method": "wordBreak",
        "complexity": "O(n^2 * m) time, O(n) space",
        "description": "Bottom-up DP with hash set lookup",
    },
    "dp": {
        "class": "SolutionDP",
        "method": "wordBreak",
        "complexity": "O(n^2 * m) time, O(n) space",
        "description": "Bottom-up DP",
    },
    "bfs": {
        "class": "SolutionBFS",
        "method": "wordBreak",
        "complexity": "O(n^2 * m) time, O(n) space",
        "description": "BFS exploration of valid segmentations",
    },
    "memo": {
        "class": "SolutionMemo",
        "method": "wordBreak",
        "complexity": "O(n^2 * m) time, O(n) space",
        "description": "Top-down with memoization",
    },
}


# ============================================================================
# Solution 1: Dynamic Programming (Bottom-Up)
# Time: O(n^2 * m) where n = len(s), m = average word length for substring check
# Space: O(n + k) where k = total characters in wordDict
#   - dp[i] = True if s[0:i] can be segmented
#   - For each position, check all words that could end there
# ============================================================================
class SolutionDP:
    """
    Bottom-up dynamic programming approach.

    State: dp[i] = True if s[0:i] can be segmented into dictionary words
    Base case: dp[0] = True (empty prefix is valid)

    Transition: dp[i] = True if for some j < i:
        - dp[j] is True (prefix s[0:j] is valid)
        - s[j:i] is in wordDict (remaining part is a word)

    We use a set for O(1) word lookup and optimize by only checking
    substrings whose length matches some word in the dictionary.
    """

    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        word_set = set(wordDict)
        n = len(s)

        # dp[i] = True if s[0:i] can be segmented
        dp = [False] * (n + 1)
        dp[0] = True  # Empty string is valid

        for i in range(1, n + 1):
            for j in range(i):
                # If prefix s[0:j] is valid and s[j:i] is a word
                if dp[j] and s[j:i] in word_set:
                    dp[i] = True
                    break  # Found valid segmentation, no need to continue

        return dp[n]


# ============================================================================
# Solution 2: BFS (Breadth-First Search)
# Time: O(n^2 * m), Space: O(n)
#   - Treat as graph where each position is a node
#   - Edge exists from i to j if s[i:j] is in wordDict
#   - BFS from 0 to find if we can reach n
# ============================================================================
class SolutionBFS:
    """
    BFS approach - explore all valid segmentation points.

    Think of it as a graph problem:
    - Nodes are positions 0 to n
    - There's an edge from i to j if s[i:j] is a valid word
    - We want to find a path from 0 to n

    BFS explores positions level by level. Each visited position
    represents a valid segmentation point.
    """

    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        word_set = set(wordDict)
        n = len(s)

        queue = deque([0])  # Start from position 0
        visited = set([0])

        while queue:
            start = queue.popleft()

            if start == n:
                return True

            # Try all possible words starting at 'start'
            for end in range(start + 1, n + 1):
                if end not in visited and s[start:end] in word_set:
                    visited.add(end)
                    queue.append(end)

        return False


# ============================================================================
# Solution 3: Memoization (Top-Down)
# Time: O(n^2 * m), Space: O(n)
#   - Recursive with caching
#   - canBreak(i) = can s[i:] be segmented?
# ============================================================================
class SolutionMemo:
    """
    Top-down dynamic programming with memoization.

    canBreak(i) = True if s[i:] (suffix starting at i) can be segmented.

    At each position i, try all words from the dictionary:
    - If word matches s[i:i+len(word)]
    - And canBreak(i + len(word)) is True
    - Then canBreak(i) is True

    Uses LRU cache for memoization.
    """

    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        word_set = set(wordDict)
        n = len(s)

        @lru_cache(maxsize=None)
        def canBreak(start: int) -> bool:
            # Base case: successfully segmented entire string
            if start == n:
                return True

            # Try each possible word at current position
            for end in range(start + 1, n + 1):
                word = s[start:end]
                if word in word_set and canBreak(end):
                    return True

            return False

        return canBreak(0)


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: s as JSON string
        Line 2: wordDict as JSON array

    Example:
        "leetcode"
        ["leet","code"]
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')

    s = json.loads(lines[0])
    wordDict = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.wordBreak(s, wordDict)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
