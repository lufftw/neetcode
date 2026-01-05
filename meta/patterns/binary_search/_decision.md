## When to Use Binary Search

### Problem Indicators

✅ **Use binary search when:**
- Sorted array or monotonic property
- Need to find a boundary or threshold
- Search space can be halved based on a condition
- O(log n) is required or beneficial
- "Minimize the maximum" or "maximize the minimum" problems

❌ **Don't use binary search when:**
- Data is unsorted and sorting is expensive
- No monotonic property exists
- Need to examine all elements anyway
- Search space cannot be meaningfully halved

### Decision Flowchart

```
Is the problem about finding a specific element or boundary?
├── Yes → Is the data sorted or have monotonic property?
│         ├── Yes → Binary Search!
│         │         ├── Find exact value? → Exact match template
│         │         ├── Find first/last? → Lower/upper bound template
│         │         ├── Rotated array? → Rotated array template
│         │         └── Find optimal answer? → Answer space template
│         └── No → Can you sort it? Is it worth the cost?
│                   ├── Yes → Sort + Binary Search
│                   └── No → Use linear search or hash map
└── No → Binary search probably doesn't apply
```


