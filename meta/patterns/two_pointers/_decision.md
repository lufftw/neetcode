## When to Use Two Pointers

### Problem Indicators

✅ **Use two pointers when:**
- Working with **sorted** arrays/lists
- Need to find **pairs or tuples** with a target property
- **In-place** modification is required
- Need to detect **cycles** in sequences
- **Merging** sorted sequences

❌ **Don't use two pointers when:**
- Array is unsorted and sorting is not allowed
- Need all pairs regardless of order (use hash map)
- Problem requires **non-contiguous** elements
- Relationship between elements is not monotonic

### Decision Flowchart

```
Is the array sorted (or can be sorted)?
├── No → Is it a linked list cycle problem?
│        ├── Yes → Fast–Slow Pointers
│        └── No → Consider hash map or other approach
└── Yes → What's the goal?
          ├── Find pair with target sum → Opposite Pointers
          ├── Remove/deduplicate in-place → Same-Direction
          ├── Partition by property → Dutch Flag
          ├── Find all unique tuples → Dedup Enumeration
          └── Merge two sequences → Merge Pattern
```

