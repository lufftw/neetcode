## Variation: Peak / Local Extremum (LeetCode 162)

> **Problem**: Find a peak element where `nums[i] > nums[i-1]` and `nums[i] > nums[i+1]`.
> **Key Insight**: If `nums[mid] < nums[mid+1]`, peak must exist on the right.
> **Invariant**: A peak always exists in the search range.

### Why Binary Search Works for Peaks

In an array where `nums[-1] = nums[n] = -∞` (conceptually), a peak always exists:

```
Observation: If nums[mid] < nums[mid + 1], we're on an ascending slope.
Following the ascending direction must eventually lead to a peak.

Case 1: Ascending at mid → peak exists in [mid + 1, right]
        [..., mid, mid+1, ...]
              ↗
        Go right

Case 2: Descending at mid → peak exists in [left, mid]
        [..., mid, mid+1, ...]
              ↘
        Go left (mid could be the peak)
```

### Implementation

```python
def find_peak_element(nums: list[int]) -> int:
    """
    Find a peak element and return its index.

    A peak element is strictly greater than its neighbors.
    The array may contain multiple peaks; return any one.

    Boundary conditions:
    - nums[-1] = nums[n] = -infinity (conceptually)
    - So nums[0] is a peak if nums[0] > nums[1]
    - And nums[n-1] is a peak if nums[n-1] > nums[n-2]

    Algorithm:
    - If nums[mid] < nums[mid + 1]: ascending slope, peak is on the right
    - If nums[mid] > nums[mid + 1]: descending slope, mid could be peak
    - Continue until single element remains

    Why we never skip a peak:
    - When we go right (ascending), we follow towards a peak
    - When we go left (descending), mid might be the peak, so we keep it

    Invariant:
    - There's always at least one peak in [left, right]

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Args:
        nums: Array where nums[i] != nums[i + 1] for all valid i

    Returns:
        Index of any peak element
    """
    left, right = 0, len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2

        if nums[mid] < nums[mid + 1]:
            # Ascending slope: peak must be in [mid + 1, right]
            # We can exclude mid because mid + 1 is greater
            left = mid + 1
        else:
            # Descending slope: peak is in [left, mid]
            # mid could be the peak, so include it
            right = mid

    # left == right: only one candidate, must be a peak
    return left
```

### Mountain Array Variant (LeetCode 852)

```python
def peak_index_in_mountain_array(arr: list[int]) -> int:
    """
    Find the peak index in a mountain array.

    Mountain array: arr[0] < arr[1] < ... < arr[peak] > ... > arr[n-1]
    Guaranteed to have exactly one peak.

    Same logic as find_peak_element.

    Time Complexity: O(log n)
    Space Complexity: O(1)
    """
    left, right = 0, len(arr) - 1

    while left < right:
        mid = left + (right - left) // 2

        if arr[mid] < arr[mid + 1]:
            left = mid + 1
        else:
            right = mid

    return left
```


