## When to Use In-Place Reversal

### Decision Flowchart

```
Is this a linked list problem?
├── No → Different pattern
└── Yes → Does it involve reversing node order?
    ├── No → Consider: two-pointers, fast/slow, merge
    └── Yes → IN-PLACE REVERSAL PATTERN
        │
        ├── Reverse entire list?
        │   └── Use 206 template (three-pointer)
        │
        ├── Reverse a specific segment [left, right]?
        │   └── Use 92 template (dummy + boundary tracking)
        │
        ├── Reverse in groups of k?
        │   └── Use 25 template (group management + kth-node check)
        │
        ├── Reverse pairs (k=2)?
        │   └── Use 25 template with k=2
        │
        └── Reverse with some condition?
            └── Combine with appropriate variant + condition check
```

### Pattern Recognition Signals

**Use In-Place Reversal when you see**:
- "Reverse" + "linked list" in problem statement
- Need to reorder nodes without extra space
- Swap adjacent pairs or groups
- Follow-up asks for O(1) space

**Key constraint indicators**:
- "You may not modify the values" → Must manipulate pointers
- "O(1) extra memory" → Must be in-place
- "In one pass" → Iterative approach preferred

### Variant Selection Guide

| Scenario | Variant | Template |
|----------|---------|----------|
| Reverse everything | Full | 206 |
| Reverse middle portion | Segment | 92 |
| Reverse from head to position | Segment (left=1) | 92 |
| Reverse every 2 nodes | K-Group (k=2) | 25 |
| Reverse every k nodes | K-Group | 25 |
| Reverse if condition met | Custom + base | 206 + condition |

### Space-Time Trade-offs

| Approach | Time | Space | Use When |
|----------|------|-------|----------|
| Iterative | O(N) | O(1) | Default choice |
| Recursive | O(N) | O(N) | Cleaner for some k-group cases |
| Array copy | O(N) | O(N) | Only if space not constrained |

### Common Mistakes to Avoid

1. **Not using dummy node** when head might change
2. **Forgetting to save `next`** before reversing pointer
3. **Wrong reconnection** after segment reversal
4. **Off-by-one** in position counting (1-indexed vs 0-indexed)
5. **Reversing too many nodes** in k-group when remainder < k


