## Variation: Lower Bound / Upper Bound (LeetCode 34, 35)

> **Lower Bound**: First index where `arr[i] >= target`
> **Upper Bound**: First index where `arr[i] > target`
> **Use Case**: Finding ranges, handling duplicates, insertion position.

### Lower Bound Implementation

```python
def lower_bound(arr: list[int], target: int) -> int:
    """
    Find the first index where arr[i] >= target.

    This is the standard library equivalent of C++ std::lower_bound.
    If target is not found, returns the insertion point.

    Predicate: arr[mid] >= target

    Properties:
    - All elements before result are < target
    - All elements from result onwards are >= target
    - Result can be len(arr) if all elements < target

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Args:
        arr: Sorted array (ascending)
        target: Value to search for

    Returns:
        First index i where arr[i] >= target, or len(arr) if none
    """
    left, right = 0, len(arr)

    while left < right:
        mid = left + (right - left) // 2

        if arr[mid] >= target:
            # arr[mid] is a candidate (it's >= target)
            # But there might be an earlier one
            right = mid
        else:
            # arr[mid] < target, so answer must be after mid
            left = mid + 1

    return left
```

### Upper Bound Implementation

```python
def upper_bound(arr: list[int], target: int) -> int:
    """
    Find the first index where arr[i] > target.

    This is the standard library equivalent of C++ std::upper_bound.

    Predicate: arr[mid] > target

    Properties:
    - All elements before result are <= target
    - All elements from result onwards are > target
    - Result can be len(arr) if all elements <= target

    Use with lower_bound to find range of target:
    - First occurrence: lower_bound(arr, target)
    - Last occurrence: upper_bound(arr, target) - 1
    - Count of target: upper_bound - lower_bound

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Args:
        arr: Sorted array (ascending)
        target: Value to search for

    Returns:
        First index i where arr[i] > target, or len(arr) if none
    """
    left, right = 0, len(arr)

    while left < right:
        mid = left + (right - left) // 2

        if arr[mid] > target:
            # arr[mid] is a candidate (it's > target)
            right = mid
        else:
            # arr[mid] <= target, so answer must be after mid
            left = mid + 1

    return left
```

### Finding First and Last Position (LeetCode 34)

```python
def search_range(nums: list[int], target: int) -> list[int]:
    """
    Find the starting and ending position of target in sorted array.

    Algorithm:
    1. Use lower_bound to find first occurrence
    2. Use upper_bound to find position after last occurrence
    3. Verify target actually exists

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Args:
        nums: Sorted array (ascending)
        target: Value to find range for

    Returns:
        [first, last] indices, or [-1, -1] if not found
    """
    if not nums:
        return [-1, -1]

    # Find first position where nums[i] >= target
    first = lower_bound(nums, target)

    # Check if target exists
    if first == len(nums) or nums[first] != target:
        return [-1, -1]

    # Find first position where nums[i] > target
    # Last occurrence is one position before
    last = upper_bound(nums, target) - 1

    return [first, last]
```

### Search Insert Position (LeetCode 35)

```python
def search_insert(nums: list[int], target: int) -> int:
    """
    Find index where target is or would be inserted.

    This is exactly lower_bound: first position where nums[i] >= target.

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Args:
        nums: Sorted array of distinct integers
        target: Value to find or insert

    Returns:
        Index of target or insertion position
    """
    return lower_bound(nums, target)
```

### Handling Duplicates

```
Array with duplicates: [1, 2, 2, 2, 2, 3, 4], target = 2

lower_bound(2) = 1  → First position where arr[i] >= 2
                      Points to first 2

upper_bound(2) = 5  → First position where arr[i] > 2
                      Points to 3 (element after last 2)

Count of 2s = upper_bound - lower_bound = 5 - 1 = 4
Range of 2s = [lower_bound, upper_bound - 1] = [1, 4]
```


