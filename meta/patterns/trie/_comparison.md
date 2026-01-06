## Pattern Comparison

| Problem | Trie Modification | Search Type | Extra Data |
|---------|-------------------|-------------|------------|
| **208 - Implement Trie** | Basic structure | Exact + Prefix | `is_end` flag |
| **211 - Add/Search Words** | DFS search | Wildcard '.' | None |
| **212 - Word Search II** | Build from words | Grid backtracking | `word` at end |
| **648 - Replace Words** | Find shortest | First matching prefix | None |
| **1268 - Search Suggestions** | Store words at nodes | Collect with prefix | `words[]` list |

---

## Operation Comparison

| Operation | 208 Basic | 211 Wildcard | 212 Grid | 648 Replace | 1268 Autocomplete |
|-----------|-----------|--------------|----------|-------------|-------------------|
| Insert | O(L) | O(L) | O(L) | O(L) | O(L) |
| Search exact | O(L) | O(26^W × L) | - | - | - |
| Search prefix | O(L) | - | - | O(L) | O(1)* |
| Find words | - | - | O(4^L) | - | O(K) |

*With precomputed suggestions

---

## When to Use Each Variation

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
