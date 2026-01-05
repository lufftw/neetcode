## Binary Search vs Alternatives

> **Core Insight**: Know when NOT to use binary search.

### When Binary Search Applies

✅ **Use binary search when:**
- Sorted or monotonic property exists
- Search space can be halved by a predicate
- O(log n) gives meaningful improvement
- Clear true/false boundary exists

### When to Use Alternatives

#### Alternative 1: Hash Map (O(1) lookup)

**Use instead when:**
- Need exact match in unsorted data
- Multiple lookups expected
- Space O(n) is acceptable

**Example**: Two Sum (unsorted) — hash map beats sorting + binary search

#### Alternative 2: Two Pointers (O(n) traverse)

**Use instead when:**
- Need to examine pairs/triplets
- Sorted data but need all combinations
- Search + constraint is better expressed as pointer movement

**Example**: 3Sum — two pointers on sorted array

#### Alternative 3: Sliding Window

**Use instead when:**
- Contiguous subarray/substring
- Add/remove elements incrementally
- Window property is monotonic

**Example**: Minimum Window Substring — can't binary search, need sliding window

#### Alternative 4: Linear Scan

**Use instead when:**
- Data is small (n < 100)
- Binary search overhead not worth it
- Need to check all elements anyway

### Decision Matrix

| Problem Type | Binary Search | Alternative |
|-------------|---------------|-------------|
| Find in sorted array | ✅ Yes | - |
| Find in unsorted array | ❌ No | Hash map |
| Optimize with monotonic predicate | ✅ Yes | - |
| All pairs with constraint | ❌ No | Two pointers |
| Contiguous subarray optimization | ❌ No | Sliding window |
| Small n (< 100) | Maybe | Linear might be simpler |

### Boundary with Other Patterns

```
┌─────────────────────────────────────────────────────────────────┐
│                    Pattern Selection Guide                       │
├─────────────────────────────────────────────────────────────────┤
│  Sorted array + find element?                                    │
│  └── Binary Search                                               │
│                                                                  │
│  Sorted array + find pair summing to target?                    │
│  └── Two Pointers (not binary search each element)             │
│                                                                  │
│  Unsorted array + find pair summing to target?                  │
│  └── Hash Map                                                    │
│                                                                  │
│  Find optimal subarray length?                                   │
│  └── Sliding Window (if property monotonic in window size)     │
│  └── Binary Search (if answer space is discrete)               │
└─────────────────────────────────────────────────────────────────┘
```


