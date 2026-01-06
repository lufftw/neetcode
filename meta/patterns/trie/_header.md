# Trie (Prefix Tree) Pattern

## API Kernel: `Trie`

> **Core Mechanism**: Tree-based data structure for efficient string prefix operations.

A **Trie** (pronounced "try") is a tree where each node represents a character, and paths from root to nodes represent prefixes. This enables O(L) operations where L is the string length, regardless of how many strings are stored.

---

## When to Use Trie

| Signal | Example |
|--------|---------|
| Prefix matching | "Find all words starting with 'app'" |
| Autocomplete | "Suggest completions for partial input" |
| Word validation | "Check if word exists in dictionary" |
| Wildcard search | "Match 'a.c' where . is any character" |
| Longest prefix | "Find longest matching prefix" |

---

## Core Trie Structure

```python
class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.is_end: bool = False
        # Optional: store additional data
        # self.word: str = ""  # Store complete word at end node
        # self.count: int = 0  # Count of words with this prefix
```

---

## Base Operations

### Insert Word - O(L)

```python
def insert(self, word: str) -> None:
    node = self.root
    for char in word:
        if char not in node.children:
            node.children[char] = TrieNode()
        node = node.children[char]
    node.is_end = True
```

### Search Word - O(L)

```python
def search(self, word: str) -> bool:
    node = self._find_node(word)
    return node is not None and node.is_end
```

### Search Prefix - O(L)

```python
def startsWith(self, prefix: str) -> bool:
    return self._find_node(prefix) is not None

def _find_node(self, prefix: str) -> Optional[TrieNode]:
    node = self.root
    for char in prefix:
        if char not in node.children:
            return None
        node = node.children[char]
    return node
```

---

## Pattern Variations

| Problem | Variation | Key Modification |
|---------|-----------|------------------|
| LC 208 | Basic Trie | Standard insert/search/prefix |
| LC 211 | Wildcard Search | DFS with '.' matching any character |
| LC 212 | Trie + Backtracking | Build trie, then DFS on grid |
| LC 648 | Prefix Replacement | Find shortest prefix match |
| LC 1268 | Autocomplete | Collect words with given prefix |

---
