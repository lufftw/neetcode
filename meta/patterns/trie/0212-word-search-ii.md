## Problem: Word Search II [LC 212]

> **Pattern**: Trie + Backtracking
> **Difficulty**: Hard
> **Delta from Base**: Build trie from words, DFS on grid

### Problem Statement

Given an m×n board of characters and a list of words, return all words that can be formed by sequentially adjacent cells.

### Invariant

**Build trie from words, then DFS on grid following trie paths.**

### Why Trie + Backtracking?

Without Trie: For each cell, try each word → O(cells × words × word_length)
With Trie: For each cell, follow trie paths → O(cells × 4^max_length) with early termination

The trie enables:
1. **Shared prefix search**: "apple" and "application" share traversal for "appl"
2. **Early termination**: Stop if current path isn't a valid prefix
3. **Multiple word detection**: Find multiple words in single DFS

### Template Implementation

```python
class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.word: Optional[str] = None  # Store complete word at end


class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        # Step 1: Build trie from words
        root = TrieNode()
        for word in words:
            node = root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.word = word  # Mark end with the word itself

        # Step 2: DFS from each cell
        rows, cols = len(board), len(board[0])
        result = []

        def dfs(r: int, c: int, node: TrieNode) -> None:
            char = board[r][c]

            # Not a valid trie path
            if char not in node.children:
                return

            next_node = node.children[char]

            # Found a word!
            if next_node.word:
                result.append(next_node.word)
                next_node.word = None  # Avoid duplicates

            # Mark visited
            board[r][c] = '#'

            # Explore 4 directions
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != '#':
                    dfs(nr, nc, next_node)

            # Restore cell
            board[r][c] = char

            # Optimization: prune empty branches
            if not next_node.children:
                del node.children[char]

        # Start DFS from each cell
        for r in range(rows):
            for c in range(cols):
                dfs(r, c, root)

        return result
```

### Trace Example

```
board = [["o","a","a","n"],
         ["e","t","a","e"],
         ["i","h","k","r"],
         ["i","f","l","v"]]
words = ["oath","pea","eat","rain"]

Trie:
root → o → a → t → h (word="oath")
     → p → e → a (word="pea")
     → e → a → t (word="eat")
     → r → a → i → n (word="rain")

DFS from (0,0) 'o':
  → (1,0) 'e': no 'e' child of 'o' in trie, backtrack
  → (0,1) 'a': follow trie o→a
    → (1,1) 't': follow trie o→a→t
      → (1,2) 'a': no 'a' child of 't', backtrack
      → (2,1) 'h': follow trie o→a→t→h, word="oath" FOUND!

Result: ["oath", "eat"]
```

### Key Optimizations

1. **Store word at node**: Avoid reconstructing word from path
2. **Prune empty branches**: Remove trie nodes after finding words
3. **In-place marking**: Use board itself for visited tracking

### Complexity

- **Time**: O(M × N × 4^L) where L = max word length
- **Space**: O(W × L) for trie where W = number of words

---
