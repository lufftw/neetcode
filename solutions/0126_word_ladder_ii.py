"""
Problem: Word Ladder II
Link: https://leetcode.com/problems/word-ladder-ii/

Find ALL shortest transformation sequences from beginWord to endWord. Each step
changes exactly one letter, and all intermediate words must be in wordList.

Constraints:
- 1 <= beginWord.length <= 5
- 1 <= wordList.length <= 500
- beginWord != endWord
- All words same length, lowercase letters

Topics: Hash Table, String, Backtracking, Breadth First Search
"""
from typing import List
from collections import defaultdict
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "findLadders",
        "complexity": "O(n * m * 26) time, O(n * m) space",
        "description": "BFS to build parent graph + DFS backtracking",
    },
}


# JUDGE_FUNC for generated tests (order of paths may vary)
def _reference(beginWord: str, endWord: str, wordList: List[str]) -> List[List[str]]:
    """Reference implementation."""
    word_set = set(wordList)
    if endWord not in word_set:
        return []
    parents = defaultdict(set)
    current = {beginWord}
    visited = {beginWord}
    found = False
    while current and not found:
        nxt = set()
        for w in current:
            for i in range(len(w)):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    if c == w[i]:
                        continue
                    nw = w[:i] + c + w[i+1:]
                    if nw not in word_set:
                        continue
                    if nw not in visited:
                        nxt.add(nw)
                        parents[nw].add(w)
                        if nw == endWord:
                            found = True
                    elif nw in nxt:
                        parents[nw].add(w)
        visited |= nxt
        current = nxt
    if not found:
        return []
    result = []
    path = [endWord]
    def dfs(w):
        if w == beginWord:
            result.append(path[::-1])
            return
        for p in parents[w]:
            path.append(p)
            dfs(p)
            path.pop()
    dfs(endWord)
    return result


def judge(actual, expected, input_data: str) -> bool:
    lines = input_data.strip().split('\n')
    beginWord = json.loads(lines[0])
    endWord = json.loads(lines[1])
    wordList = json.loads(lines[2])
    if isinstance(actual, str):
        actual = json.loads(actual)
    # Compare as sets of tuples (order doesn't matter)
    actual_set = {tuple(p) for p in actual}
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        expected_set = {tuple(p) for p in expected}
        return actual_set == expected_set
    ref = _reference(beginWord, endWord, wordList)
    ref_set = {tuple(p) for p in ref}
    return actual_set == ref_set


JUDGE_FUNC = judge


# ============================================================================
# Solution: BFS + DFS Backtracking
# Time: O(n * m * 26) for BFS, Space: O(n * m) for parent graph
# ============================================================================
class Solution:
    # Key insight:
    #   - BFS finds shortest distance level by level
    #   - Track ALL parents at shortest distance for each word
    #   - After BFS, DFS from endWord back to beginWord using parent graph
    #
    # Why level-by-level BFS:
    #   - Need to capture multiple parents at same level
    #   - Once we move to next level, we mark current level as visited
    #   - This prevents longer paths from adding incorrect parents

    def findLadders(self, beginWord: str, endWord: str, wordList: List[str]) -> List[List[str]]:
        word_set = set(wordList)
        if endWord not in word_set:
            return []

        # parents[word] = set of words that can reach it at shortest distance
        parents = defaultdict(set)

        # BFS level by level
        current_level = {beginWord}
        visited = {beginWord}
        found = False

        while current_level and not found:
            next_level = set()

            for word in current_level:
                for i in range(len(word)):
                    for c in 'abcdefghijklmnopqrstuvwxyz':
                        if c == word[i]:
                            continue
                        next_word = word[:i] + c + word[i+1:]

                        if next_word not in word_set:
                            continue

                        if next_word not in visited:
                            next_level.add(next_word)
                            parents[next_word].add(word)
                            if next_word == endWord:
                                found = True
                        elif next_word in next_level:
                            # Same level, different parent - add it
                            parents[next_word].add(word)

            visited |= next_level
            current_level = next_level

        if not found:
            return []

        # DFS to collect all paths from endWord to beginWord
        result = []
        path = [endWord]

        def dfs(word: str) -> None:
            if word == beginWord:
                result.append(path[::-1])
                return
            for parent in parents[word]:
                path.append(parent)
                dfs(parent)
                path.pop()

        dfs(endWord)
        return result


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: beginWord (JSON string)
        Line 2: endWord (JSON string)
        Line 3: wordList (JSON array)

    Example:
        "hit"
        "cog"
        ["hot","dot","dog","lot","log","cog"]
        -> [["hit","hot","dot","dog","cog"],["hit","hot","lot","log","cog"]]
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    beginWord = json.loads(lines[0])
    endWord = json.loads(lines[1])
    wordList = json.loads(lines[2])

    solver = get_solver(SOLUTIONS)
    result = solver.findLadders(beginWord, endWord, wordList)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
