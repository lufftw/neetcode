## Problem: Replace Words [LC 648]

> **Pattern**: Trie Prefix Replacement
> **Difficulty**: Medium
> **Delta from Base**: Find shortest matching prefix

### Problem Statement

Given a dictionary of roots and a sentence, replace each word with its shortest root. If a word has no root, keep it unchanged.

Example: dictionary = ["cat", "bat", "rat"], sentence = "the cattle was rattled by the battery"
Output: "the cat was rat by the bat"

### Invariant

**For each word, find the shortest prefix that exists in trie.**

### Delta from Base Template

```python
# BASE: Check if full word exists
def search(self, word: str) -> bool:
    node = self._find_node(word)
    return node is not None and node.is_end

# REPLACE: Find shortest prefix that is a complete word
def find_shortest_root(self, word: str) -> str:
    node = self.root
    for i, char in enumerate(word):
        if char not in node.children:
            break  # No prefix exists
        node = node.children[char]
        if node.is_end:
            return word[:i + 1]  # Found shortest root!
    return word  # No root found, return original
```

### Complete Implementation

```python
class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.is_end: bool = False


class Solution:
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
            """Find shortest root for a word."""
            node = root
            for i, char in enumerate(word):
                if char not in node.children:
                    return word  # No matching prefix
                node = node.children[char]
                if node.is_end:
                    return word[:i + 1]  # Return shortest root
            return word  # No root found

        # Replace each word in sentence
        words = sentence.split()
        return ' '.join(find_root(word) for word in words)
```

### Trace Example

```
dictionary = ["cat", "bat", "rat"]
sentence = "the cattle was rattled by the battery"

Trie:
root → c → a → t (end)
     → b → a → t (end)
     → r → a → t (end)

Processing "cattle":
  'c' → found in trie
  'a' → found, continue
  't' → found, is_end=True! Return "cat"

Processing "rattled":
  'r' → found
  'a' → found
  't' → found, is_end=True! Return "rat"

Processing "battery":
  'b' → found
  'a' → found
  't' → found, is_end=True! Return "bat"

Processing "the": 't' found, 'h' not found → "the"

Output: "the cat was rat by the bat"
```

### Why Trie is Optimal

| Approach | Time per Word | Total Time |
|----------|---------------|------------|
| Check each root | O(D × L) | O(W × D × L) |
| Hash set of roots | O(L²) substrings | O(W × L²) |
| **Trie** | O(L) | O(W × L) |

Where D = dictionary size, W = words in sentence, L = word length.

### Complexity

- **Time**: O(D × L + W × L) - build trie + process words
- **Space**: O(D × L) for trie

---
