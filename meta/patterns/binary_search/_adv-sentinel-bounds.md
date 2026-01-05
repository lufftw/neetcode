## Sentinel Bounds & Virtual Boundaries

> **Core Insight**: `low` and `high` don't always come from the array — they come from **problem constraints**.

### Understanding Virtual Boundaries

For **answer space** problems, bounds are derived from:
- Problem constraints (min/max possible values)
- Mathematical guarantees (what must be true)

Not from:
- Array length
- Array indices

### Bound Derivation Patterns

#### Pattern 1: Minimum Capacity/Rate

The minimum must handle the largest single item:

```python
# Can't ship a package heavier than capacity
left = max(weights)

# Can't eat a pile bigger than speed × 1 hour
left = 1  # (or could be max(piles) if must finish each pile in 1 hour)
```

#### Pattern 2: Maximum Capacity/Rate

The maximum is when everything is in one group:

```python
# Ship everything in 1 day
right = sum(weights)

# Finish largest pile in 1 hour
right = max(piles)
```

### Common Bound Formulas

| Problem Type | left | right |
|-------------|------|-------|
| Min capacity | `max(items)` | `sum(items)` |
| Min speed | `1` | `max(items)` |
| Min time | `1` | `max(times)` |
| Max distance | `0` | `total_distance` |

### Why Beginners Get This Wrong

Common mistakes:

| Wrong | Why It's Wrong | Correct |
|-------|---------------|---------|
| `left = 0` for capacity | Can't have 0 capacity | `left = max(weights)` |
| `right = len(arr)` | Confusing index with value domain | `right = sum(arr)` |
| `left = 1` for all | Sometimes min must be larger | Analyze constraints |

### The Guarantee Principle

**Both bounds must guarantee the answer is included**:

1. `left` = smallest value that MIGHT work
2. `right` = largest value that DEFINITELY works

This ensures binary search can't miss the answer.

### Example: Why `max(weights)` for Shipping?

```
weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
days = 5

Q: Why can't capacity be 9?
A: We have a package weighing 10. Capacity 9 can't ship it.
   So capacity MUST be >= max(weights) = 10.

Q: Why is sum(weights) = 55 the upper bound?
A: With capacity 55, we can ship everything in 1 day.
   We'll never need more capacity than that.
```


