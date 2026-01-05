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
13. [Strict vs Non-Strict Inequality Strategy](#13-strict-vs-non-strict-inequality-strategy)
14. [Existence vs Optimization Binary Search](#14-existence-vs-optimization-binary-search)
15. [Search Domain Typing: Index vs Value Domain](#15-search-domain-typing-index-vs-value-domain)
16. [Boundary Stability Rule](#16-boundary-stability-rule)
17. [Binary Search + Greedy Combination Pattern](#17-binary-search--greedy-combination-pattern)
18. [Sentinel Bounds & Virtual Boundaries](#18-sentinel-bounds--virtual-boundaries)
19. [Binary Search Failure Modes](#19-binary-search-failure-modes)
20. [Binary Search vs Alternatives](#20-binary-search-vs-alternatives)
21. [Summary: The Complete Mental Model](#21-summary-the-complete-mental-model)

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

## 13. Strict vs Non-Strict Inequality Strategy

> **Core Insight**: The choice between `<` and `<=` is not about "which is correct" — it's about **invariant definition**.

### 13.1 The Real Pain Point

Many developers memorize `while left <= right` but don't understand **when to use `<` vs `<=`**. This leads to:
- Off-by-one errors
- Infinite loops
- Wrong boundary detection

### 13.2 Two Canonical Loop Styles

#### Style 1: `while left <= right` (Closed Interval)

```python
# Invariant: answer is in [left, right] (inclusive both ends)
left, right = 0, len(arr) - 1
while left <= right:
    mid = (left + right) // 2
    if condition(mid):
        right = mid - 1  # Exclude mid, search [left, mid-1]
    else:
        left = mid + 1   # Exclude mid, search [mid+1, right]
# Loop ends when left > right (empty interval)
```

**Use when:**
- Finding exact match
- Need to check every element
- Return -1 if not found

**Examples:** 704 (Binary Search), 33 (Search in Rotated)

#### Style 2: `while left < right` (Half-Open Interval)

```python
# Invariant: answer is in [left, right) or [left, right]
left, right = 0, len(arr)  # Note: right = len(arr), not len(arr)-1
while left < right:
    mid = (left + right) // 2
    if condition(mid):
        right = mid        # Keep mid in range, search [left, mid]
    else:
        left = mid + 1     # Exclude mid, search [mid+1, right]
# Loop ends when left == right (single candidate)
```

**Use when:**
- Finding boundary (first/last true)
- Answer guaranteed to exist
- Need the boundary position

**Examples:** 34 (First/Last Position), 35 (Search Insert), 875 (Koko Bananas)

### 13.3 Decision Matrix

| Question | Style 1 (`<=`) | Style 2 (`<`) |
|----------|---------------|---------------|
| Interval type | Closed `[l, r]` | Half-open `[l, r)` |
| Initial right | `len(arr) - 1` | `len(arr)` |
| When found | Move both boundaries | Move one boundary |
| Loop ends | `left > right` | `left == right` |
| Best for | Exact match | Boundary finding |

### 13.4 Why This Matters for Duplicates

With duplicates (LC 34, 81), the inequality choice determines:
- Whether you find **first** or **last** occurrence
- Whether boundary **includes** or **excludes** target

```python
# Find FIRST occurrence of target
while left < right:
    mid = (left + right) // 2
    if arr[mid] >= target:  # Include mid in left part
        right = mid
    else:
        left = mid + 1

# Find LAST occurrence of target
while left < right:
    mid = (left + right + 1) // 2  # Bias right to avoid infinite loop
    if arr[mid] <= target:  # Include mid in right part
        left = mid
    else:
        right = mid - 1
```

### 13.5 The Infinite Loop Trap

When `left < right` and you do `left = mid` (without +1), you risk infinite loop:

```
┌─────────────────────────────────────────────────┐
│  left = 3, right = 4                            │
│  mid = (3 + 4) // 2 = 3                         │
│  If left = mid → left = 3 (no progress!)        │
│                                                 │
│  Solution: Use mid = (left + right + 1) // 2    │
│  mid = (3 + 4 + 1) // 2 = 4                     │
│  Now left = mid → left = 4 (progress!)          │
└─────────────────────────────────────────────────┘
```

### 13.6 Covered Problems

| Problem | Inequality | Why |
|---------|-----------|-----|
| 34 First/Last Position | `<` | Finding boundaries with duplicates |
| 81 Rotated with Duplicates | `<=` | Need to check all, worst case linear |
| 875 Koko Eating Bananas | `<` | Finding minimum feasible answer |
| 1011 Ship Packages | `<` | Finding minimum capacity |
| 410 Split Array | `<` | Minimizing maximum sum |

---

## 14. Existence vs Optimization Binary Search

> **Core Insight**: Is the problem asking "Does it exist?" or "What's the optimal value?"

### 14.1 Two Fundamental Question Types

#### Type 1: Existence Query

**Question**: "Is target present?" / "Does a valid configuration exist?"

**Return Type**: `bool` or index (with -1 for not found)

**Template**:
```python
def exists(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return True  # or return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return False  # or return -1
```

**Characteristics**:
- Search terminates early on exact match
- Uses `left <= right` to check all candidates
- Often returns boolean or index

**Examples**: 704, 33, 81

#### Type 2: Optimization Query

**Question**: "What's the minimum/maximum valid value?"

**Return Type**: The actual value (int/float)

**Template**:
```python
def find_minimum(low, high, feasible):
    while low < high:
        mid = (low + high) // 2
        if feasible(mid):
            high = mid      # mid works, try smaller
        else:
            low = mid + 1   # mid doesn't work, need larger
    return low
```

**Characteristics**:
- Never terminates early (need to find optimal)
- Uses `left < right` to converge to answer
- Always returns a value (answer guaranteed to exist)

**Examples**: 875, 1011, 410, 774, 1283, 1482

### 14.2 Side-by-Side Comparison

| Aspect | Existence | Optimization |
|--------|-----------|--------------|
| Question | "Is it there?" | "What's the best?" |
| Return type | `bool` / `int` (-1) | `int` / `float` |
| Early termination | Yes (on match) | No (need boundary) |
| Loop condition | `left <= right` | `left < right` |
| Search space | Array indices | Value range |
| Predicate | `arr[mid] == target` | `feasible(mid)` |

### 14.3 Mapping to Template Choice

```
┌──────────────────────────────────────────────────────────┐
│  "Does X exist?"                                          │
│  ├── Yes → Use exact match template                       │
│  │         └── Returns: found index or -1                 │
│  │                                                        │
│  "What's the minimum/maximum X?"                          │
│  ├── Yes → Use first_true / last_true template            │
│  │         └── Returns: optimal value                     │
│  │                                                        │
│  Tip: Optimization often uses "first_true" for minimize   │
│       and "last_true" for maximize                        │
└──────────────────────────────────────────────────────────┘
```

### 14.4 Why first_true vs last_true?

For **minimize** problems (find minimum valid value):
```python
# Find first speed where Koko can finish
# Predicate: can_finish(speed) returns True/False
# [F, F, F, T, T, T, T] → find first T
def first_true(lo, hi, predicate):
    while lo < hi:
        mid = (lo + hi) // 2
        if predicate(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

For **maximize** problems (find maximum valid value):
```python
# Find maximum pages per day such that reading finishes
# [T, T, T, T, F, F, F] → find last T
def last_true(lo, hi, predicate):
    while lo < hi:
        mid = (lo + hi + 1) // 2  # Bias right
        if predicate(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo
```

### 14.5 Problem Classification

| Problem | Type | Return | Template |
|---------|------|--------|----------|
| 704 Binary Search | Existence | Index/-1 | Exact match |
| 33 Rotated Search | Existence | Index/-1 | Exact match + pivot |
| 81 Rotated (dupes) | Existence | bool | Exact match + linear fallback |
| 35 Search Insert | Optimization | Index | first_true (>= target) |
| 875 Koko Bananas | Optimization | Speed value | first_true (can finish) |
| 1011 Ship Packages | Optimization | Capacity | first_true (can ship) |
| 410 Split Array | Optimization | Max sum | first_true (can split) |

---

## 15. Search Domain Typing: Index vs Value Domain

> **Core Insight**: Binary search doesn't always run on array indices. Understanding the **domain** is crucial for correct setup.

### 15.1 Two Domain Types

#### Index Domain (Positional Search)

**Search space**: Array indices `[0, n-1]`

**What you're finding**: The position/index of an element

**Initialization**:
```python
left, right = 0, len(arr) - 1  # or len(arr) for half-open
```

**Examples**:
- Find target in sorted array → index
- Find first occurrence → index
- Find peak element → index
- Find rotation pivot → index

#### Value Domain (Answer Space Search)

**Search space**: Range of possible answer values `[min_val, max_val]`

**What you're finding**: The actual answer value (not its position)

**Initialization**:
```python
# Bounds come from problem constraints, NOT array length
left = min_possible_answer
right = max_possible_answer
```

**Examples**:
- Minimum eating speed → the speed value
- Minimum ship capacity → the capacity value
- Maximum split sum → the sum value

### 15.2 Why This Distinction Matters

Common mistakes when confusing domains:

| Mistake | Cause | Fix |
|---------|-------|-----|
| `left = 0, right = len(arr)` for value search | Using index bounds for value search | Use `left = min(arr), right = sum(arr)` |
| `return left` gives wrong value | Returning index when value needed | Ensure loop finds value, not position |
| `mid` interpretation wrong | Thinking mid is index, but it's value | Be explicit: `mid_speed`, `mid_capacity` |

### 15.3 Domain Classification by Problem

#### Index Domain Problems

| Problem | Search For | Bounds | Returns |
|---------|-----------|--------|---------|
| 704 Binary Search | Target index | `[0, n-1]` | Index |
| 33 Rotated Search | Target index | `[0, n-1]` | Index |
| 34 First/Last Position | Boundary index | `[0, n-1]` | Index |
| 162 Peak Element | Peak index | `[0, n-1]` | Index |
| 153 Rotated Minimum | Pivot index | `[0, n-1]` | Index |

#### Value Domain Problems

| Problem | Search For | Bounds | Returns |
|---------|-----------|--------|---------|
| 875 Koko Bananas | Eating speed | `[1, max(piles)]` | Speed |
| 1011 Ship Packages | Ship capacity | `[max(weights), sum(weights)]` | Capacity |
| 410 Split Array | Maximum sum | `[max(nums), sum(nums)]` | Sum |
| 774 Minimize Max Distance | Distance | `[0, max_gap]` | Distance |
| 1482 Min Days for Bouquets | Days | `[1, max(bloomDay)]` | Days |

### 15.4 Correct Bound Initialization

For **value domain** problems, bounds must guarantee the answer is included:

```python
# 875. Koko Eating Bananas
# Speed must be at least 1 (can't eat 0 bananas/hour)
# Speed at most max(piles) (can finish largest pile in 1 hour)
left, right = 1, max(piles)

# 1011. Capacity to Ship Packages
# Capacity must hold heaviest package
# Capacity at most total weight (ship everything in 1 day)
left, right = max(weights), sum(weights)

# 410. Split Array Largest Sum
# Min sum is largest element (one per subarray)
# Max sum is total (everything in one subarray)
left, right = max(nums), sum(nums)
```

### 15.5 Visual Domain Comparison

```
┌─────────────────────────────────────────────────────────────────┐
│  Index Domain                                                    │
│  ──────────────                                                  │
│  Search space: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]                   │
│                 └─────── array indices ───────┘                  │
│  mid = 4 means: "check element at position 4"                   │
│                                                                  │
│  Value Domain                                                    │
│  ────────────                                                    │
│  Search space: [1, 2, 3, ..., 1000000]                          │
│                 └─── possible answer values ───┘                 │
│  mid = 500 means: "test if 500 is a valid answer"              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 16. Boundary Stability Rule

> **Core Insight**: Why moving left/right this way is **always safe** — the correctness guarantee of binary search.

### 16.1 The Fundamental Question

> "How do we know we're not skipping the answer when we move boundaries?"

This is the **correctness proof** that separates confident programmers from those who trial-and-error.

### 16.2 The Invariant Guarantee

**Binary search correctness depends on maintaining this invariant**:

> After each iteration, the answer (if it exists) remains within `[left, right]`.

This means:
- When we move `left = mid + 1`, we're **certain** the answer is NOT in `[old_left, mid]`
- When we move `right = mid - 1` or `right = mid`, we're **certain** the answer is NOT in `(mid, old_right]`

### 16.3 Why We Never Skip the Answer

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

### 16.4 Comparison with Sliding Window Invariant

Like sliding window's "window always satisfies constraint", binary search has:

| Technique | Invariant | Guarantee |
|-----------|-----------|-----------|
| Sliding Window | Window always satisfies constraint | Expand/contract preserves validity |
| Binary Search | Answer always in `[left, right]` | Boundary moves preserve answer |

### 16.5 Common Mistakes That Violate Stability

| Mistake | Why It Breaks | Fix |
|---------|--------------|-----|
| `left = mid` with floor division | May not progress when `right = left + 1` | Use `mid = (l + r + 1) // 2` |
| `right = mid - 1` in first_true | Might exclude the answer | Use `right = mid` |
| Moving both when unsure | Double-moves can skip answer | Move only the correct boundary |

### 16.6 The Safety Checklist

Before finalizing binary search code, verify:

1. ✅ **Predicate is monotonic**: All F before all T (or vice versa)
2. ✅ **Boundary move preserves answer**: New range still contains answer
3. ✅ **Loop makes progress**: Interval shrinks every iteration
4. ✅ **Termination is correct**: Final `left` (or `right`) is the answer

---

## 17. Binary Search + Greedy Combination Pattern

> **Core Insight**: Many answer-space problems are "**Greedy feasibility check + Binary search over answers**".

### 17.1 The Pattern Structure

```python
def solve(nums, constraint):
    left, right = min_answer, max_answer

    def is_feasible(candidate):
        """Greedy check: can we achieve this candidate value?"""
        # Use greedy algorithm to verify feasibility
        return greedy_check(nums, candidate, constraint)

    while left < right:
        mid = (left + right) // 2
        if is_feasible(mid):
            right = mid      # or left = mid for maximize
        else:
            left = mid + 1   # or right = mid - 1 for maximize
    return left
```

### 17.2 Why This Pattern Is So Common

**The "capacity/rate/limit" family** all share this structure:

1. **Binary search** over the answer space (what's the optimal value?)
2. **Greedy simulation** to check feasibility (can this value work?)

The greedy part is crucial — it's **O(n)** and determines the overall **O(n log range)** complexity.

### 17.3 Pattern Examples

#### 875. Koko Eating Bananas

```python
def minEatingSpeed(piles, h):
    left, right = 1, max(piles)

    def can_finish(speed):
        # Greedy: eat each pile, count hours
        hours = sum((pile + speed - 1) // speed for pile in piles)
        return hours <= h

    while left < right:
        mid = (left + right) // 2
        if can_finish(mid):
            right = mid
        else:
            left = mid + 1
    return left
```

#### 1011. Capacity to Ship Packages

```python
def shipWithinDays(weights, days):
    left, right = max(weights), sum(weights)

    def can_ship(capacity):
        # Greedy: load packages until capacity, count days
        day_count, current_load = 1, 0
        for w in weights:
            if current_load + w > capacity:
                day_count += 1
                current_load = 0
            current_load += w
        return day_count <= days

    while left < right:
        mid = (left + right) // 2
        if can_ship(mid):
            right = mid
        else:
            left = mid + 1
    return left
```

#### 410. Split Array Largest Sum

```python
def splitArray(nums, k):
    left, right = max(nums), sum(nums)

    def can_split(max_sum):
        # Greedy: start new subarray when sum exceeds max_sum
        splits, current_sum = 1, 0
        for num in nums:
            if current_sum + num > max_sum:
                splits += 1
                current_sum = 0
            current_sum += num
        return splits <= k

    while left < right:
        mid = (left + right) // 2
        if can_split(mid):
            right = mid
        else:
            left = mid + 1
    return left
```

### 17.4 The Greedy Feasibility Check Pattern

All these problems share the same greedy structure:

```python
def is_feasible(limit):
    count = 1  # Start with 1 group/day/split
    current = 0

    for item in items:
        if current + item > limit:
            count += 1       # Start new group
            current = 0
        current += item

    return count <= allowed_groups
```

### 17.5 Why This Matters for System Design

This pattern abstracts to:
- **Rate limiting**: What's the minimum rate to handle load?
- **Resource allocation**: What's the minimum capacity needed?
- **Load balancing**: What's the optimal split?

The predicate abstraction (`is_feasible`) is a powerful design pattern.

### 17.6 Covered Problems

| Problem | Search For | Greedy Check |
|---------|-----------|--------------|
| 875 Koko Bananas | Min speed | Can eat all piles in h hours? |
| 1011 Ship Packages | Min capacity | Can ship all in d days? |
| 410 Split Array | Min max-sum | Can split into k subarrays? |
| 774 Min Max Distance | Min distance | Can place k gas stations? |
| 1482 Min Days | Min days | Can make m bouquets? |

---

## 18. Sentinel Bounds & Virtual Boundaries

> **Core Insight**: `low` and `high` don't always come from the array — they come from **problem constraints**.

### 18.1 Understanding Virtual Boundaries

For **answer space** problems, bounds are derived from:
- Problem constraints (min/max possible values)
- Mathematical guarantees (what must be true)

Not from:
- Array length
- Array indices

### 18.2 Bound Derivation Patterns

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

### 18.3 Common Bound Formulas

| Problem Type | left | right |
|-------------|------|-------|
| Min capacity | `max(items)` | `sum(items)` |
| Min speed | `1` | `max(items)` |
| Min time | `1` | `max(times)` |
| Max distance | `0` | `total_distance` |

### 18.4 Why Beginners Get This Wrong

Common mistakes:

| Wrong | Why It's Wrong | Correct |
|-------|---------------|---------|
| `left = 0` for capacity | Can't have 0 capacity | `left = max(weights)` |
| `right = len(arr)` | Confusing index with value domain | `right = sum(arr)` |
| `left = 1` for all | Sometimes min must be larger | Analyze constraints |

### 18.5 The Guarantee Principle

**Both bounds must guarantee the answer is included**:

1. `left` = smallest value that MIGHT work
2. `right` = largest value that DEFINITELY works

This ensures binary search can't miss the answer.

### 18.6 Example: Why `max(weights)` for Shipping?

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

---

## 19. Binary Search Failure Modes

> **Core Insight**: Systematic error classification helps debug faster than trial-and-error.

### 19.1 Failure Mode Taxonomy

#### Mode 1: Infinite Loop

**Symptom**: Program never terminates

**Causes**:
- `left = mid` with `mid = (left + right) // 2` when `right = left + 1`
- No boundary movement in some branch
- Wrong loop condition

**Fix**:
```python
# If doing left = mid, use ceiling division
mid = (left + right + 1) // 2

# Verify both branches move boundaries
if condition:
    right = mid      # or right = mid - 1
else:
    left = mid + 1   # Must have + 1
```

#### Mode 2: Boundary Never Moves

**Symptom**: Loop exits immediately or after 1 iteration

**Causes**:
- Wrong initial bounds
- Condition always True or always False
- Wrong inequality direction

**Fix**:
```python
# Check initial bounds include answer
assert left <= answer <= right

# Check predicate has transition
assert not predicate(left) and predicate(right)  # for first_true
```

#### Mode 3: Wrong Mid Bias

**Symptom**: Off-by-one errors, returns adjacent element

**Causes**:
- Using floor when ceiling needed (or vice versa)
- first_true vs last_true confusion

**Fix**:
```python
# first_true: floor division, move right
mid = (left + right) // 2
right = mid

# last_true: ceiling division, move left
mid = (left + right + 1) // 2
left = mid
```

#### Mode 4: Predicate Not Monotonic

**Symptom**: Wrong answer, inconsistent behavior

**Causes**:
- Predicate doesn't have clean F→T or T→F transition
- Multiple transitions in predicate

**Fix**:
```python
# Verify predicate is monotonic
# All False before all True (or vice versa)
[F, F, F, T, T, T]  # OK
[F, T, F, T, F, T]  # NOT OK - can't use binary search
```

#### Mode 5: Wrong Inequality Under Duplicates

**Symptom**: Finds wrong occurrence (first vs last)

**Causes**:
- Using `>` when should use `>=` (or vice versa)
- Not handling equality case correctly

**Fix**:
```python
# First occurrence: include mid in right part when equal
if arr[mid] >= target:
    right = mid

# Last occurrence: include mid in left part when equal
if arr[mid] <= target:
    left = mid
```

### 19.2 Debug Checklist

When binary search fails, check in order:

1. ☐ **Bounds correct?** — Does `[left, right]` include the answer?
2. ☐ **Predicate monotonic?** — Clean F→T transition?
3. ☐ **Loop makes progress?** — Does interval shrink each iteration?
4. ☐ **Correct mid formula?** — Floor for first_true, ceiling for last_true?
5. ☐ **Boundary moves correct?** — Does answer stay in range?
6. ☐ **Return value correct?** — Return `left` or `right`?

---

## 20. Binary Search vs Alternatives

> **Core Insight**: Know when NOT to use binary search.

### 20.1 When Binary Search Applies

✅ **Use binary search when:**
- Sorted or monotonic property exists
- Search space can be halved by a predicate
- O(log n) gives meaningful improvement
- Clear true/false boundary exists

### 20.2 When to Use Alternatives

#### Alternative 1: Hash Map (O(1) lookup)

**Use instead when:**
- Need exact match in unsorted data
- Multiple lookups expected
- Space O(n) is acceptable

**Example**: Two Sum (unsorted) — hash map beats sorting + binary search

#### Alternative 2: Two Pointers (O(n) traverse)

**Use instead when:**
- Need to examine pairs/triplets
- Sorted data but need all combinations
- Search + constraint is better expressed as pointer movement

**Example**: 3Sum — two pointers on sorted array

#### Alternative 3: Sliding Window

**Use instead when:**
- Contiguous subarray/substring
- Add/remove elements incrementally
- Window property is monotonic

**Example**: Minimum Window Substring — can't binary search, need sliding window

#### Alternative 4: Linear Scan

**Use instead when:**
- Data is small (n < 100)
- Binary search overhead not worth it
- Need to check all elements anyway

### 20.3 Decision Matrix

| Problem Type | Binary Search | Alternative |
|-------------|---------------|-------------|
| Find in sorted array | ✅ Yes | - |
| Find in unsorted array | ❌ No | Hash map |
| Optimize with monotonic predicate | ✅ Yes | - |
| All pairs with constraint | ❌ No | Two pointers |
| Contiguous subarray optimization | ❌ No | Sliding window |
| Small n (< 100) | Maybe | Linear might be simpler |

### 20.4 Boundary with Other Patterns

```
┌─────────────────────────────────────────────────────────────────┐
│                    Pattern Selection Guide                       │
├─────────────────────────────────────────────────────────────────┤
│  Sorted array + find element?                                    │
│  └── Binary Search                                               │
│                                                                  │
│  Sorted array + find pair summing to target?                    │
│  └── Two Pointers (not binary search each element)             │
│                                                                  │
│  Unsorted array + find pair summing to target?                  │
│  └── Hash Map                                                    │
│                                                                  │
│  Find optimal subarray length?                                   │
│  └── Sliding Window (if property monotonic in window size)     │
│  └── Binary Search (if answer space is discrete)               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 21. Summary: The Complete Mental Model

These 8 concepts form a complete decision framework:

| # | Concept | Key Question |
|---|---------|--------------|
| 1 | Inequality Strategy | `<=` vs `<` — which loop style? |
| 2 | Existence vs Optimization | bool vs value — what to return? |
| 3 | Domain Typing | Index vs Value — what are bounds? |
| 4 | Boundary Stability | Why is this correct? |
| 5 | + Greedy Pattern | What's the O(n) feasibility check? |
| 6 | Sentinel Bounds | How to derive bounds? |
| 7 | Failure Modes | How to debug? |
| 8 | vs Alternatives | When NOT to use? |

With these concepts, binary search becomes as **transferable** as sliding window — a systematic approach rather than memorized templates.



---



*Document generated for NeetCode Practice Framework — API Kernel: BinarySearchBoundary*
