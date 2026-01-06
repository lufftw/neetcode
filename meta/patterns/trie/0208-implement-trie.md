## Problem: Implement Trie (Prefix Tree) [LC 208] - BASE

> **Pattern**: Basic Trie Operations
> **Difficulty**: Medium
> **Role**: Base template for all Trie problems

### Problem Statement

Implement a trie with `insert`, `search`, and `startsWith` methods.

### Invariant

**A path from root represents a prefix; `is_end` marks complete words.**

### Template Implementation

```python
class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.is_end: bool = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Insert word into trie. O(L) time."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        """Return True if word is in trie. O(L) time."""
        node = self._find_node(word)
        return node is not None and node.is_end

    def startsWith(self, prefix: str) -> bool:
        """Return True if any word starts with prefix. O(L) time."""
        return self._find_node(prefix) is not None

    def _find_node(self, prefix: str) -> Optional[TrieNode]:
        """Navigate to node representing prefix, or None if not found."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
```

### Trace Example

```
Insert: "apple", "app"

After "apple":
root → a → p → p → l → e (is_end=True)

After "app":
root → a → p → p (is_end=True) → l → e (is_end=True)
              ↑
          Now marked as end

search("app")    → True  (node exists AND is_end=True)
search("appl")   → False (node exists BUT is_end=False)
startsWith("ap") → True  (node exists)
```

### Key Insights

1. **Space Efficiency**: Shared prefixes use shared nodes
2. **Time Complexity**: O(L) for all operations, independent of dictionary size
3. **Trade-off**: Uses more space than hash set but enables prefix operations

### Complexity

- **Time**: O(L) per operation where L = string length
- **Space**: O(N × L) worst case for N words of length L

---
