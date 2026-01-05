## Variation: Rotated Sorted Array (LeetCode 33, 81)

> **Problem**: Search in a sorted array that has been rotated at an unknown pivot.
> **Key Insight**: At least one half of the array around mid is always sorted.
> **Invariant**: Target is in the sorted half if it falls within that range.

### Core Reasoning

A rotated sorted array looks like:

```
Original: [0, 1, 2, 3, 4, 5, 6]
Rotated:  [4, 5, 6, 0, 1, 2, 3]
                  ↑
               pivot

Property: For any mid, at least one of [left, mid] or [mid, right] is sorted.

Case 1: arr[left] <= arr[mid] → Left half is sorted
Case 2: arr[left] > arr[mid]  → Right half is sorted
```

### Implementation (No Duplicates - LeetCode 33)

```python
def search_rotated(nums: list[int], target: int) -> int:
    """
    Search for target in rotated sorted array (no duplicates).

    Algorithm:
    1. Find mid
    2. Determine which half is sorted (compare arr[left] with arr[mid])
    3. Check if target is in the sorted half
    4. Narrow search to the appropriate half

    Key Insight:
    - If left half is sorted AND target is in [arr[left], arr[mid]): go left
    - If left half is sorted AND target is NOT in range: go right
    - If right half is sorted AND target is in (arr[mid], arr[right]]: go right
    - If right half is sorted AND target is NOT in range: go left

    Invariant:
    - If target exists, it's in [left, right]

    Why this doesn't skip the answer:
    - We only eliminate a half when we're CERTAIN target isn't there
    - The sorted half gives us exact boundaries to check

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Args:
        nums: Rotated sorted array (distinct elements)
        target: Value to find

    Returns:
        Index of target, or -1 if not found
    """
    if not nums:
        return -1

    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid

        # Determine which half is sorted
        if nums[left] <= nums[mid]:
            # Left half [left, mid] is sorted
            if nums[left] <= target < nums[mid]:
                # Target is in the sorted left half
                right = mid - 1
            else:
                # Target is in the right half
                left = mid + 1
        else:
            # Right half [mid, right] is sorted
            if nums[mid] < target <= nums[right]:
                # Target is in the sorted right half
                left = mid + 1
            else:
                # Target is in the left half
                right = mid - 1

    return -1
```

### Implementation (With Duplicates - LeetCode 81)

```python
def search_rotated_with_duplicates(nums: list[int], target: int) -> bool:
    """
    Search for target in rotated sorted array (may have duplicates).

    Key Challenge:
    When nums[left] == nums[mid] == nums[right], we cannot determine
    which half is sorted. In this case, we must shrink linearly.

    Example: [1, 0, 1, 1, 1] with target = 0
    - left=0, right=4, mid=2
    - nums[0]=1, nums[2]=1, nums[4]=1
    - Cannot tell if [1,0,1] or [1,1,1] is sorted

    Solution: When this ambiguity occurs, shrink search space by 1.

    Worst Case: O(n) when all elements are equal except one
    Average Case: O(log n) when duplicates are sparse

    Time Complexity: O(n) worst case, O(log n) average
    Space Complexity: O(1)

    Args:
        nums: Rotated sorted array (may have duplicates)
        target: Value to find

    Returns:
        True if target exists, False otherwise
    """
    if not nums:
        return False

    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return True

        # Handle ambiguous case: can't determine sorted half
        if nums[left] == nums[mid] == nums[right]:
            left += 1
            right -= 1
        elif nums[left] <= nums[mid]:
            # Left half is sorted
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            # Right half is sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return False
```

### Two-Phase Approach: Find Pivot Then Search

An alternative approach separates the problem into two steps:

```python
def search_rotated_two_phase(nums: list[int], target: int) -> int:
    """
    Two-phase approach: find pivot, then search in appropriate half.

    Phase 1: Find the pivot (minimum element)
    Phase 2: Binary search in the correct half

    Time Complexity: O(log n)
    Space Complexity: O(1)
    """
    if not nums:
        return -1

    n = len(nums)

    # Phase 1: Find pivot (index of minimum element)
    left, right = 0, n - 1
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
    pivot = left

    # Phase 2: Determine which half to search
    left, right = 0, n - 1
    if target >= nums[pivot] and target <= nums[n - 1]:
        left = pivot
    else:
        right = pivot - 1

    # Phase 3: Standard binary search
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```


