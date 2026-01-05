# Binary Search Patterns: Complete Reference

> **API Kernel**: `BinarySearchBoundary`
> **Core Mechanism**: Systematically halve the search space by maintaining a predicate-based invariant until the boundary between true/false regions is found.

This document presents the **canonical binary search template** and all its major variations. Each implementation follows consistent naming conventions and includes detailed algorithmic explanations.

---

## Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Base Template: Predicate Boundary Search](#2-base-template-predicate-boundary-search)
3. [Variation: Exact Match Search](#3-variation-exact-match-search)
4. [Variation: Lower Bound / Upper Bound (LeetCode 34, 35)](#4-variation-lower-bound--upper-bound-leetcode-34-35)
5. [Variation: Rotated Sorted Array (LeetCode 33, 81)](#5-variation-rotated-sorted-array-leetcode-33-81)
6. [Variation: Binary Search on Answer Space (LeetCode 875, 1011)](#6-variation-binary-search-on-answer-space-leetcode-875-1011)
7. [Variation: Peak / Local Extremum (LeetCode 162)](#7-variation-peak--local-extremum-leetcode-162)
8. [Off-by-One Handling and Termination Guarantees](#8-off-by-one-handling-and-termination-guarantees)
9. [Pattern Comparison Table](#9-pattern-comparison-table)
10. [When to Use Binary Search](#10-when-to-use-binary-search)
11. [LeetCode Problem Mapping](#11-leetcode-problem-mapping)
12. [Template Quick Reference](#12-template-quick-reference)

---

## 1. Core Concepts

### 1.1 What is Binary Search?

Binary search is a **divide-and-conquer** algorithm that efficiently locates a target or boundary in a sorted/monotonic search space by repeatedly halving the search interval. Instead of examining all N elements (O(n)), binary search achieves O(log n) by eliminating half the remaining candidates at each step.

```
Search Space Reduction:
┌─────────────────────────────────────────────────────────────┐
│  [    left ──────────── mid ──────────── right    ]         │
│                          │                                   │
│    ◄──── eliminate ────► │ ◄──── or eliminate ────►         │
│                          │                                   │
│  After decision: search space reduced by half               │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Why Predicate/Boundary Search is the Canonical Kernel

Traditional binary search for "find exact value" is actually a **special case** of the more general **predicate boundary search**:

- **Predicate Boundary**: Find the first (or last) position where a condition becomes true
- **Exact Match**: Find where `arr[mid] == target` (predicate: `arr[i] >= target`)
- **Lower Bound**: Find first position where `arr[i] >= target`
- **Upper Bound**: Find first position where `arr[i] > target`

The predicate formulation unifies all binary search variants under one mental model:

```
Predicate View:
┌───────────────────────────────────────────────────────────┐
│  [F, F, F, F, F, T, T, T, T, T]                            │
│                ↑                                           │
│             boundary                                       │
│                                                            │
│  Find the FIRST index where predicate(arr[i]) is True     │
└───────────────────────────────────────────────────────────┘
```

### 1.3 The Core Invariant

Every binary search maintains this invariant throughout execution:

> **Invariant**: The answer (if it exists) lies within the range `[left, right]`.

When the loop terminates (`left > right` or `left == right`), the boundary has been found.

### 1.4 Sub-Pattern Classification

| Sub-Pattern | Key Characteristic | Examples |
|-------------|-------------------|----------|
| **Exact Match** | Find specific value | Classic binary search |
| **Lower Bound** | First position where `arr[i] >= target` | LeetCode 34, 35 |
| **Upper Bound** | First position where `arr[i] > target` | LeetCode 34 |
| **Rotated Array** | Split invariant across pivot | LeetCode 33, 81, 153 |
| **Answer Space** | Search over possible answers | LeetCode 875, 1011, 410 |
| **Peak Finding** | Neighbor comparison invariant | LeetCode 162, 852 |

---

## 2. Base Template: Predicate Boundary Search

> **Core Insight**: Binary search finds the boundary between false and true regions of a monotonic predicate.
> **Invariant**: `left` is always in the false region, `right` is always in the true region (or vice versa).
> **Result**: Upon termination, `left` points to the first true position.

### 2.1 Implementation

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

### 2.2 Why This Works

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

### 2.3 Loop Condition: `left < right` vs `left <= right`

| Condition | Termination | Use Case |
|-----------|-------------|----------|
| `left < right` | `left == right` (one element) | Boundary search (first true) |
| `left <= right` | `left > right` (empty range) | Exact match (may not exist) |

For predicate boundary search, `left < right` is preferred because:
- We always shrink to exactly one candidate
- No risk of infinite loop (each iteration reduces range by at least 1)
- The final `left` is guaranteed to be the answer or the bound

### 2.4 Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Integer overflow | `(left + right) / 2` overflows | Use `left + (right - left) // 2` |
| Infinite loop | `left` never increases | Ensure `left = mid + 1` when predicate is False |
| Off-by-one | Wrong boundary returned | Carefully define predicate semantics |
| Empty range | `left > right` initially | Handle edge case or validate input |

---

## 3. Variation: Exact Match Search

> **Problem**: Find the index of a specific target value.
> **Delta from Base**: Predicate is `arr[mid] >= target`, then verify exact match.
> **Use Case**: Classic binary search in sorted array.

### 3.1 Implementation

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

### 3.2 Key Difference from Boundary Search

| Aspect | Exact Match | Boundary Search |
|--------|-------------|-----------------|
| Loop condition | `left <= right` | `left < right` |
| On match | Return immediately | Continue to find first/last |
| Result | Single index or -1 | Boundary position |
| When not found | Returns -1 | Returns insertion point |

---

## 4. Variation: Lower Bound / Upper Bound (LeetCode 34, 35)

> **Lower Bound**: First index where `arr[i] >= target`
> **Upper Bound**: First index where `arr[i] > target`
> **Use Case**: Finding ranges, handling duplicates, insertion position.

### 4.1 Lower Bound Implementation

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

### 4.2 Upper Bound Implementation

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

### 4.3 Finding First and Last Position (LeetCode 34)

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

### 4.4 Search Insert Position (LeetCode 35)

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

### 4.5 Handling Duplicates

```
Array with duplicates: [1, 2, 2, 2, 2, 3, 4], target = 2

lower_bound(2) = 1  → First position where arr[i] >= 2
                      Points to first 2

upper_bound(2) = 5  → First position where arr[i] > 2
                      Points to 3 (element after last 2)

Count of 2s = upper_bound - lower_bound = 5 - 1 = 4
Range of 2s = [lower_bound, upper_bound - 1] = [1, 4]
```

---

## 5. Variation: Rotated Sorted Array (LeetCode 33, 81)

> **Problem**: Search in a sorted array that has been rotated at an unknown pivot.
> **Key Insight**: At least one half of the array around mid is always sorted.
> **Invariant**: Target is in the sorted half if it falls within that range.

### 5.1 Core Reasoning

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

### 5.2 Implementation (No Duplicates - LeetCode 33)

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

### 5.3 Implementation (With Duplicates - LeetCode 81)

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

### 5.4 Two-Phase Approach: Find Pivot Then Search

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

---

## 6. Variation: Binary Search on Answer Space (LeetCode 875, 1011)

> **Problem**: Find the minimum (or maximum) value that satisfies a feasibility predicate.
> **Key Insight**: The answer itself is what we binary search, not an index.
> **Invariant**: If `x` is feasible, all values greater (or less) are also feasible.

### 6.1 When to Use Binary Search on Answer

This pattern applies when:

1. You need to find an **optimal value** (minimize/maximize)
2. There's a **monotonic feasibility** condition
3. You can **check feasibility** in O(n) or better

```
Search Space for "Minimize Maximum":
┌─────────────────────────────────────────────────────────────┐
│  Answer Space: [min_possible, max_possible]                 │
│                                                             │
│  [infeasible, infeasible, ..., feasible, feasible, ...]    │
│                                   ↑                         │
│                              first feasible = answer        │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 Template

```python
def binary_search_on_answer(lo: int, hi: int, is_feasible) -> int:
    """
    Find the minimum value in [lo, hi] where is_feasible(x) is True.

    Requirements:
    - is_feasible is monotonic: if is_feasible(x), then is_feasible(x+1)
    - At least one value in [lo, hi] must be feasible

    This is exactly predicate boundary search over the answer space.

    Time Complexity: O(log(hi - lo) × feasibility_check)
    Space Complexity: O(1)

    Args:
        lo: Minimum possible answer (inclusive)
        hi: Maximum possible answer (inclusive)
        is_feasible: Function returning True if answer x is feasible

    Returns:
        Minimum feasible answer
    """
    while lo < hi:
        mid = lo + (hi - lo) // 2

        if is_feasible(mid):
            # mid works, but maybe something smaller also works
            hi = mid
        else:
            # mid doesn't work, need larger value
            lo = mid + 1

    return lo
```

### 6.3 Koko Eating Bananas (LeetCode 875)

```python
def min_eating_speed(piles: list[int], h: int) -> int:
    """
    Find minimum eating speed k to finish all bananas within h hours.

    Problem:
    - Each hour, Koko eats k bananas from one pile
    - If pile has less than k, she eats the whole pile and waits
    - Find minimum k such that total hours <= h

    Insight:
    - Answer space: [1, max(piles)]
    - If k=1 works, any larger k also works (monotonic)
    - Feasibility check: sum(ceil(pile/k) for pile in piles) <= h

    Predicate: can_finish(k) = total_hours(k) <= h

    Time Complexity: O(n × log(max(piles)))
    Space Complexity: O(1)

    Args:
        piles: Array of banana pile sizes
        h: Available hours

    Returns:
        Minimum eating speed
    """
    def hours_needed(speed: int) -> int:
        """Calculate total hours needed at given speed."""
        total = 0
        for pile in piles:
            # Ceiling division: (pile + speed - 1) // speed
            total += (pile + speed - 1) // speed
        return total

    def can_finish(speed: int) -> bool:
        """Check if Koko can finish within h hours at this speed."""
        return hours_needed(speed) <= h

    # Answer space: [1, max(piles)]
    # At speed = max(piles), each pile takes 1 hour
    lo, hi = 1, max(piles)

    while lo < hi:
        mid = lo + (hi - lo) // 2

        if can_finish(mid):
            # This speed works, try to find a smaller one
            hi = mid
        else:
            # Too slow, need faster eating
            lo = mid + 1

    return lo
```

### 6.4 Capacity To Ship Packages (LeetCode 1011)

```python
def ship_within_days(weights: list[int], days: int) -> int:
    """
    Find minimum ship capacity to ship all packages within given days.

    Problem:
    - Packages must be shipped in order (no reordering)
    - Each day, ship consecutive packages up to capacity
    - Find minimum capacity to finish in exactly `days` days

    Insight:
    - Minimum capacity = max(weights) (must fit largest package)
    - Maximum capacity = sum(weights) (ship everything in one day)
    - If capacity C works, C+1 also works (monotonic)

    Feasibility Check:
    - Greedily fill each day up to capacity
    - Count days needed
    - Return days_needed <= days

    Time Complexity: O(n × log(sum(weights)))
    Space Complexity: O(1)

    Args:
        weights: Array of package weights (in order)
        days: Number of days to ship all packages

    Returns:
        Minimum ship capacity
    """
    def days_needed(capacity: int) -> int:
        """Calculate days needed to ship all packages at given capacity."""
        day_count = 1
        current_load = 0

        for weight in weights:
            if current_load + weight > capacity:
                # Start a new day
                day_count += 1
                current_load = weight
            else:
                current_load += weight

        return day_count

    def can_ship(capacity: int) -> bool:
        """Check if all packages can be shipped within `days` days."""
        return days_needed(capacity) <= days

    # Answer space: [max(weights), sum(weights)]
    lo = max(weights)  # Must fit largest package
    hi = sum(weights)  # Can ship everything in one day

    while lo < hi:
        mid = lo + (hi - lo) // 2

        if can_ship(mid):
            # This capacity works, try smaller
            hi = mid
        else:
            # Need more capacity
            lo = mid + 1

    return lo
```

### 6.5 Common Answer Space Problems

| Problem | Answer Space | Feasibility Predicate | Monotonicity |
|---------|-------------|----------------------|--------------|
| Koko Eating Bananas | [1, max(piles)] | hours_needed <= h | Increasing k → decreasing hours |
| Ship Packages | [max(w), sum(w)] | days_needed <= d | Increasing cap → decreasing days |
| Split Array (410) | [max(nums), sum(nums)] | splits_needed <= m | Increasing max → decreasing splits |
| Magnetic Force (1552) | [1, max_dist] | can_place_balls | Increasing dist → harder to place |

---

## 7. Variation: Peak / Local Extremum (LeetCode 162)

> **Problem**: Find a peak element where `nums[i] > nums[i-1]` and `nums[i] > nums[i+1]`.
> **Key Insight**: If `nums[mid] < nums[mid+1]`, peak must exist on the right.
> **Invariant**: A peak always exists in the search range.

### 7.1 Why Binary Search Works for Peaks

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

### 7.2 Implementation

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

### 7.3 Mountain Array Variant (LeetCode 852)

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

---

## 8. Off-by-One Handling and Termination Guarantees

### 8.1 Mid Calculation: Left-Bias vs Right-Bias

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

### 8.2 Loop Invariant Verification

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

### 8.3 Inclusive vs Exclusive Bounds

| Style | Initialization | Loop Condition | Update Rules |
|-------|---------------|----------------|--------------|
| `[left, right]` | `left = 0, right = n - 1` | `left <= right` | `left = mid + 1`, `right = mid - 1` |
| `[left, right)` | `left = 0, right = n` | `left < right` | `left = mid + 1`, `right = mid` |

The `[left, right)` style with `left < right` is generally preferred for boundary search because:
- Natural for "find first" problems
- Final `left` directly gives the answer position
- Compatible with array slicing semantics

### 8.4 Edge Case Checklist

| Case | Handling |
|------|----------|
| Empty array | Return -1 or appropriate default |
| Single element | Loop body executes 0 times, return left |
| Target not found | Return insertion point or -1 |
| All elements equal | Works correctly if predicate handles it |
| Integer overflow | Use `left + (right - left) // 2` |
| Duplicates | Decide: first occurrence, last, or any |

---

## 9. Pattern Comparison Table

| Pattern | Search Space | Predicate | Loop Condition | Result |
|---------|-------------|-----------|----------------|--------|
| Exact Match | Array indices | `arr[mid] == target` | `left <= right` | Index or -1 |
| Lower Bound | Array indices | `arr[mid] >= target` | `left < right` | First >= |
| Upper Bound | Array indices | `arr[mid] > target` | `left < right` | First > |
| Rotated Search | Array indices | Sorted-half check | `left <= right` | Index or -1 |
| Answer Space | Value range | Feasibility check | `left < right` | Min feasible |
| Peak Finding | Array indices | Slope comparison | `left < right` | Peak index |

---

## 10. When to Use Binary Search

### 10.1 Problem Indicators

✅ **Use binary search when:**
- Sorted array or monotonic property
- Need to find a boundary or threshold
- Search space can be halved based on a condition
- O(log n) is required or beneficial
- "Minimize the maximum" or "maximize the minimum" problems

❌ **Don't use binary search when:**
- Data is unsorted and sorting is expensive
- No monotonic property exists
- Need to examine all elements anyway
- Search space cannot be meaningfully halved

### 10.2 Decision Flowchart

```
Is the problem about finding a specific element or boundary?
├── Yes → Is the data sorted or have monotonic property?
│         ├── Yes → Binary Search!
│         │         ├── Find exact value? → Exact match template
│         │         ├── Find first/last? → Lower/upper bound template
│         │         ├── Rotated array? → Rotated array template
│         │         └── Find optimal answer? → Answer space template
│         └── No → Can you sort it? Is it worth the cost?
│                   ├── Yes → Sort + Binary Search
│                   └── No → Use linear search or hash map
└── No → Binary search probably doesn't apply
```

---

## 11. LeetCode Problem Mapping

### 11.1 Boundary / Occurrence

| ID | Problem Name | Pattern | Difficulty |
|----|--------------|---------|------------|
| 34 | Find First and Last Position of Element in Sorted Array | Lower/Upper Bound | Medium |
| 35 | Search Insert Position | Lower Bound | Easy |
| 278 | First Bad Version | First True | Easy |
| 374 | Guess Number Higher or Lower | Predicate Search | Easy |

### 11.2 Rotated Array

| ID | Problem Name | Pattern | Difficulty |
|----|--------------|---------|------------|
| 33 | Search in Rotated Sorted Array | Rotated (distinct) | Medium |
| 81 | Search in Rotated Sorted Array II | Rotated (duplicates) | Medium |
| 153 | Find Minimum in Rotated Sorted Array | Find Pivot | Medium |
| 154 | Find Minimum in Rotated Sorted Array II | Find Pivot (dup) | Hard |

### 11.3 Binary Search on Answer Space

| ID | Problem Name | Pattern | Difficulty |
|----|--------------|---------|------------|
| 875 | Koko Eating Bananas | Min Speed | Medium |
| 1011 | Capacity To Ship Packages Within D Days | Min Capacity | Medium |
| 410 | Split Array Largest Sum | Min Max Sum | Hard |
| 774 | Minimize Max Distance to Gas Station | Min Max Distance | Hard |
| 1552 | Magnetic Force Between Two Balls | Max Min Distance | Medium |

### 11.4 Peak / Extremum

| ID | Problem Name | Pattern | Difficulty |
|----|--------------|---------|------------|
| 162 | Find Peak Element | Peak Finding | Medium |
| 852 | Peak Index in a Mountain Array | Peak Finding | Medium |
| 1095 | Find in Mountain Array | Peak + Search | Hard |

---

## 12. Template Quick Reference

### 12.1 Predicate Boundary (First True)

```python
def first_true(lo, hi, predicate):
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if predicate(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

### 12.2 Lower Bound

```python
def lower_bound(arr, target):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] >= target:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

### 12.3 Upper Bound

```python
def upper_bound(arr, target):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] > target:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

### 12.4 Rotated Array Search

```python
def search_rotated(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:  # Left sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:  # Right sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
```

### 12.5 Binary Search on Answer

```python
def min_feasible(lo, hi, is_feasible):
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if is_feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

### 12.6 Peak Finding

```python
def find_peak(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] < nums[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return lo
```



---



*Document generated for NeetCode Practice Framework — API Kernel: BinarySearchBoundary*
