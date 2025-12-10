## When to Use Sliding Window

### Problem Indicators

✅ **Use sliding window when:**
- Looking for contiguous subarray/substring
- Need to optimize (min/max) some property of the subarray
- Property can be maintained incrementally as window changes
- Adding/removing elements has O(1) state update

❌ **Don't use sliding window when:**
- Elements are not contiguous (use dynamic programming)
- Property requires global knowledge (use prefix sum + binary search)
- Window boundaries depend on non-local information

### Decision Flowchart

```
Is the answer a contiguous subarray/substring?
├── No → Use DP or other technique
└── Yes → Can you maintain window state incrementally?
          ├── No → Consider prefix sum or other technique
          └── Yes → Sliding Window!
                    ├── Fixed size window? → Use fixed window template
                    └── Variable size? → Maximize or Minimize?
                                        ├── Maximize → Expand always, contract on violation
                                        └── Minimize → Expand until valid, contract while valid
```


