# solutions/0208_implement_trie_prefix_tree.py
"""
Problem: Implement Trie (Prefix Tree)
Link: https://leetcode.com/problems/implement-trie-prefix-tree/

A trie (pronounced as "try") or prefix tree is a tree data structure used to
efficiently store and retrieve keys in a dataset of strings. There are various
applications of this data structure, such as autocomplete and spellchecker.

Implement the Trie class:
- Trie() Initializes the trie object.
- void insert(String word) Inserts the string word into the trie.
- boolean search(String word) Returns true if word is in the trie.
- boolean startsWith(String prefix) Returns true if any word starts with prefix.

Example 1:
    Input: ["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
           [[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
    Output: [null, null, true, false, true, null, true]

Constraints:
- 1 <= word.length, prefix.length <= 2000
- word and prefix consist only of lowercase English letters.
- At most 3 * 10^4 calls in total will be made to insert, search, and startsWith.

Topics: Hash Table, String, Design, Trie
"""
from typing import Dict, Optional, List, Any
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual: Any, expected: Any, input_data: str) -> bool:
    """Validate Trie operations."""
    # For design problems, compare operation results
    if isinstance(actual, list) and isinstance(expected, list):
        if len(actual) != len(expected):
            return False
        for a, e in zip(actual, expected):
            if a != e:
                return False
        return True
    return actual == expected


# ============================================
# SOLUTION 1: Basic Trie with Dictionary
# ============================================
class TrieNode:
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end: bool = False


class Trie:
    """
    Standard Trie implementation using dictionary for children.

    Time Complexity: O(L) for all operations where L = word length
    Space Complexity: O(N * L) for N words of average length L
    """

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Insert word into trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        """Return True if word exists in trie."""
        node = self._find_node(word)
        return node is not None and node.is_end

    def startsWith(self, prefix: str) -> bool:
        """Return True if any word starts with given prefix."""
        return self._find_node(prefix) is not None

    def _find_node(self, prefix: str) -> Optional[TrieNode]:
        """Navigate to node representing prefix, or None if not found."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node


# ============================================
# SOLUTION 2: Trie with Array (26 letters)
# ============================================
class TrieNodeArray:
    def __init__(self):
        self.children: List[Optional['TrieNodeArray']] = [None] * 26
        self.is_end: bool = False


class TrieArray:
    """
    Trie using fixed-size array for children (faster for lowercase letters only).

    Time Complexity: O(L) for all operations
    Space Complexity: O(N * L * 26) - more memory but faster access
    """

    def __init__(self):
        self.root = TrieNodeArray()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            idx = ord(char) - ord('a')
            if node.children[idx] is None:
                node.children[idx] = TrieNodeArray()
            node = node.children[idx]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self._find_node(word)
        return node is not None and node.is_end

    def startsWith(self, prefix: str) -> bool:
        return self._find_node(prefix) is not None

    def _find_node(self, prefix: str) -> Optional[TrieNodeArray]:
        node = self.root
        for char in prefix:
            idx = ord(char) - ord('a')
            if node.children[idx] is None:
                return None
            node = node.children[idx]
        return node


# ============================================
# SOLUTION METADATA
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Trie",
        "design_class": True,
    },
    "array": {
        "class": "TrieArray",
        "design_class": True,
    },
}


def solve(input_data: str, variant: str = "default") -> List[Any]:
    """
    Run Trie operations from input data.

    Input format:
    Line 1: JSON list of operations ["Trie", "insert", "search", ...]
    Line 2: JSON list of arguments [[], ["apple"], ["apple"], ...]
    """
    import json

    lines = input_data.strip().split('\n')
    operations = json.loads(lines[0])
    arguments = json.loads(lines[1])

    trie_class = Trie if variant == "default" else TrieArray
    result = []
    trie = None

    for op, args in zip(operations, arguments):
        if op == "Trie":
            trie = trie_class()
            result.append(None)
        elif op == "insert":
            trie.insert(args[0])
            result.append(None)
        elif op == "search":
            result.append(trie.search(args[0]))
        elif op == "startsWith":
            result.append(trie.startsWith(args[0]))

    return result


if __name__ == "__main__":
    # Test cases
    test_input = '''["Trie","insert","search","search","startsWith","insert","search"]
[[],["apple"],["apple"],["app"],["app"],["app"],["app"]]'''

    result = solve(test_input)
    print(f"Result: {result}")
    expected = [None, None, True, False, True, None, True]
    print(f"Expected: {expected}")
    print(f"Match: {result == expected}")
