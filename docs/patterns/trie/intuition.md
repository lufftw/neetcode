# Trie Patterns: Mental Models & Intuition

> Build deep understanding of when and why Tries work for string problems.

## The Core Insight

**A Trie is a tree where each path from root represents a prefix.**

This simple structure enables O(L) operations where L is the string length - regardless of how many strings are stored!

---

## Mental Model 1: The Branching Path

Imagine a filing cabinet where each drawer leads to more drawers:

```
                    root
                   /    \
                  a      b
                 / \      \
                p   t      a
               /     \      \
              p       e      t(end)
             /
            l
           /
          e(end)

Words: "apple", "ate", "bat"

Finding "apple":
  root → a → p → p → l → e ✓ (found: is_end=True)

Finding "app":
  root → a → p → p → NOT is_end ✗ (prefix exists, not a word)

Finding "apt":
  root → a → p → ✗ (no 't' child)
```

**Key insight**: Shared prefixes share paths. "apple" and "application" share "appl".

---

## Mental Model 2: The Autocomplete Tree

Think of how your phone suggests words:

```
You type: "m" → [mobile, money, monitor]
You type: "mo" → [mobile, money, monitor]
You type: "mou" → [mouse, mousepad]

The Trie naturally groups words by prefix:

      m
     /|\
    o i a
   /|  |  \
  n u  c   t...
 /|  |  |
e i  s  r...
|  \  |
y   t e
|    \
pot   pad
```

Each node in the trie represents a "state" in typing - where you are after typing certain characters.

---

## Mental Model 3: Wildcard as Branching

For '.' wildcard search, think of it as taking ALL possible paths:

```
Words: "bad", "dad", "mad"
Search: ".ad"

         root
        / | \
       b  d  m
       |  |  |
       a  a  a
       |  |  |
       d  d  d
      (end)(end)(end)

'.' at position 0 → Try ALL children (b, d, m)
  Each path leads to 'a' → then 'd' → found!

It's like parallel universe exploration - the '.' splits reality.
```

---

## Mental Model 4: Grid + Trie = Pruned Search

For Word Search II, visualize the trie as a "validity checker":

```
Board:        Trie (words: ["oath", "eat"]):
o a a n            root
e t a e           /    \
i h k r          o      e
i f l v         /        \
               a          a
              /            \
             t              t
            /              (end)
           h
          (end)

DFS from 'o':
  Check: Is 'o' in trie? ✓ → Continue
  Move to 'a': Is 'a' child of 'o' in trie? ✓ → Continue
  Move to 't': Is 't' child of 'a' in trie? ✓ → Continue
  Move to 'h': Is 'h' child of 't' in trie? ✓ + is_end → Found "oath"!

Without trie: Try all 10,000 words at each cell
With trie: Follow single path, prune instantly if no match
```

---

## Mental Model 5: Shortest Prefix = First End

For Replace Words, you're looking for the "first exit":

```
Dictionary: ["cat", "ca"]
Word: "cattle"

Trie:
root → c → a(end) → t(end)
           ↑
           First end!

Traversing "cattle":
  'c' → keep going
  'a' → is_end=True! Stop here, return "ca"

The first is_end you hit is the shortest root.
```

---

## Algorithm Selection Guide

| Problem Type | Pattern | Why |
|--------------|---------|-----|
| Exact word lookup | Basic Trie | O(L) guaranteed |
| Prefix checking | startsWith() | Natural trie operation |
| Wildcard search | DFS on Trie | Branch on '.' |
| Multi-word grid search | Trie + Backtracking | Prune invalid paths |
| Shortest prefix | Find first is_end | Early termination |
| Autocomplete | Store words at nodes | O(1) per prefix query |

---

## Common Pitfalls

### Pitfall 1: Confusing Prefix vs Word

```python
# WRONG: Only checks if path exists
def search(self, word):
    node = self._find_node(word)
    return node is not None  # "app" returns True even if only "apple" exists!

# CORRECT: Check is_end flag
def search(self, word):
    node = self._find_node(word)
    return node is not None and node.is_end
```

### Pitfall 2: Forgetting to Mark End

```python
# WRONG: No end marker
def insert(self, word):
    node = self.root
    for char in word:
        if char not in node.children:
            node.children[char] = TrieNode()
        node = node.children[char]
    # Missing: node.is_end = True

# CORRECT: Mark word end
def insert(self, word):
    # ... same as above ...
    node.is_end = True  # Essential!
```

### Pitfall 3: Duplicates in Grid Search

```python
# WRONG: Can find same word multiple times
if next_node.word:
    result.append(next_node.word)
    # Word stays, might be found again from different path

# CORRECT: Clear after finding
if next_node.word:
    result.append(next_node.word)
    next_node.word = None  # Prevent duplicates
```

### Pitfall 4: Not Pruning in Grid Search

```python
# INEFFICIENT: Keep empty branches
if next_node.word:
    result.append(next_node.word)
    next_node.word = None

# OPTIMIZED: Prune empty branches
if next_node.word:
    result.append(next_node.word)
    next_node.word = None

if not next_node.children and not next_node.word:
    del node.children[char]  # Prune dead end
```

---

## Practice Progression

### Level 1: Basic Operations
1. **LC 208 - Implement Trie** (Insert, search, prefix)

### Level 2: Enhanced Search
2. **LC 211 - Add and Search Words** (Wildcard with '.')

### Level 3: Application
3. **LC 648 - Replace Words** (Shortest prefix match)
4. **LC 1268 - Search Suggestions System** (Autocomplete)

### Level 4: Combination
5. **LC 212 - Word Search II** (Trie + Backtracking)

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│                        TRIE                              │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  STRUCTURE:                  INSERT:                     │
│  ──────────                  ───────                     │
│  children = {}               for char in word:           │
│  is_end = False                if char not in children:  │
│                                  create node             │
│                                move to child             │
│                              mark is_end = True          │
│                                                          │
│  SEARCH WORD:                SEARCH PREFIX:              │
│  ────────────                ─────────────               │
│  node = find_node(word)      return find_node(prefix)    │
│  return node and node.is_end        is not None          │
│                                                          │
│  WILDCARD '.':               GRID + TRIE:                │
│  ────────────                ──────────                  │
│  if char == '.':             Build trie from words       │
│    try ALL children          DFS grid, follow trie       │
│  else:                       Prune if no trie path       │
│    follow exact path         Mark visited, backtrack     │
│                                                          │
│  COMPLEXITY:                                             │
│  ──────────                                              │
│  Insert:     O(L)                                        │
│  Search:     O(L) exact, O(26^D × L) with D wildcards   │
│  Space:      O(N × L) for N words                        │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## When to Use Trie vs Alternatives

```
Need string prefix operations?
│
├─ No → Hash Set (simpler for exact lookup)
│
└─ Yes
   │
   ├─ Static data, few queries? → Sorted Array + Binary Search
   │
   └─ Dynamic data OR many queries? → Trie
      │
      ├─ Need wildcards? → Trie + DFS
      │
      ├─ Multiple strings in grid? → Trie + Backtracking
      │
      └─ Need suggestions? → Trie with word lists at nodes
```
