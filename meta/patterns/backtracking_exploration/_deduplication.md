## Deduplication Strategies

### Strategy Comparison

| Strategy | When to Use | Example |
|----------|-------------|---------|
| **Sorting + Same-Level Skip** | Input has duplicates | Permutations II, Subsets II |
| **Start Index** | Subsets/Combinations (order doesn't matter) | Subsets, Combinations |
| **Used Array** | Permutations (all elements, order matters) | Permutations |
| **Canonical Ordering** | Implicit via index ordering | All subset-like problems |

### Same-Level Skip Pattern

```python
# Sort first, then skip duplicates at same level
nums.sort()

for i in range(start, n):
    # Skip if current equals previous at same tree level
    if i > start and nums[i] == nums[i - 1]:
        continue
    # ... process nums[i]
```

### Used Array Pattern

```python
# For permutations with duplicates
if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
    continue
# This ensures we use duplicates in order (leftmost first)
```

