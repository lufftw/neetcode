## Off-by-One, Comparison Semantics, and Robustness

### Strict vs Non-Strict Monotonicity

| Comparison | Stack Order | When Elements Are Popped | Use Case |
|------------|-------------|--------------------------|----------|
| `<` (strict) | Decreasing | When strictly greater appears | Default NGE |
| `<=` (non-strict) | Decreasing | When greater or equal appears | Contribution with duplicates |
| `>` (strict) | Increasing | When strictly smaller appears | Default NSE |
| `>=` (non-strict) | Increasing | When smaller or equal appears | Histogram with duplicates |

### Stable Boundary for Duplicates

When dealing with duplicates, use **asymmetric tie-breaking**:

```python
# Left boundary: strictly smaller (exclusive)
while stack and arr[stack[-1]] >= arr[i]:  # >=

# Right boundary: smaller or equal (inclusive)
while stack and arr[stack[-1]] > arr[i]:   # >
```

This creates a consistent "left-closed, right-open" convention.

### Index vs Value Storage

**Always store indices**, not values:

```python
# Canonical: Store indices
stack.append(i)
value = arr[stack[-1]]
distance = i - stack[-1]

# Anti-pattern: Store values (loses position information)
stack.append(arr[i])  # Can't compute distances!
```

### Sentinel Usage Patterns

| Sentinel | Purpose | Example |
|----------|---------|---------|
| `heights.append(0)` | Force flush at end | Histogram |
| `stack = [-1]` | Virtual left boundary | Handle empty stack |
| `temperatures.append(float('inf'))` | Force all elements to pop | Ensure completion |

### Edge Case Checklist

- [ ] **Empty input**: Return appropriate default (0, [], etc.)
- [ ] **All equal elements**: Check comparison semantics
- [ ] **Single element**: Stack operations should handle gracefully
- [ ] **Strictly increasing/decreasing**: One of the boundaries may be all default
- [ ] **Overflow-safe arithmetic**: Use modular arithmetic for contribution counting
- [ ] **No-boundary cases**: Elements remaining in stack after processing


