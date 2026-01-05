## Off-by-One Handling and Termination Guarantees

### Mid Calculation: Left-Bias vs Right-Bias

```python
# Left-biased (rounds down) - Standard
mid = left + (right - left) // 2

# Right-biased (rounds up)
mid = left + (right - left + 1) // 2
```

**When does bias matter?**

| Scenario | `left = mid` | `left = mid + 1` |
|----------|-------------|------------------|
| 2 elements, left-bias | mid = left → infinite loop! | ✓ Correct |
| 2 elements, right-bias | ✓ Correct | mid = right → safe |

**Rule**: Use left-bias (`//2`) when using `left = mid + 1` on the false branch.

### Loop Invariant Verification

For `while left < right`:

```
Initialization: [left, right] contains the answer
Maintenance: Each iteration reduces range by at least 1
Termination: left == right, range has exactly 1 element
Post-condition: left is the answer (or indicates not found)
```

Progress guarantee:
- If `right = mid`, range becomes `[left, mid]` where `mid < right` (or `mid == left`)
- If `left = mid + 1`, range becomes `[mid + 1, right]` which excludes `mid`
- Either way, range strictly decreases

### Inclusive vs Exclusive Bounds

| Style | Initialization | Loop Condition | Update Rules |
|-------|---------------|----------------|--------------|
| `[left, right]` | `left = 0, right = n - 1` | `left <= right` | `left = mid + 1`, `right = mid - 1` |
| `[left, right)` | `left = 0, right = n` | `left < right` | `left = mid + 1`, `right = mid` |

The `[left, right)` style with `left < right` is generally preferred for boundary search because:
- Natural for "find first" problems
- Final `left` directly gives the answer position
- Compatible with array slicing semantics

### Edge Case Checklist

| Case | Handling |
|------|----------|
| Empty array | Return -1 or appropriate default |
| Single element | Loop body executes 0 times, return left |
| Target not found | Return insertion point or -1 |
| All elements equal | Works correctly if predicate handles it |
| Integer overflow | Use `left + (right - left) // 2` |
| Duplicates | Decide: first occurrence, last, or any |


