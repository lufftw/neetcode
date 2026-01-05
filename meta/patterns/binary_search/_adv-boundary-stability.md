## Boundary Stability Rule

> **Core Insight**: Why moving left/right this way is **always safe** — the correctness guarantee of binary search.

### The Fundamental Question

> "How do we know we're not skipping the answer when we move boundaries?"

This is the **correctness proof** that separates confident programmers from those who trial-and-error.

### The Invariant Guarantee

**Binary search correctness depends on maintaining this invariant**:

> After each iteration, the answer (if it exists) remains within `[left, right]`.

This means:
- When we move `left = mid + 1`, we're **certain** the answer is NOT in `[old_left, mid]`
- When we move `right = mid - 1` or `right = mid`, we're **certain** the answer is NOT in `(mid, old_right]`

### Why We Never Skip the Answer

#### For `first_true` (finding first True in [F,F,F,T,T,T]):

```python
while left < right:
    mid = (left + right) // 2
    if predicate(mid):  # mid is True
        right = mid     # Answer could be mid or before, keep mid
    else:               # mid is False
        left = mid + 1  # Answer must be after mid, exclude mid
```

**Proof of correctness**:
1. If `predicate(mid)` is True → answer is `<= mid` → keep mid in range
2. If `predicate(mid)` is False → answer is `> mid` → exclude mid safely

**Visual**:
```
[F, F, F, F, T, T, T, T]
             ↑
          boundary

If mid lands on F: answer is to the right → left = mid + 1 (safe)
If mid lands on T: answer is here or left → right = mid (safe)
```

#### For `last_true` (finding last True in [T,T,T,T,F,F,F]):

```python
while left < right:
    mid = (left + right + 1) // 2  # Bias right
    if predicate(mid):  # mid is True
        left = mid      # Answer could be mid or after, keep mid
    else:               # mid is False
        right = mid - 1 # Answer must be before mid, exclude mid
```

**Proof of correctness**:
1. If `predicate(mid)` is True → answer is `>= mid` → keep mid in range
2. If `predicate(mid)` is False → answer is `< mid` → exclude mid safely

### Comparison with Sliding Window Invariant

Like sliding window's "window always satisfies constraint", binary search has:

| Technique | Invariant | Guarantee |
|-----------|-----------|-----------|
| Sliding Window | Window always satisfies constraint | Expand/contract preserves validity |
| Binary Search | Answer always in `[left, right]` | Boundary moves preserve answer |

### Common Mistakes That Violate Stability

| Mistake | Why It Breaks | Fix |
|---------|--------------|-----|
| `left = mid` with floor division | May not progress when `right = left + 1` | Use `mid = (l + r + 1) // 2` |
| `right = mid - 1` in first_true | Might exclude the answer | Use `right = mid` |
| Moving both when unsure | Double-moves can skip answer | Move only the correct boundary |

### The Safety Checklist

Before finalizing binary search code, verify:

1. ✅ **Predicate is monotonic**: All F before all T (or vice versa)
2. ✅ **Boundary move preserves answer**: New range still contains answer
3. ✅ **Loop makes progress**: Interval shrinks every iteration
4. ✅ **Termination is correct**: Final `left` (or `right`) is the answer


