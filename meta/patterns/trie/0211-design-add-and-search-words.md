## Problem: Design Add and Search Words Data Structure [LC 211]

> **Pattern**: Trie with Wildcard Search
> **Difficulty**: Medium
> **Delta from Base**: DFS for '.' wildcard matching

### Problem Statement

Design a data structure that supports adding words and searching with '.' wildcards that can match any letter.

### Invariant

**On '.', branch to ALL children; on letter, follow exact path.**

### Delta from Base Template

```python
# BASE: Linear traversal
def search(self, word: str) -> bool:
    node = self._find_node(word)
    return node is not None and node.is_end

# WILDCARD: DFS with branching on '.'
def search(self, word: str) -> bool:
    def dfs(node: TrieNode, i: int) -> bool:
        if i == len(word):
            return node.is_end

        char = word[i]
        if char == '.':
            # Try ALL children
            return any(dfs(child, i + 1) for child in node.children.values())
        else:
            # Follow exact path
            if char not in node.children:
                return False
            return dfs(node.children[char], i + 1)

    return dfs(self.root, 0)
```

### Complete Implementation

```python
class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.is_end: bool = False


class WordDictionary:
    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        """Same as base Trie insert."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        """Search with '.' wildcard support using DFS."""
        def dfs(node: TrieNode, i: int) -> bool:
            if i == len(word):
                return node.is_end

            char = word[i]
            if char == '.':
                # Wildcard: try all possible children
                for child in node.children.values():
                    if dfs(child, i + 1):
                        return True
                return False
            else:
                # Exact match required
                if char not in node.children:
                    return False
                return dfs(node.children[char], i + 1)

        return dfs(self.root, 0)
```

### Trace Example

```
addWord("bad"), addWord("dad"), addWord("mad")

Trie structure:
root → b → a → d (end)
     → d → a → d (end)
     → m → a → d (end)

search(".ad"):
  '.' matches 'b' → 'a' → 'd' → is_end=True → Return True

search("b.."):
  'b' → '.' matches 'a' → '.' matches 'd' → is_end=True → Return True

search("b.d"):
  'b' → '.' matches 'a' → 'd' → is_end=True → Return True
```

### Complexity

- **Time**: O(L) without wildcards, O(26^W × L) worst case with W wildcards
- **Space**: O(N × L) for trie + O(L) recursion stack

---
