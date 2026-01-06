## Decision Guide: When to Use Trie

### Use Trie When

| Scenario | Why Trie Works |
|----------|----------------|
| **Prefix operations** | O(L) regardless of dictionary size |
| **Autocomplete/suggestions** | Efficient prefix-based collection |
| **Spell checking** | Quick validation and suggestions |
| **IP routing (longest prefix match)** | Bit-level trie for routing tables |
| **Word games (Boggle, Word Search)** | Prune invalid paths early |

### Trie vs. Alternatives

| Approach | Prefix Search | Exact Search | Space | Best For |
|----------|---------------|--------------|-------|----------|
| **Trie** | O(L) | O(L) | O(N×L) | Prefix-heavy operations |
| **Hash Set** | O(L²)* | O(L) | O(N×L) | Exact lookups only |
| **Sorted Array + Binary Search** | O(L log N) | O(L log N) | O(N×L) | Static dictionary |

*Check all prefixes

### Decision Flowchart

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

### Common Patterns by Problem Type

| Problem Type | Pattern | Example |
|--------------|---------|---------|
| Implement dictionary | Basic Trie | LC 208 |
| Regex/wildcard matching | DFS Trie | LC 211 |
| Multiple string search in grid | Trie + Backtracking | LC 212 |
| Prefix-based replacement | Shortest prefix match | LC 648 |
| Autocomplete system | Trie with word lists | LC 1268 |
| Longest common prefix | Trie depth analysis | LC 14 |
| Count prefixes | Trie with counters | LC 1804 |

### Red Flags (Don't Use Trie)

- Only need exact word matching → Hash Set is simpler
- Very short strings (< 5 chars) → Overhead may not be worth it
- Memory-constrained environment → Trie nodes have overhead
- Need fuzzy matching → Consider edit distance algorithms instead

---
