# solutions/0648_replace_words.py
"""
Problem: Replace Words
Link: https://leetcode.com/problems/replace-words/

In English, we have a concept called root, which can be followed by some other
word to form another longer word - let's call this word derivative. For example,
when the root "help" is followed by the word "ful", we can form a derivative "helpful".

Given a dictionary consisting of many roots and a sentence consisting of words
separated by spaces, replace all the derivatives in the sentence with the root
forming it. If a derivative can be replaced by more than one root, replace it
with the root that has the shortest length.

Example 1:
    Input: dictionary = ["cat","bat","rat"], sentence = "the cattle was rattled by the battery"
    Output: "the cat was rat by the bat"

Example 2:
    Input: dictionary = ["a","b","c"], sentence = "aadsfasf absbs bbab cadsfabd"
    Output: "a]b c"

Constraints:
- 1 <= dictionary.length <= 1000
- 1 <= dictionary[i].length <= 100
- dictionary[i] consists of only lower-case letters.
- 1 <= sentence.length <= 10^6
- sentence consists of only lower-case letters and spaces.
- The number of words in sentence is in the range [1, 1000]
- The length of each word in sentence is in the range [1, 1000]
- Every two consecutive words in sentence will be separated by exactly one space.
- sentence does not have leading or trailing spaces.

Topics: Array, Hash Table, String, Trie
"""
from typing import Dict, Optional, List, Any
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual: Any, expected: Any, input_data: str) -> bool:
    """Validate Replace Words solution."""
    if isinstance(actual, str) and isinstance(expected, str):
        return actual == expected
    return actual == expected


# ============================================
# SOLUTION 1: Trie-based Prefix Replacement
# ============================================
class TrieNode:
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end: bool = False


class Solution:
    """
    Use a Trie to efficiently find the shortest root for each word.

    For each word in the sentence:
    1. Traverse the trie character by character
    2. If we hit a node marked as end (is_end=True), we found the shortest root
    3. If we can't continue or reach end of word without finding a root, keep original

    Time Complexity: O(D * L + W * L) where D = dict size, W = words in sentence
    Space Complexity: O(D * L) for trie
    """

    def replaceWords(self, dictionary: List[str], sentence: str) -> str:
        # Build trie from dictionary
        root = TrieNode()
        for word in dictionary:
            node = root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.is_end = True

        def find_root(word: str) -> str:
            """Find shortest root for a word, or return original if none found."""
            node = root
            for i, char in enumerate(word):
                if char not in node.children:
                    return word  # No matching prefix
                node = node.children[char]
                if node.is_end:
                    return word[:i + 1]  # Found shortest root
            return word  # No root found

        # Process each word in sentence
        words = sentence.split()
        return ' '.join(find_root(word) for word in words)


# ============================================
# SOLUTION 2: Hash Set Approach (for comparison)
# ============================================
class SolutionHashSet:
    """
    Alternative approach using hash set.
    Check all prefixes of each word against the dictionary.

    Time Complexity: O(W * L^2) where W = words, L = max word length
    Space Complexity: O(D * L) for set

    Trie is faster when dictionary is large or words have long common prefixes.
    """

    def replaceWords(self, dictionary: List[str], sentence: str) -> str:
        dict_set = set(dictionary)

        def find_root(word: str) -> str:
            # Check prefixes from shortest to longest
            for i in range(1, len(word) + 1):
                prefix = word[:i]
                if prefix in dict_set:
                    return prefix
            return word

        words = sentence.split()
        return ' '.join(find_root(word) for word in words)


# ============================================
# SOLUTION METADATA
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "replaceWords",
    },
    "hashset": {
        "class": "SolutionHashSet",
        "method": "replaceWords",
    },
}


def solve(input_data: str, variant: str = "default") -> str:
    """
    Solve Replace Words.

    Input format:
    Line 1: JSON array of dictionary words
    Line 2: Sentence string
    """
    import json

    lines = input_data.strip().split('\n')
    dictionary = json.loads(lines[0])
    sentence = lines[1] if len(lines) > 1 else ""

    solver_class = Solution if variant == "default" else SolutionHashSet
    solver = solver_class()

    return solver.replaceWords(dictionary, sentence)


if __name__ == "__main__":
    test_input = '''["cat","bat","rat"]
the cattle was rattled by the battery'''

    result = solve(test_input)
    print(f"Result: {result}")
    expected = "the cat was rat by the bat"
    print(f"Expected: {expected}")
    print(f"Match: {result == expected}")

    # Test case 2
    test_input2 = '''["a","b","c"]
aadsfasf absbs bbab cadsfabd'''
    result2 = solve(test_input2)
    print(f"\nResult 2: {result2}")
    expected2 = "a a b c"
    print(f"Expected 2: {expected2}")
    print(f"Match: {result2 == expected2}")
