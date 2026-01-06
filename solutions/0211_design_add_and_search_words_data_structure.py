# solutions/0211_design_add_and_search_words_data_structure.py
"""
Problem: Design Add and Search Words Data Structure
Link: https://leetcode.com/problems/design-add-and-search-words-data-structure/

Design a data structure that supports adding new words and finding if a string
matches any previously added string.

Implement the WordDictionary class:
- WordDictionary() Initializes the object.
- void addWord(word) Adds word to the data structure.
- bool search(word) Returns true if there is any string that matches word.
  word may contain dots '.' where dots can match any letter.

Example 1:
    Input: ["WordDictionary","addWord","addWord","addWord","search","search","search","search"]
           [[],["bad"],["dad"],["mad"],["pad"],["bad"],[".ad"],["b.."]]
    Output: [null,null,null,null,false,true,true,true]

Constraints:
- 1 <= word.length <= 25
- word in addWord consists of lowercase English letters.
- word in search consists of '.' or lowercase English letters.
- There will be at most 2 dots in word for search queries.
- At most 10^4 calls will be made to addWord and search.

Topics: String, Depth-First Search, Design, Trie
"""
from typing import Dict, Optional, List, Any
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual: Any, expected: Any, input_data: str) -> bool:
    """Validate WordDictionary operations."""
    if isinstance(actual, list) and isinstance(expected, list):
        if len(actual) != len(expected):
            return False
        for a, e in zip(actual, expected):
            if a != e:
                return False
        return True
    return actual == expected


# ============================================
# SOLUTION: Trie with DFS for Wildcard Search
# ============================================
class TrieNode:
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end: bool = False


class WordDictionary:
    """
    Trie-based dictionary with wildcard '.' search support.

    The key insight is that '.' can match any single character, so we need
    to try all possible children when we encounter a dot.

    Time Complexity:
        - addWord: O(L) where L = word length
        - search: O(L) without dots, O(26^D * L) with D dots

    Space Complexity: O(N * L) for N words of average length L
    """

    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        """Add a word to the dictionary."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        """
        Search for word with '.' wildcard support.

        '.' can match any single letter, so we use DFS to try all
        possible paths when encountering a dot.
        """
        def dfs(node: TrieNode, i: int) -> bool:
            # Reached end of word
            if i == len(word):
                return node.is_end

            char = word[i]

            if char == '.':
                # Wildcard: try ALL children
                for child in node.children.values():
                    if dfs(child, i + 1):
                        return True
                return False
            else:
                # Exact character: follow specific path
                if char not in node.children:
                    return False
                return dfs(node.children[char], i + 1)

        return dfs(self.root, 0)


# ============================================
# SOLUTION 2: Iterative with Stack
# ============================================
class WordDictionaryIterative:
    """
    Same logic but using explicit stack instead of recursion.
    Useful when recursion depth might be a concern.
    """

    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        # Stack contains (node, index) pairs
        stack = [(self.root, 0)]

        while stack:
            node, i = stack.pop()

            if i == len(word):
                if node.is_end:
                    return True
                continue

            char = word[i]

            if char == '.':
                # Push all children to explore
                for child in node.children.values():
                    stack.append((child, i + 1))
            else:
                if char in node.children:
                    stack.append((node.children[char], i + 1))

        return False


# ============================================
# SOLUTION METADATA
# ============================================
SOLUTIONS = {
    "default": {
        "class": "WordDictionary",
        "design_class": True,
    },
    "iterative": {
        "class": "WordDictionaryIterative",
        "design_class": True,
    },
}


def solve(input_data: str, variant: str = "default") -> List[Any]:
    """Run WordDictionary operations from input data."""
    import json

    lines = input_data.strip().split('\n')
    operations = json.loads(lines[0])
    arguments = json.loads(lines[1])

    dict_class = WordDictionary if variant == "default" else WordDictionaryIterative
    result = []
    word_dict = None

    for op, args in zip(operations, arguments):
        if op == "WordDictionary":
            word_dict = dict_class()
            result.append(None)
        elif op == "addWord":
            word_dict.addWord(args[0])
            result.append(None)
        elif op == "search":
            result.append(word_dict.search(args[0]))

    return result


if __name__ == "__main__":
    test_input = '''["WordDictionary","addWord","addWord","addWord","search","search","search","search"]
[[],["bad"],["dad"],["mad"],["pad"],["bad"],[".ad"],["b.."]]'''

    result = solve(test_input)
    print(f"Result: {result}")
    expected = [None, None, None, None, False, True, True, True]
    print(f"Expected: {expected}")
    print(f"Match: {result == expected}")
