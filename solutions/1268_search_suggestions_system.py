# solutions/1268_search_suggestions_system.py
"""
Problem: Search Suggestions System
Link: https://leetcode.com/problems/search-suggestions-system/

You are given an array of strings products and a string searchWord.

Design a system that suggests at most three product names from products after
each character of searchWord is typed. Suggested products should have common
prefix with searchWord. If there are more than three products with a common
prefix return the three lexicographically minimum products.

Return a list of lists of the suggested products after each character of
searchWord is typed.

Example 1:
    Input: products = ["mobile","mouse","moneypot","monitor","mousepad"], searchWord = "mouse"
    Output: [["mobile","moneypot","monitor"],
             ["mobile","moneypot","monitor"],
             ["mouse","mousepad"],
             ["mouse","mousepad"],
             ["mouse","mousepad"]]

Example 2:
    Input: products = ["havana"], searchWord = "havana"
    Output: [["havana"],["havana"],["havana"],["havana"],["havana"],["havana"]]

Constraints:
- 1 <= products.length <= 1000
- 1 <= products[i].length <= 3000
- 1 <= sum(products[i].length) <= 2 * 10^4
- All the strings of products are unique.
- products[i] consists of lowercase English letters.
- 1 <= searchWord.length <= 1000
- searchWord consists of lowercase English letters.

Topics: Array, String, Binary Search, Trie, Sorting, Heap
"""
from typing import Dict, Optional, List, Any
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual: Any, expected: Any, input_data: str) -> bool:
    """Validate Search Suggestions System solution."""
    if isinstance(actual, list) and isinstance(expected, list):
        if len(actual) != len(expected):
            return False
        for a, e in zip(actual, expected):
            if a != e:
                return False
        return True
    return actual == expected


# ============================================
# SOLUTION 1: Trie with Precomputed Suggestions
# ============================================
class TrieNode:
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.suggestions: List[str] = []  # Top 3 suggestions at this prefix


class Solution:
    """
    Build a Trie and store top 3 lexicographically smallest products at each node.

    Key insight: If we insert products in sorted order, the first 3 products
    reaching each node are the lexicographically smallest.

    Time Complexity: O(N * L * log N + N * L) for sorting + building
    Space Complexity: O(N * L) for trie with suggestions
    """

    def suggestedProducts(self, products: List[str], searchWord: str) -> List[List[str]]:
        # Sort products for lexicographical order
        products.sort()

        # Build trie with top-3 suggestions at each node
        root = TrieNode()
        for product in products:
            node = root
            for char in product:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
                # Keep only top 3 (input is already sorted)
                if len(node.suggestions) < 3:
                    node.suggestions.append(product)

        # Query for each prefix of searchWord
        result = []
        node = root
        for char in searchWord:
            if node and char in node.children:
                node = node.children[char]
                result.append(node.suggestions)
            else:
                # No more matches for this and remaining prefixes
                node = None
                result.append([])

        return result


# ============================================
# SOLUTION 2: Binary Search Approach
# ============================================
class SolutionBinarySearch:
    """
    Alternative approach using binary search on sorted products.

    For each prefix:
    1. Binary search to find first product >= prefix
    2. Check up to 3 products starting from that position

    Time Complexity: O(N log N + L * (log N + 3 * L))
    Space Complexity: O(1) extra space (excluding output)
    """

    def suggestedProducts(self, products: List[str], searchWord: str) -> List[List[str]]:
        import bisect

        products.sort()
        result = []
        prefix = ""

        for char in searchWord:
            prefix += char

            # Find first product >= prefix
            idx = bisect.bisect_left(products, prefix)

            # Collect up to 3 matching products
            suggestions = []
            for i in range(idx, min(idx + 3, len(products))):
                if products[i].startswith(prefix):
                    suggestions.append(products[i])
                else:
                    break

            result.append(suggestions)

        return result


# ============================================
# SOLUTION 3: Trie with DFS Collection
# ============================================
class TrieNodeDFS:
    def __init__(self):
        self.children: Dict[str, 'TrieNodeDFS'] = {}
        self.is_end: bool = False
        self.word: Optional[str] = None


class SolutionTrieDFS:
    """
    Build trie, then for each prefix, DFS to collect words in sorted order.

    Visiting children in sorted (alphabetical) order guarantees lexicographical
    ordering of results.
    """

    def suggestedProducts(self, products: List[str], searchWord: str) -> List[List[str]]:
        # Build trie
        root = TrieNodeDFS()
        for product in products:
            node = root
            for char in product:
                if char not in node.children:
                    node.children[char] = TrieNodeDFS()
                node = node.children[char]
            node.is_end = True
            node.word = product

        def collect_words(node: TrieNodeDFS, limit: int) -> List[str]:
            """DFS to collect up to 'limit' words in lex order."""
            words = []

            def dfs(n: TrieNodeDFS):
                if len(words) >= limit:
                    return
                if n.is_end and n.word:
                    words.append(n.word)
                # Visit children in sorted order for lex ordering
                for char in sorted(n.children.keys()):
                    if len(words) >= limit:
                        return
                    dfs(n.children[char])

            dfs(node)
            return words

        # Query each prefix
        result = []
        node = root

        for char in searchWord:
            if node and char in node.children:
                node = node.children[char]
                result.append(collect_words(node, 3))
            else:
                node = None
                result.append([])

        return result


# ============================================
# SOLUTION METADATA
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "suggestedProducts",
    },
    "binary_search": {
        "class": "SolutionBinarySearch",
        "method": "suggestedProducts",
    },
    "trie_dfs": {
        "class": "SolutionTrieDFS",
        "method": "suggestedProducts",
    },
}


def solve(input_data: str, variant: str = "default") -> List[List[str]]:
    """
    Solve Search Suggestions System.

    Input format:
    Line 1: JSON array of products
    Line 2: searchWord string
    """
    import json

    lines = input_data.strip().split('\n')
    products = json.loads(lines[0])
    searchWord = lines[1] if len(lines) > 1 else ""

    if variant == "default":
        solver = Solution()
    elif variant == "binary_search":
        solver = SolutionBinarySearch()
    else:
        solver = SolutionTrieDFS()

    return solver.suggestedProducts(products, searchWord)


if __name__ == "__main__":
    test_input = '''["mobile","mouse","moneypot","monitor","mousepad"]
mouse'''

    result = solve(test_input)
    print("Result:")
    for r in result:
        print(f"  {r}")

    expected = [
        ["mobile", "moneypot", "monitor"],
        ["mobile", "moneypot", "monitor"],
        ["mouse", "mousepad"],
        ["mouse", "mousepad"],
        ["mouse", "mousepad"]
    ]
    print("\nExpected:")
    for e in expected:
        print(f"  {e}")
    print(f"\nMatch: {result == expected}")
