## Base Template: Predicate Boundary Search

> **Core Insight**: Binary search finds the boundary between false and true regions of a monotonic predicate.
> **Invariant**: `left` is always in the false region, `right` is always in the true region (or vice versa).
> **Result**: Upon termination, `left` points to the first true position.

### Implementation

```python
def binary_search_first_true(left: int, right: int, predicate) -> int:
    """
    Find the first position where predicate(x) is True.

    This is the canonical binary search template. All other variations
    are specializations of this pattern with specific predicates.

    Requirements:
    - predicate(x) must be monotonic: once True, stays True
    - Search space [left, right] where answer exists or returns right+1

    Invariant:
    - At all times, if answer exists, it's in [left, right]
    - predicate(left - 1) is False (or left is minimum)
    - predicate(right + 1) is True (or right is maximum)

    Algorithm:
    1. Compute mid = left + (right - left) // 2 (overflow-safe)
    2. If predicate(mid) is True, answer could be mid or earlier
       → search left half: right = mid
    3. If predicate(mid) is False, answer must be after mid
       → search right half: left = mid + 1
    4. Terminate when left == right (single candidate remaining)

    Time Complexity: O(log n) iterations × O(predicate)
    Space Complexity: O(1)

    Args:
        left: Lower bound of search space (inclusive)
        right: Upper bound of search space (inclusive)
        predicate: Monotonic function returning bool

    Returns:
        First index where predicate is True, or right + 1 if never True
    """
    # Search space: [left, right]
    while left < right:
        # Overflow-safe midpoint calculation
        mid = left + (right - left) // 2

        if predicate(mid):
            # predicate(mid) is True
            # Answer could be mid or something earlier
            # Maintain invariant: answer is in [left, mid]
            right = mid
        else:
            # predicate(mid) is False
            # Answer must be strictly after mid
            # Maintain invariant: answer is in [mid + 1, right]
            left = mid + 1

    # left == right: only one candidate remains
    # This is the first position where predicate might be True
    return left
```

### Why This Works

The algorithm maintains a **shrinking invariant**:
- If `predicate(mid)` is True: the first True could be at `mid` or before → keep `mid` in range
- If `predicate(mid)` is False: the first True must be after `mid` → exclude `mid`

```
Visualization:
Initial:  [F, F, F, F, T, T, T, T]
           ↑                    ↑
          left                right

Step 1:   mid = 3 (F), so left = 4
          [F, F, F, F, T, T, T, T]
                       ↑        ↑
                      left    right

Step 2:   mid = 5 (T), so right = 5
          [F, F, F, F, T, T, T, T]
                       ↑  ↑
                      left right

Step 3:   mid = 4 (T), so right = 4
          [F, F, F, F, T, T, T, T]
                       ↑
                    left=right

Result: left = 4 (first True position)
```

### Loop Condition: `left < right` vs `left <= right`

| Condition | Termination | Use Case |
|-----------|-------------|----------|
| `left < right` | `left == right` (one element) | Boundary search (first true) |
| `left <= right` | `left > right` (empty range) | Exact match (may not exist) |

For predicate boundary search, `left < right` is preferred because:
- We always shrink to exactly one candidate
- No risk of infinite loop (each iteration reduces range by at least 1)
- The final `left` is guaranteed to be the answer or the bound

### Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Integer overflow | `(left + right) / 2` overflows | Use `left + (right - left) // 2` |
| Infinite loop | `left` never increases | Ensure `left = mid + 1` when predicate is False |
| Off-by-one | Wrong boundary returned | Carefully define predicate semantics |
| Empty range | `left > right` initially | Handle edge case or validate input |


