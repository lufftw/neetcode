## Problem: Search Suggestions System [LC 1268]

> **Pattern**: Trie Autocomplete
> **Difficulty**: Medium
> **Delta from Base**: Collect top-k words with given prefix

### Problem Statement

Given an array of products and a search word, return for each prefix of the search word up to 3 lexicographically smallest products that match the prefix.

### Invariant

**For each prefix, DFS from prefix node to collect words in sorted order.**

### Approach Options

| Approach | Build | Query per Prefix | Best When |
|----------|-------|------------------|-----------|
| Sort + Binary Search | O(N log N) | O(log N + K) | Few queries |
| **Trie + DFS** | O(N × L) | O(K) | Many queries |
| Trie + Precomputed | O(N × L × K) | O(1) | Very many queries |

### Template Implementation

```python
class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.words: List[str] = []  # Store up to 3 words at each node


class Solution:
    def suggestedProducts(self, products: List[str], searchWord: str) -> List[List[str]]:
        # Sort products for lexicographical order
        products.sort()

        # Build trie with top-3 words at each node
        root = TrieNode()
        for product in products:
            node = root
            for char in product:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
                # Keep only top 3 (already sorted)
                if len(node.words) < 3:
                    node.words.append(product)

        # Query for each prefix
        result = []
        node = root
        for i, char in enumerate(searchWord):
            if node and char in node.children:
                node = node.children[char]
                result.append(node.words)
            else:
                # No more matches for this and remaining prefixes
                node = None
                result.append([])

        return result
```

### Alternative: DFS Collection

```python
def suggestedProducts(self, products: List[str], searchWord: str) -> List[List[str]]:
    # Build basic trie
    root = TrieNode()
    for product in products:
        node = root
        for char in product:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.word = product

    def collect_words(node: TrieNode, limit: int) -> List[str]:
        """DFS to collect up to 'limit' words in lex order."""
        words = []

        def dfs(n: TrieNode):
            if len(words) >= limit:
                return
            if hasattr(n, 'word') and n.word:
                words.append(n.word)
            # Visit children in sorted order for lex ordering
            for char in sorted(n.children.keys()):
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
```

### Trace Example

```
products = ["mobile","mouse","moneypot","monitor","mousepad"]
searchWord = "mouse"

Sorted: ["mobile","moneypot","monitor","mouse","mousepad"]

Trie with top-3 words at each node:
root
  → m: ["mobile","moneypot","monitor"]
    → o: ["mobile","moneypot","monitor"]
      → b: ["mobile"]
      → n: ["moneypot","monitor"]
      → u: ["mouse","mousepad"]
        → s: ["mouse","mousepad"]
          → e: ["mouse","mousepad"]

Query "m": ["mobile","moneypot","monitor"]
Query "mo": ["mobile","moneypot","monitor"]
Query "mou": ["mouse","mousepad"]
Query "mous": ["mouse","mousepad"]
Query "mouse": ["mouse","mousepad"]
```

### Key Insight: Pre-store vs. Collect

**Pre-store (implemented above)**:
- Store top-3 at each node during build
- O(1) query but O(N × L) extra space

**Collect on demand**:
- DFS from prefix node each query
- O(K) per query, less space

### Complexity

- **Time**: O(N × L × log N) for build (sorting), O(L) per query
- **Space**: O(N × L) for trie + O(3 × L) for stored suggestions

---
