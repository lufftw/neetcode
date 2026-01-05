## Variation: Exact Match Search

> **Problem**: Find the index of a specific target value.
> **Delta from Base**: Predicate is `arr[mid] >= target`, then verify exact match.
> **Use Case**: Classic binary search in sorted array.

### Implementation

```python
def binary_search_exact(arr: list[int], target: int) -> int:
    """
    Find index of target in sorted array, or -1 if not found.

    This is a specialization of predicate boundary search where:
    - Predicate: arr[mid] >= target
    - After finding boundary, verify arr[boundary] == target

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Args:
        arr: Sorted array (ascending)
        target: Value to find

    Returns:
        Index of target, or -1 if not found
    """
    if not arr:
        return -1

    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            return mid  # Found exact match
        elif arr[mid] < target:
            left = mid + 1  # Target is in right half
        else:
            right = mid - 1  # Target is in left half

    return -1  # Not found
```

### Key Difference from Boundary Search

| Aspect | Exact Match | Boundary Search |
|--------|-------------|-----------------|
| Loop condition | `left <= right` | `left < right` |
| On match | Return immediately | Continue to find first/last |
| Result | Single index or -1 | Boundary position |
| When not found | Returns -1 | Returns insertion point |


