## When to Use Monotonic Stack

### Problem Indicators

✅ **Use monotonic stack when:**
- Finding "next greater/smaller element" for each position
- Computing spans or distances to boundaries
- Calculating contributions based on interval widths
- Processing histograms or finding maximal rectangles
- Greedy digit/character selection with order constraints

❌ **Don't use monotonic stack when:**
- No boundary/comparison relationship between elements
- Need random access to boundaries (use precomputation)
- Problem requires bidirectional boundaries simultaneously (may need two passes)
- Simpler O(n) traversal suffices

### Decision Flowchart

```
Is there a "nearest element satisfying a condition" query?
├── Yes → Is the condition based on comparison (>, <, >=, <=)?
│         ├── Yes → Monotonic Stack
│         │         ├── Finding boundaries → Base template
│         │         ├── Computing areas/spans → Histogram pattern
│         │         ├── Counting subarrays → Contribution pattern
│         │         ├── Trapping water/valleys → Container pattern
│         │         └── Greedy selection → Greedy monotonic stack
│         └── No → Other technique (hash map, etc.)
└── No → Monotonic stack probably doesn't apply
```


