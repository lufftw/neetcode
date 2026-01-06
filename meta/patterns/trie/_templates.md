## Quick Reference Templates

### Basic Trie Structure

```python
class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.is_end: bool = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self._find_node(word)
        return node is not None and node.is_end

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

### Wildcard Search (DFS)

```python
def search_with_wildcard(self, word: str) -> bool:
    def dfs(node: TrieNode, i: int) -> bool:
        if i == len(word):
            return node.is_end

        char = word[i]
        if char == '.':
            return any(dfs(child, i + 1) for child in node.children.values())

        if char not in node.children:
            return False
        return dfs(node.children[char], i + 1)

    return dfs(self.root, 0)
```

---

### Trie + Grid Backtracking

```python
def find_words_in_grid(board: List[List[str]], words: List[str]) -> List[str]:
    # Build trie
    root = TrieNode()
    for word in words:
        node = root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.word = word  # Store word at end

    result = []
    rows, cols = len(board), len(board[0])

    def dfs(r: int, c: int, node: TrieNode):
        char = board[r][c]
        if char not in node.children:
            return

        next_node = node.children[char]
        if next_node.word:
            result.append(next_node.word)
            next_node.word = None  # Avoid duplicates

        board[r][c] = '#'  # Mark visited
        for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != '#':
                dfs(nr, nc, next_node)
        board[r][c] = char  # Restore

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, root)

    return result
```

---

### Shortest Prefix Match

```python
def find_shortest_root(self, word: str) -> str:
    node = self.root
    for i, char in enumerate(word):
        if char not in node.children:
            return word  # No prefix found
        node = node.children[char]
        if node.is_end:
            return word[:i + 1]  # Shortest prefix
    return word
```

---

### Autocomplete with Top-K

```python
class AutocompleteTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
                node.children[char].suggestions = []
            node = node.children[char]
            # Maintain top-k suggestions (already sorted input)
            if len(node.suggestions) < 3:
                node.suggestions.append(word)

    def get_suggestions(self, prefix: str) -> List[str]:
        node = self._find_node(prefix)
        return node.suggestions if node else []
```

---

### Complexity Summary

| Operation | Time | Space |
|-----------|------|-------|
| Build trie (N words, L avg length) | O(N × L) | O(N × L) |
| Insert word | O(L) | O(L) new nodes |
| Search exact | O(L) | O(1) |
| Search prefix | O(L) | O(1) |
| Wildcard search | O(26^W × L) | O(L) stack |
| Grid search | O(4^L) per cell | O(L) stack |
| Collect K suggestions | O(K) | O(K) |

---
