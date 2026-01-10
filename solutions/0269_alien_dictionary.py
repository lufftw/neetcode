# solutions/0269_alien_dictionary.py
"""
Problem: Alien Dictionary
https://leetcode.com/problems/alien-dictionary/

Given a sorted list of words in an alien language, determine the character
ordering. Return "" if no valid ordering exists (cycle or invalid input).

Key insight: Compare adjacent words to extract ordering constraints.
The first differing character between word[i] and word[i+1] tells us which
char comes before which. Build a directed graph and topologically sort.

Constraints:
- 1 <= words.length <= 100
- 1 <= words[i].length <= 100
- words[i] consists of only lowercase English letters
"""
import json
import sys
from collections import defaultdict, deque
from typing import List

from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionBFS",
        "method": "alienOrder",
        "complexity": "O(C) time, O(1) space",
        "description": "BFS topological sort (Kahn's algorithm)",
    },
    "dfs": {
        "class": "SolutionDFS",
        "method": "alienOrder",
        "complexity": "O(C) time, O(1) space",
        "description": "DFS topological sort with cycle detection",
    },
}


class SolutionBFS:
    """
    BFS topological sort (Kahn's algorithm).

    WHY: Topological sort gives a valid ordering of nodes in a DAG.
    Compare adjacent words to build a graph of character precedence.
    BFS processes chars with no incoming edges first, naturally yielding
    the ordering. Detects cycles if not all chars are processed.

    HOW:
    1. Collect all unique chars and build adjacency list from word comparisons
    2. Track in-degree for each char
    3. Start BFS with chars having in-degree 0
    4. Process each char, reducing neighbor in-degrees
    5. If result contains all chars, valid ordering; else cycle exists
    """

    def alienOrder(self, words: List[str]) -> str:
        # Collect all unique characters
        chars = set()
        for word in words:
            chars.update(word)

        # Build graph: adjacency list and in-degrees
        adj = defaultdict(set)
        in_degree = {c: 0 for c in chars}

        # Compare adjacent words to extract ordering
        for i in range(len(words) - 1):
            word1, word2 = words[i], words[i + 1]

            # Check for invalid case: prefix comes after longer word
            if len(word1) > len(word2) and word1[:len(word2)] == word2:
                return ""

            # Find first differing character
            for c1, c2 in zip(word1, word2):
                if c1 != c2:
                    # c1 comes before c2
                    if c2 not in adj[c1]:
                        adj[c1].add(c2)
                        in_degree[c2] += 1
                    break

        # BFS (Kahn's algorithm)
        queue = deque([c for c in chars if in_degree[c] == 0])
        result = []

        while queue:
            c = queue.popleft()
            result.append(c)

            for neighbor in adj[c]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # If not all chars in result, there's a cycle
        if len(result) != len(chars):
            return ""

        return "".join(result)


class SolutionDFS:
    """
    DFS topological sort with cycle detection.

    WHY: DFS naturally produces reverse topological order when we add
    nodes to result after visiting all descendants. Cycle detection
    via tracking nodes in current recursion path.

    HOW:
    1. Build graph from word comparisons
    2. DFS each unvisited node, tracking visited (completed) and path (current)
    3. If we hit a node in current path, cycle detected
    4. Add node to result after processing all descendants
    5. Reverse result for correct order
    """

    def alienOrder(self, words: List[str]) -> str:
        # Collect all unique characters
        chars = set()
        for word in words:
            chars.update(word)

        # Build graph
        adj = defaultdict(set)

        for i in range(len(words) - 1):
            word1, word2 = words[i], words[i + 1]

            # Invalid: prefix comes after longer word
            if len(word1) > len(word2) and word1[:len(word2)] == word2:
                return ""

            for c1, c2 in zip(word1, word2):
                if c1 != c2:
                    adj[c1].add(c2)
                    break

        # DFS with cycle detection
        # State: 0 = unvisited, 1 = in current path, 2 = completed
        state = {c: 0 for c in chars}
        result = []

        def dfs(c: str) -> bool:
            if state[c] == 1:  # Cycle detected
                return False
            if state[c] == 2:  # Already processed
                return True

            state[c] = 1  # Mark as in current path

            for neighbor in adj[c]:
                if not dfs(neighbor):
                    return False

            state[c] = 2  # Mark as completed
            result.append(c)  # Add to result (reverse order)
            return True

        # Process all characters
        for c in chars:
            if state[c] == 0:
                if not dfs(c):
                    return ""

        return "".join(reversed(result))


def judge(actual, expected, input_data: str) -> bool:
    """
    Validate alien dictionary result.
    Multiple valid orderings may exist, so we verify the output is consistent.
    """
    if isinstance(actual, str):
        # Handle JSON string (e.g., "\"wertf\"")
        if actual.startswith('"'):
            actual = json.loads(actual)

    words = json.loads(input_data.strip())

    # Use reference to check if problem is solvable
    ref_result = _alien_order_ref(words)

    # If reference returns "", actual must also return ""
    if ref_result == "":
        return actual == ""

    # Otherwise, validate actual is a valid ordering
    return _is_valid_order(actual, words)


def _alien_order_ref(words: List[str]) -> str:
    """Reference implementation using BFS."""
    chars = set()
    for word in words:
        chars.update(word)

    adj = defaultdict(set)
    in_degree = {c: 0 for c in chars}

    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        if len(w1) > len(w2) and w1[:len(w2)] == w2:
            return ""
        for c1, c2 in zip(w1, w2):
            if c1 != c2:
                if c2 not in adj[c1]:
                    adj[c1].add(c2)
                    in_degree[c2] += 1
                break

    queue = deque([c for c in chars if in_degree[c] == 0])
    result = []

    while queue:
        c = queue.popleft()
        result.append(c)
        for neighbor in adj[c]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return "".join(result) if len(result) == len(chars) else ""


def _is_valid_order(order: str, words: List[str]) -> bool:
    """Check if order is a valid alien ordering for the given words."""
    if not order:
        return False

    # Get all chars that should be in the order
    all_chars = set()
    for word in words:
        all_chars.update(word)

    # Order must contain exactly these chars
    if set(order) != all_chars:
        return False

    # Build char position map
    pos = {c: i for i, c in enumerate(order)}

    # Verify words are sorted according to this order
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        for c1, c2 in zip(w1, w2):
            if c1 != c2:
                if pos[c1] > pos[c2]:
                    return False
                break
        else:
            # All compared chars equal, shorter word must come first
            if len(w1) > len(w2):
                return False

    return True


JUDGE_FUNC = judge


def solve():
    lines = sys.stdin.read().strip().split("\n")
    words = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.alienOrder(words)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
