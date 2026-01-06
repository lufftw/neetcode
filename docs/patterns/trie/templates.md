# Trie (Prefix Tree) Pattern

## Table of Contents

1. [API Kernel: `Trie`](#1-api-kernel-trie)
2. [When to Use Trie](#2-when-to-use-trie)
3. [Core Trie Structure](#3-core-trie-structure)
4. [Base Operations](#4-base-operations)
5. [Pattern Variations](#5-pattern-variations)
6. [Problem: Implement Trie (Prefix Tree) [LC 208] - BASE](#6-problem-implement-trie-prefix-tree-lc-208---base)
7. [Problem: Design Add and Search Words Data Structure [LC 211]](#7-problem-design-add-and-search-words-data-structure-lc-211)
8. [Problem: Word Search II [LC 212]](#8-problem-word-search-ii-lc-212)
9. [Problem: Replace Words [LC 648]](#9-problem-replace-words-lc-648)
10. [Problem: Search Suggestions System [LC 1268]](#10-problem-search-suggestions-system-lc-1268)
11. [Pattern Comparison](#11-pattern-comparison)
12. [Operation Comparison](#12-operation-comparison)
13. [When to Use Each Variation](#13-when-to-use-each-variation)
14. [Decision Guide: When to Use Trie](#14-decision-guide-when-to-use-trie)
15. [Quick Reference Templates](#15-quick-reference-templates)

---

## 1. API Kernel: `Trie`

> **Core Mechanism**: Tree-based data structure for efficient string prefix operations.

A **Trie** (pronounced "try") is a tree where each node represents a character, and paths from root to nodes represent prefixes. This enables O(L) operations where L is the string length, regardless of how many strings are stored.

---

## 2. When to Use Trie

| Signal | Example |
|--------|---------|
| Prefix matching | "Find all words starting with 'app'" |
| Autocomplete | "Suggest completions for partial input" |
| Word validation | "Check if word exists in dictionary" |
| Wildcard search | "Match 'a.c' where . is any character" |
| Longest prefix | "Find longest matching prefix" |

---

## 3. Core Trie Structure

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

## 4. Base Operations

### 4.1 Insert Word - O(L)

```python
def insert(self, word: str) -> None:
    node = self.root
    for char in word:
        if char not in node.children:
            node.children[char] = TrieNode()
        node = node.children[char]
    node.is_end = True
```

### 4.2 Search Word - O(L)

```python
def search(self, word: str) -> bool:
    node = self._find_node(word)
    return node is not None and node.is_end
```

### 4.3 Search Prefix - O(L)

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

## 5. Pattern Variations

| Problem | Variation | Key Modification |
|---------|-----------|------------------|
| LC 208 | Basic Trie | Standard insert/search/prefix |
| LC 211 | Wildcard Search | DFS with '.' matching any character |
| LC 212 | Trie + Backtracking | Build trie, then DFS on grid |
| LC 648 | Prefix Replacement | Find shortest prefix match |
| LC 1268 | Autocomplete | Collect words with given prefix |

---

---

## 6. Problem: Implement Trie (Prefix Tree) [LC 208] - BASE

> **Pattern**: Basic Trie Operations
> **Difficulty**: Medium
> **Role**: Base template for all Trie problems

### 6.1 Problem Statement

Implement a trie with `insert`, `search`, and `startsWith` methods.

### 6.2 Invariant

**A path from root represents a prefix; `is_end` marks complete words.**

### 6.3 Template Implementation

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

### 6.4 Trace Example

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

### 6.5 Key Insights

1. **Space Efficiency**: Shared prefixes use shared nodes
2. **Time Complexity**: O(L) for all operations, independent of dictionary size
3. **Trade-off**: Uses more space than hash set but enables prefix operations

### 6.6 Complexity

- **Time**: O(L) per operation where L = string length
- **Space**: O(N × L) worst case for N words of length L

---

---

## 7. Problem: Design Add and Search Words Data Structure [LC 211]

> **Pattern**: Trie with Wildcard Search
> **Difficulty**: Medium
> **Delta from Base**: DFS for '.' wildcard matching

### 7.1 Problem Statement

Design a data structure that supports adding words and searching with '.' wildcards that can match any letter.

### 7.2 Invariant

**On '.', branch to ALL children; on letter, follow exact path.**

### 7.3 Delta from Base Template

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

### 7.4 Complete Implementation

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

### 7.5 Trace Example

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

### 7.6 Complexity

- **Time**: O(L) without wildcards, O(26^W × L) worst case with W wildcards
- **Space**: O(N × L) for trie + O(L) recursion stack

---

---

## 8. Problem: Word Search II [LC 212]

> **Pattern**: Trie + Backtracking
> **Difficulty**: Hard
> **Delta from Base**: Build trie from words, DFS on grid

### 8.1 Problem Statement

Given an m×n board of characters and a list of words, return all words that can be formed by sequentially adjacent cells.

### 8.2 Invariant

**Build trie from words, then DFS on grid following trie paths.**

### 8.3 Why Trie + Backtracking?

Without Trie: For each cell, try each word → O(cells × words × word_length)
With Trie: For each cell, follow trie paths → O(cells × 4^max_length) with early termination

The trie enables:
1. **Shared prefix search**: "apple" and "application" share traversal for "appl"
2. **Early termination**: Stop if current path isn't a valid prefix
3. **Multiple word detection**: Find multiple words in single DFS

### 8.4 Template Implementation

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

### 8.5 Trace Example

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

### 8.6 Key Optimizations

1. **Store word at node**: Avoid reconstructing word from path
2. **Prune empty branches**: Remove trie nodes after finding words
3. **In-place marking**: Use board itself for visited tracking

### 8.7 Complexity

- **Time**: O(M × N × 4^L) where L = max word length
- **Space**: O(W × L) for trie where W = number of words

---

---

## 9. Problem: Replace Words [LC 648]

> **Pattern**: Trie Prefix Replacement
> **Difficulty**: Medium
> **Delta from Base**: Find shortest matching prefix

### 9.1 Problem Statement

Given a dictionary of roots and a sentence, replace each word with its shortest root. If a word has no root, keep it unchanged.

Example: dictionary = ["cat", "bat", "rat"], sentence = "the cattle was rattled by the battery"
Output: "the cat was rat by the bat"

### 9.2 Invariant

**For each word, find the shortest prefix that exists in trie.**

### 9.3 Delta from Base Template

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

### 9.4 Complete Implementation

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

### 9.5 Trace Example

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

### 9.6 Why Trie is Optimal

| Approach | Time per Word | Total Time |
|----------|---------------|------------|
| Check each root | O(D × L) | O(W × D × L) |
| Hash set of roots | O(L²) substrings | O(W × L²) |
| **Trie** | O(L) | O(W × L) |

Where D = dictionary size, W = words in sentence, L = word length.

### 9.7 Complexity

- **Time**: O(D × L + W × L) - build trie + process words
- **Space**: O(D × L) for trie

---

---

## 10. Problem: Search Suggestions System [LC 1268]

> **Pattern**: Trie Autocomplete
> **Difficulty**: Medium
> **Delta from Base**: Collect top-k words with given prefix

### 10.1 Problem Statement

Given an array of products and a search word, return for each prefix of the search word up to 3 lexicographically smallest products that match the prefix.

### 10.2 Invariant

**For each prefix, DFS from prefix node to collect words in sorted order.**

### 10.3 Approach Options

| Approach | Build | Query per Prefix | Best When |
|----------|-------|------------------|-----------|
| Sort + Binary Search | O(N log N) | O(log N + K) | Few queries |
| **Trie + DFS** | O(N × L) | O(K) | Many queries |
| Trie + Precomputed | O(N × L × K) | O(1) | Very many queries |

### 10.4 Template Implementation

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

### 10.5 Alternative: DFS Collection

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

### 10.6 Trace Example

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

### 10.7 Key Insight: Pre-store vs. Collect

**Pre-store (implemented above)**:
- Store top-3 at each node during build
- O(1) query but O(N × L) extra space

**Collect on demand**:
- DFS from prefix node each query
- O(K) per query, less space

### 10.8 Complexity

- **Time**: O(N × L × log N) for build (sorting), O(L) per query
- **Space**: O(N × L) for trie + O(3 × L) for stored suggestions

---

---

## 11. Pattern Comparison

| Problem | Trie Modification | Search Type | Extra Data |
|---------|-------------------|-------------|------------|
| **208 - Implement Trie** | Basic structure | Exact + Prefix | `is_end` flag |
| **211 - Add/Search Words** | DFS search | Wildcard '.' | None |
| **212 - Word Search II** | Build from words | Grid backtracking | `word` at end |
| **648 - Replace Words** | Find shortest | First matching prefix | None |
| **1268 - Search Suggestions** | Store words at nodes | Collect with prefix | `words[]` list |

---

## 12. Operation Comparison

| Operation | 208 Basic | 211 Wildcard | 212 Grid | 648 Replace | 1268 Autocomplete |
|-----------|-----------|--------------|----------|-------------|-------------------|
| Insert | O(L) | O(L) | O(L) | O(L) | O(L) |
| Search exact | O(L) | O(26^W × L) | - | - | - |
| Search prefix | O(L) | - | - | O(L) | O(1)* |
| Find words | - | - | O(4^L) | - | O(K) |

*With precomputed suggestions

---

## 13. When to Use Each Variation

```
Need exact word lookup?
├─ Yes → Basic Trie (LC 208)
└─ No
   │
   Support wildcards?
   ├─ Yes → Wildcard Trie (LC 211)
   └─ No
      │
      Search in 2D grid?
      ├─ Yes → Trie + Backtracking (LC 212)
      └─ No
         │
         Find shortest matching prefix?
         ├─ Yes → Prefix Replacement (LC 648)
         └─ No
            │
            Return multiple suggestions?
            └─ Yes → Autocomplete Trie (LC 1268)
```

---

---

## 14. Decision Guide: When to Use Trie

### 14.1 Use Trie When

| Scenario | Why Trie Works |
|----------|----------------|
| **Prefix operations** | O(L) regardless of dictionary size |
| **Autocomplete/suggestions** | Efficient prefix-based collection |
| **Spell checking** | Quick validation and suggestions |
| **IP routing (longest prefix match)** | Bit-level trie for routing tables |
| **Word games (Boggle, Word Search)** | Prune invalid paths early |

### 14.2 Trie vs. Alternatives

| Approach | Prefix Search | Exact Search | Space | Best For |
|----------|---------------|--------------|-------|----------|
| **Trie** | O(L) | O(L) | O(N×L) | Prefix-heavy operations |
| **Hash Set** | O(L²)* | O(L) | O(N×L) | Exact lookups only |
| **Sorted Array + Binary Search** | O(L log N) | O(L log N) | O(N×L) | Static dictionary |

*Check all prefixes

### 14.3 Decision Flowchart

```
Do you need prefix operations?
├─ No → Use Hash Set (simpler, same performance for exact lookup)
└─ Yes
   │
   Is the dictionary dynamic (frequent inserts)?
   ├─ Yes → Use Trie
   └─ No (static dictionary)
      │
      How many queries?
      ├─ Few → Sorted array + binary search
      └─ Many → Use Trie (amortize build cost)
```

### 14.4 Common Patterns by Problem Type

| Problem Type | Pattern | Example |
|--------------|---------|---------|
| Implement dictionary | Basic Trie | LC 208 |
| Regex/wildcard matching | DFS Trie | LC 211 |
| Multiple string search in grid | Trie + Backtracking | LC 212 |
| Prefix-based replacement | Shortest prefix match | LC 648 |
| Autocomplete system | Trie with word lists | LC 1268 |
| Longest common prefix | Trie depth analysis | LC 14 |
| Count prefixes | Trie with counters | LC 1804 |

### 14.5 Red Flags (Don't Use Trie)

- Only need exact word matching → Hash Set is simpler
- Very short strings (< 5 chars) → Overhead may not be worth it
- Memory-constrained environment → Trie nodes have overhead
- Need fuzzy matching → Consider edit distance algorithms instead

---

---

## 15. Quick Reference Templates

### 15.1 Basic Trie Structure

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

### 15.2 Wildcard Search (DFS)

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

### 15.3 Trie + Grid Backtracking

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

### 15.4 Shortest Prefix Match

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

### 15.5 Autocomplete with Top-K

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

### 15.6 Complexity Summary

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



---



*Document generated for NeetCode Practice Framework — API Kernel: TriePrefixSearch*
