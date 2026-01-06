## Decision Flowchart

```
                    Range Query Problem?
                           │
                           ▼
              ┌─────────────────────────┐
              │   Is the array mutable   │
              │   (updates + queries)?   │
              └─────────────────────────┘
                    │             │
                   YES            NO
                    │             │
                    ▼             ▼
           Segment Tree    Prefix Sum
           or Fenwick Tree  (O(1) query)
                    │
                    ▼
        ┌────────────────────────┐
        │  What type of query?   │
        └────────────────────────┘
              │         │
         Range Sum   Range Min/Max
              │         │
              ▼         ▼
         Fenwick    Segment Tree
          Tree      (BIT doesn't
                     support this)
```

### Key Decision Points

| Signal | Use This |
|--------|----------|
| "update element" + "query range sum" | BIT or Segment Tree |
| "update element" + "query range min/max" | Segment Tree only |
| "count elements in range" | BIT with coordinate compression |
| "count inversions" | BIT (process right-to-left) or Merge Sort |
| "count subarrays with sum in [L, R]" | Merge Sort with counting |

### Problem Pattern Recognition

| If you see... | Think... |
|---------------|----------|
| `update(index, val)` + `sumRange(left, right)` | BIT (simpler) |
| Values too large, need compression | Coordinate compression + BIT |
| "count smaller after self" | BIT right-to-left |
| "count pairs satisfying condition" | Merge Sort with counting |
| 2D array with updates | 2D Segment Tree |

---

