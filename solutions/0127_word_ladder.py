# solutions/0127_word_ladder.py
"""
Problem: Word Ladder
https://leetcode.com/problems/word-ladder/

Given two words beginWord and endWord, and a dictionary wordList, return the
number of words in the shortest transformation sequence from beginWord to
endWord. Return 0 if no such sequence exists.

Transformation rules:
- Only one letter can be changed at a time
- Each intermediate word must exist in wordList

Constraints:
- 1 <= beginWord.length <= 10
- endWord.length == beginWord.length
- 1 <= wordList.length <= 5000
- wordList[i].length == beginWord.length
- All words consist of lowercase English letters
- beginWord != endWord
- All words in wordList are unique
"""
from typing import List
from collections import deque
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionBFS",
        "method": "ladderLength",
        "complexity": "O(n * m^2) time, O(n * m) space",
        "description": "BFS with pattern-based neighbor lookup",
    },
    "bidirectional": {
        "class": "SolutionBidirectional",
        "method": "ladderLength",
        "complexity": "O(n * m^2) time, O(n * m) space",
        "description": "Bidirectional BFS for reduced search space",
    },
}


class SolutionBFS:
    """
    Standard BFS treating word transformations as graph edges.

    We preprocess wordList into a pattern dictionary where each pattern
    represents a word with one character wildcarded (e.g., "hit" -> "*it",
    "h*t", "hi*"). This enables O(m) neighbor lookup instead of O(n*m).

    BFS guarantees shortest path in unweighted graphs. Each level of BFS
    corresponds to one transformation step, so the first time we reach
    endWord gives the minimum transformation length.
    """

    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        # Early termination: target must be reachable
        word_set = set(wordList)
        if endWord not in word_set:
            return 0

        # Build pattern dictionary for O(m) neighbor lookup
        # Pattern "h*t" maps to all words matching that pattern
        m = len(beginWord)
        pattern_to_words = {}

        # Include beginWord in pattern mapping
        all_words = list(word_set) + [beginWord]
        for word in all_words:
            for i in range(m):
                pattern = word[:i] + "*" + word[i + 1 :]
                if pattern not in pattern_to_words:
                    pattern_to_words[pattern] = []
                pattern_to_words[pattern].append(word)

        # BFS from beginWord to endWord
        queue = deque([(beginWord, 1)])  # (word, transformation_count)
        visited = {beginWord}

        while queue:
            word, steps = queue.popleft()

            # Generate all patterns for current word
            for i in range(m):
                pattern = word[:i] + "*" + word[i + 1 :]

                # Check all words matching this pattern
                for neighbor in pattern_to_words.get(pattern, []):
                    if neighbor == endWord:
                        return steps + 1

                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, steps + 1))

        return 0


class SolutionBidirectional:
    """
    Bidirectional BFS meeting in the middle for reduced search space.

    Instead of searching from one end, we maintain two frontiers: one
    expanding from beginWord, one from endWord. At each step, we expand
    the smaller frontier to minimize branching factor.

    This technique transforms O(b^d) to O(2 * b^(d/2)) where b is the
    branching factor and d is the depth. For word ladders with high
    connectivity, this provides significant speedup.
    """

    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        word_set = set(wordList)
        if endWord not in word_set:
            return 0

        # Initialize two frontiers
        front = {beginWord}
        back = {endWord}
        visited = {beginWord, endWord}
        m = len(beginWord)
        steps = 1

        while front and back:
            # Always expand smaller frontier for efficiency
            # This balances the search and minimizes total nodes explored
            if len(front) > len(back):
                front, back = back, front

            next_front = set()

            for word in front:
                # Generate all one-letter variations
                for i in range(m):
                    for c in "abcdefghijklmnopqrstuvwxyz":
                        if c == word[i]:
                            continue

                        neighbor = word[:i] + c + word[i + 1 :]

                        # Check if frontiers meet
                        if neighbor in back:
                            return steps + 1

                        # Add valid unvisited neighbors to next frontier
                        if neighbor in word_set and neighbor not in visited:
                            visited.add(neighbor)
                            next_front.add(neighbor)

            front = next_front
            steps += 1

        return 0


def judge(actual, expected, input_data: str) -> bool:
    """
    Validate word ladder length using BFS.
    Computes expected shortest path independently.
    """
    import json

    lines = input_data.strip().split("\n")
    begin_word = json.loads(lines[0])
    end_word = json.loads(lines[1])
    word_list = json.loads(lines[2])

    # Compute expected using BFS
    word_set = set(word_list)
    if end_word not in word_set:
        return actual == 0

    queue = deque([(begin_word, 1)])
    visited = {begin_word}
    m = len(begin_word)

    while queue:
        word, steps = queue.popleft()
        for i in range(m):
            for c in "abcdefghijklmnopqrstuvwxyz":
                if c == word[i]:
                    continue
                neighbor = word[:i] + c + word[i + 1 :]
                if neighbor == end_word:
                    return actual == steps + 1
                if neighbor in word_set and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, steps + 1))

    return actual == 0


JUDGE_FUNC = judge


def solve():
    import sys
    import json

    lines = sys.stdin.read().strip().split("\n")

    # Parse input: beginWord, endWord, wordList
    begin_word = json.loads(lines[0])
    end_word = json.loads(lines[1])
    word_list = json.loads(lines[2])

    # Get solver and find ladder length
    solver = get_solver(SOLUTIONS)
    result = solver.ladderLength(begin_word, end_word, word_list)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
