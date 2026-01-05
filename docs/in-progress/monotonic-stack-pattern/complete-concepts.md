# Monotonic Stack Patterns: Complete Reference

> **API Kernel**: `MonotonicStack`
> **Core Mechanism**: Boundary / Candidate Resolution via Monotonicity — maintain a stack in strictly or non-strictly increasing/decreasing order to efficiently resolve boundary queries (next greater, next smaller, span, interval expansion) in amortized O(1) per element.

This document presents the **canonical monotonic stack template** and all its major variations. Each implementation follows consistent naming conventions and includes detailed algorithmic explanations.

---

## Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Base Template: Next Greater / Next Smaller Boundaries](#2-base-template-next-greater--next-smaller-boundaries)
3. [Variation: Circular Boundary Search](#3-variation-circular-boundary-search)
4. [Variation: Histogram / Interval Expansion](#4-variation-histogram--interval-expansion)
5. [Variation: Span / Distance Aggregation](#5-variation-span--distance-aggregation)
6. [Variation: Contribution / Counting via Boundaries](#6-variation-contribution--counting-via-boundaries)
7. [Variation: Container / Valley Resolution](#7-variation-container--valley-resolution)
8. [Variation: Greedy Monotonic Stack](#8-variation-greedy-monotonic-stack)
9. [Off-by-One, Comparison Semantics, and Robustness](#9-off-by-one-comparison-semantics-and-robustness)
10. [Termination Guarantees (Amortized Analysis)](#10-termination-guarantees-amortized-analysis)
11. [Pattern Comparison Table](#11-pattern-comparison-table)
12. [When to Use Monotonic Stack](#12-when-to-use-monotonic-stack)
13. [LeetCode Problem Mapping](#13-leetcode-problem-mapping)
14. [Template Quick Reference](#14-template-quick-reference)

---

## 1. Core Concepts

### 1.1 What is a Monotonic Stack?

A monotonic stack is a stack that maintains elements in a **monotonically increasing or decreasing order**. When a new element violates this order, we pop elements from the stack until the invariant is restored.

```
Monotonic Decreasing Stack (for Next Greater Element):
┌─────────────────────────────────────────────────────────────┐
│  Push: Only push if element < stack top (maintains order)   │
│  Pop:  Pop while stack top < current element                │
│        → Each popped element finds its "next greater"       │
│                                                              │
│  Stack state: [largest, ..., smallest]                      │
│               └──── bottom ────┘  └─ top                    │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Why Boundary / Candidate Resolution is the Canonical Kernel

The monotonic stack solves a fundamental class of problems: **finding the nearest element satisfying a comparison condition**. This includes:

- **Next Greater Element (NGE)**: For each element, find the first element to the right that is greater
- **Previous Smaller Element (PSE)**: For each element, find the first element to the left that is smaller
- **Span queries**: How many consecutive elements are smaller/greater?
- **Interval expansion**: How far can we extend left/right while maintaining a property?

All these reduce to the same core mechanism: **when we pop an element from the stack, the current element becomes its boundary**.

### 1.3 The Core Invariant

Every monotonic stack algorithm maintains this invariant:

> **Invariant**: The stack contains candidate elements that have not yet found their boundary, ordered monotonically.

When we encounter a new element that violates the monotonic order:
1. Pop elements until order is restored
2. Each popped element has found its boundary (the current element)
3. Push the current element as a new candidate

### 1.4 Stack Stores Indices (Canonical Form)

**Always store indices in the stack, not values.** This provides:
- Access to both position and value via `arr[stack[-1]]`
- Ability to compute distances (`current_index - stack[-1]`)
- Consistent interface across all monotonic stack variants

```python
# Canonical: Store indices
stack = []  # stack of indices
for i, val in enumerate(arr):
    while stack and arr[stack[-1]] < val:
        idx = stack.pop()
        # arr[idx] found its next greater at position i
    stack.append(i)  # Push index, not value
```

### 1.5 Resolve on Pop Semantics

The key insight of monotonic stack is that **boundaries are resolved when elements are popped**, not when they are pushed:

```
Processing: [2, 1, 5, 6, 2, 3]

Step 1: Push 2 (idx=0)     Stack: [0]
Step 2: Push 1 (idx=1)     Stack: [0, 1]   (1 < 2, order maintained)
Step 3: See 5
        Pop 1 → 1's NGE is 5 (at idx=2)
        Pop 2 → 2's NGE is 5 (at idx=2)
        Push 5 (idx=2)     Stack: [2]
Step 4: Push 6 (idx=3)     Stack: [2, 3]
Step 5: See 2
        (2 < 6, just push)
        Push 2 (idx=4)     Stack: [2, 3, 4]
Step 6: See 3
        Pop 2 → 2's NGE is 3 (at idx=5)
        Push 3 (idx=5)     Stack: [2, 3, 5]

Final: Elements [5, 6, 3] have no NGE (remain in stack)
```

---

## 2. Base Template: Next Greater / Next Smaller Boundaries

> **Pattern**: Find, for each element, the nearest element satisfying a comparison condition.
> **Invariant**: Stack contains indices of elements awaiting their boundary, in monotonic order.
> **Role**: BASE TEMPLATE for `MonotonicStack` API Kernel.

### 2.1 Four Boundary Directions

| Pattern | Direction | Stack Order | Comparison | Common Name |
|---------|-----------|-------------|------------|-------------|
| NGE-R | Next Greater to Right | Decreasing | `>` | Next Greater Element |
| NGE-L | Next Greater to Left | Decreasing (reverse) | `>` | Previous Greater Element |
| NSE-R | Next Smaller to Right | Increasing | `<` | Next Smaller Element |
| PSE-L | Previous Smaller to Left | Increasing (reverse) | `<` | Previous Smaller Element |

### 2.2 Next Greater Element to the Right (NGE-R)

```python
def next_greater_element(nums: list[int]) -> list[int]:
    """
    For each element, find the next greater element to its right.
    Returns -1 if no such element exists.

    Algorithm:
    - Maintain a monotonically decreasing stack (by value)
    - When current element > stack top, stack top found its NGE
    - Each element is pushed once and popped at most once → O(n)

    Time: O(n), Space: O(n)
    """
    n = len(nums)
    result = [-1] * n  # Default: no next greater
    stack = []  # Stack of indices, values are decreasing

    for i in range(n):
        # Pop all elements smaller than current (they found their NGE)
        while stack and nums[stack[-1]] < nums[i]:
            idx = stack.pop()
            result[idx] = nums[i]  # or result[idx] = i for index
        stack.append(i)

    return result
```

### 2.3 Previous Smaller Element to the Left (PSE-L)

```python
def previous_smaller_element(nums: list[int]) -> list[int]:
    """
    For each element, find the previous smaller element to its left.
    Returns -1 if no such element exists.

    Algorithm:
    - Maintain a monotonically increasing stack (by value)
    - For each element, pop until we find a smaller element
    - The stack top (if exists) is the previous smaller element

    Time: O(n), Space: O(n)
    """
    n = len(nums)
    result = [-1] * n
    stack = []  # Stack of indices, values are increasing

    for i in range(n):
        # Pop elements >= current (they can't be PSE for future elements)
        while stack and nums[stack[-1]] >= nums[i]:
            stack.pop()

        # Stack top (if exists) is the previous smaller element
        if stack:
            result[i] = nums[stack[-1]]  # or stack[-1] for index

        stack.append(i)

    return result
```

### 2.4 Returning Value vs Index vs Distance

The same algorithm can return different information based on the problem:

```python
def next_greater_variants(nums: list[int]) -> tuple[list[int], list[int], list[int]]:
    """
    Compute NGE returning value, index, and distance.
    """
    n = len(nums)
    nge_value = [-1] * n     # The value of next greater element
    nge_index = [-1] * n     # The index of next greater element
    nge_distance = [0] * n   # Distance to next greater element
    stack = []

    for i in range(n):
        while stack and nums[stack[-1]] < nums[i]:
            idx = stack.pop()
            nge_value[idx] = nums[i]
            nge_index[idx] = i
            nge_distance[idx] = i - idx
        stack.append(i)

    return nge_value, nge_index, nge_distance
```

### 2.5 Handling Duplicates: Strict vs Non-Strict Comparisons

**Strict comparison (`<` or `>`)**: Equal elements do NOT satisfy the boundary condition.

```python
# Strict: Find next STRICTLY greater (not equal)
while stack and nums[stack[-1]] < nums[i]:  # < means strictly less
    # ...
```

**Non-strict comparison (`<=` or `>=`)**: Equal elements DO satisfy the boundary condition.

```python
# Non-strict: Find next greater or equal
while stack and nums[stack[-1]] <= nums[i]:  # <= includes equal
    # ...
```

**When to use which:**
- **Strict**: Default for most problems (Next Greater Element)
- **Non-strict**: When duplicates should be treated as boundaries (e.g., contribution counting to avoid double-counting)

---

## 3. Variation: Circular Boundary Search

> **Problem**: Find next greater element in a circular array (LeetCode 503).
> **Key Insight**: Traverse the array twice (2n iterations), but only push indices during the first pass.

### 3.1 Implementation

```python
def next_greater_circular(nums: list[int]) -> list[int]:
    """
    Find next greater element in circular array.

    Algorithm:
    - Traverse array twice (indices 0 to 2n-1)
    - Use modulo to wrap around: actual_index = i % n
    - Only push indices during first pass (i < n)
    - Second pass only resolves remaining elements

    Time: O(n), Space: O(n)
    """
    n = len(nums)
    result = [-1] * n
    stack = []

    for i in range(2 * n):
        actual_idx = i % n

        # Pop elements that found their circular NGE
        while stack and nums[stack[-1]] < nums[actual_idx]:
            idx = stack.pop()
            result[idx] = nums[actual_idx]

        # Only push during first pass to avoid duplicate processing
        if i < n:
            stack.append(actual_idx)

    return result
```

### 3.2 Why Push Only in First Pass?

If we push in both passes, indices would be duplicated:
- First pass pushes index 0
- Second pass would push index 0 again (since 2n % n = 0)

By limiting pushes to the first pass, each index is pushed exactly once.

### 3.3 Termination and "No Boundary" Cases

After 2n iterations:
- Elements remaining in stack have no next greater element in the circular array
- Their result stays -1 (the default)

---

## 4. Variation: Histogram / Interval Expansion

> **Problem**: Find the largest rectangle in a histogram (LeetCode 84).
> **Key Insight**: For each bar, find its left and right boundaries (first smaller bar), then compute area.

### 4.1 Core Insight: Interval Expansion via Boundaries

For each bar at index `i` with height `h`:
- **Left boundary**: First bar to the left that is shorter (`left_smaller[i]`)
- **Right boundary**: First bar to the right that is shorter (`right_smaller[i]`)
- **Width**: `right_smaller[i] - left_smaller[i] - 1`
- **Area**: `h * width`

```
Histogram: [2, 1, 5, 6, 2, 3]

Bar at index 2 (height 5):
  Left boundary: index 1 (height 1 < 5)
  Right boundary: index 4 (height 2 < 5)
  Width: 4 - 1 - 1 = 2
  Area: 5 * 2 = 10
```

### 4.2 Two-Pass Approach

```python
def largest_rectangle_two_pass(heights: list[int]) -> int:
    """
    Largest rectangle using two passes for left/right boundaries.

    Time: O(n), Space: O(n)
    """
    n = len(heights)
    left_smaller = [-1] * n   # Index of first smaller bar to left
    right_smaller = [n] * n   # Index of first smaller bar to right

    # Pass 1: Find left boundaries (previous smaller)
    stack = []
    for i in range(n):
        while stack and heights[stack[-1]] >= heights[i]:
            stack.pop()
        left_smaller[i] = stack[-1] if stack else -1
        stack.append(i)

    # Pass 2: Find right boundaries (next smaller)
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and heights[stack[-1]] >= heights[i]:
            stack.pop()
        right_smaller[i] = stack[-1] if stack else n
        stack.append(i)

    # Compute maximum area
    max_area = 0
    for i in range(n):
        width = right_smaller[i] - left_smaller[i] - 1
        area = heights[i] * width
        max_area = max(max_area, area)

    return max_area
```

### 4.3 Single-Pass with Sentinel

```python
def largest_rectangle_single_pass(heights: list[int]) -> int:
    """
    Largest rectangle using single pass with sentinel.

    The sentinel (0 at end) forces all remaining bars to be popped,
    completing their rectangle computation.

    Time: O(n), Space: O(n)
    """
    heights = heights + [0]  # Sentinel: forces final flush
    stack = [-1]  # Virtual left boundary
    max_area = 0

    for i, h in enumerate(heights):
        while stack[-1] != -1 and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)

    return max_area
```

### 4.4 Sentinel-Based Flushing

The sentinel pattern ensures all elements are processed:
- **Right sentinel** (`heights.append(0)`): A bar of height 0 is smaller than all bars, forcing all stack elements to pop
- **Left sentinel** (`stack = [-1]`): A virtual boundary at index -1 handles the case when stack becomes empty

### 4.5 Strict vs Non-Strict for Duplicates

For duplicate heights, use **non-strict** comparison (`>=` instead of `>`):

```python
# With duplicates: [2, 2, 2]
# Using > (strict): Each bar stops at its immediate neighbor
# Using >= (non-strict): Each bar extends through equal-height bars

while stack[-1] != -1 and heights[stack[-1]] >= h:  # >= for duplicates
```

This ensures correct width calculation when adjacent bars have equal height.

### 4.6 Maximal Rectangle in Binary Matrix (LeetCode 85)

```python
def maximal_rectangle(matrix: list[list[str]]) -> int:
    """
    Find largest rectangle of 1s in binary matrix.

    Algorithm:
    - Build histogram row by row
    - Each cell's height = consecutive 1s above (including current)
    - Apply largest_rectangle_in_histogram to each row

    Time: O(m * n), Space: O(n)
    """
    if not matrix or not matrix[0]:
        return 0

    n = len(matrix[0])
    heights = [0] * n
    max_area = 0

    for row in matrix:
        # Update histogram
        for j in range(n):
            heights[j] = heights[j] + 1 if row[j] == '1' else 0

        # Find largest rectangle in current histogram
        max_area = max(max_area, largest_rectangle_single_pass(heights[:]))

    return max_area
```

---

## 5. Variation: Span / Distance Aggregation

> **Problem**: Compute how many consecutive days the stock price was less than or equal to today's price (LeetCode 901).
> **Key Insight**: Span = distance to previous greater element.

### 5.1 Daily Temperatures (LeetCode 739)

```python
def daily_temperatures(temperatures: list[int]) -> list[int]:
    """
    For each day, find how many days until a warmer temperature.
    This is the distance to the next greater element.

    Time: O(n), Space: O(n)
    """
    n = len(temperatures)
    result = [0] * n
    stack = []  # Stack of indices, temperatures are decreasing

    for i in range(n):
        while stack and temperatures[stack[-1]] < temperatures[i]:
            idx = stack.pop()
            result[idx] = i - idx  # Distance to next greater
        stack.append(i)

    return result
```

### 5.2 Online Stock Span (LeetCode 901)

```python
class StockSpanner:
    """
    Online computation of stock span.
    Span = number of consecutive days with price <= today's price.

    Key insight: Span includes the current day plus all days
    that were "dominated" by previous greater prices.

    Stack stores (price, span) pairs.
    """
    def __init__(self):
        self.stack = []

    def next(self, price: int) -> int:
        span = 1  # Current day counts

        # Pop and accumulate spans of dominated days
        while self.stack and self.stack[-1][0] <= price:
            _, prev_span = self.stack.pop()
            span += prev_span

        self.stack.append((price, span))
        return span
```

### 5.3 Span Interpretation

The span at position `i` represents:
- **Count interpretation**: Number of consecutive elements to the left that are dominated
- **Distance interpretation**: `i - index_of_previous_greater_element`

---

## 6. Variation: Contribution / Counting via Boundaries

> **Problem**: Sum of subarray minimums (LeetCode 907).
> **Key Insight**: Each element's contribution = element × (left_count) × (right_count).

### 6.1 Contribution Counting Formula

For element at index `i` with value `v`:
- Let `L` = number of consecutive elements to the left where `v` is the minimum
- Let `R` = number of consecutive elements to the right where `v` is the minimum
- Element's contribution to total sum = `v × L × R`

This counts exactly how many subarrays have `v` as their minimum.

```
Array: [3, 1, 2, 4]
Element 1 at index 1:
  L = 2 (can extend to include index 0)
  R = 3 (can extend to include indices 2, 3)
  Contribution = 1 × 2 × 3 = 6

  Subarrays where 1 is minimum:
  [3,1], [1], [1,2], [1,2,4], [3,1,2], [3,1,2,4] → 6 subarrays
```

### 6.2 Sum of Subarray Minimums (LeetCode 907)

```python
def sum_of_subarray_minimums(arr: list[int]) -> int:
    """
    Sum of minimums of all subarrays.

    Algorithm:
    - For each element, find left/right boundaries (previous/next smaller)
    - Use asymmetric tie-breaking to avoid double-counting duplicates:
      - Left boundary: strictly smaller (<)
      - Right boundary: smaller or equal (<=)

    Time: O(n), Space: O(n)
    """
    MOD = 10**9 + 7
    n = len(arr)

    # left[i] = distance to previous smaller element
    # right[i] = distance to next smaller or equal element
    left = [0] * n
    right = [0] * n

    # Compute left boundaries (previous strictly smaller)
    stack = []
    for i in range(n):
        while stack and arr[stack[-1]] >= arr[i]:  # >= for strict <
            stack.pop()
        left[i] = i - stack[-1] if stack else i + 1
        stack.append(i)

    # Compute right boundaries (next smaller or equal)
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] > arr[i]:  # > for <=
            stack.pop()
        right[i] = stack[-1] - i if stack else n - i
        stack.append(i)

    # Sum contributions
    result = 0
    for i in range(n):
        result = (result + arr[i] * left[i] * right[i]) % MOD

    return result
```

### 6.3 Asymmetric Tie-Breaking for Duplicates

When duplicates exist, we must avoid counting the same subarray twice:
- **Left boundary**: Use strict comparison (`<`) → previous strictly smaller
- **Right boundary**: Use non-strict comparison (`<=`) → next smaller or equal

This creates a "left-closed, right-open" style where each subarray is counted exactly once.

### 6.4 Sum of Subarray Ranges (LeetCode 2104)

```python
def sum_of_subarray_ranges(nums: list[int]) -> int:
    """
    Sum of (max - min) for all subarrays.

    = Sum of all subarray maximums - Sum of all subarray minimums

    Use dual stacks: one for max contribution, one for min contribution.

    Time: O(n), Space: O(n)
    """
    n = len(nums)

    def sum_of_extremes(compare_greater: bool) -> int:
        """Compute sum of subarray max (if True) or min (if False)."""
        left = [0] * n
        right = [0] * n
        stack = []

        # Comparison functions for max vs min
        def dominates(a, b):
            return a > b if compare_greater else a < b

        def dominates_or_equal(a, b):
            return a >= b if compare_greater else a <= b

        # Left boundaries
        for i in range(n):
            while stack and dominates_or_equal(nums[i], nums[stack[-1]]):
                stack.pop()
            left[i] = i - stack[-1] if stack else i + 1
            stack.append(i)

        # Right boundaries
        stack = []
        for i in range(n - 1, -1, -1):
            while stack and dominates(nums[i], nums[stack[-1]]):
                stack.pop()
            right[i] = stack[-1] - i if stack else n - i
            stack.append(i)

        return sum(nums[i] * left[i] * right[i] for i in range(n))

    sum_max = sum_of_extremes(True)
    sum_min = sum_of_extremes(False)
    return sum_max - sum_min
```

---

## 7. Variation: Container / Valley Resolution

> **Problem**: Calculate trapped rainwater (LeetCode 42).
> **Key Insight**: Each "pop" completes a valley — water trapped between left wall, bottom, and right wall.

### 7.1 Stack-Based Trapping Rain Water

```python
def trap(height: list[int]) -> int:
    """
    Calculate total trapped rainwater.

    Algorithm:
    - Maintain a monotonically decreasing stack
    - When we see a taller bar, we've found a valley
    - Pop the bottom of the valley, compute water trapped
    - Water width = current_index - left_wall_index - 1
    - Water height = min(left_wall, right_wall) - bottom_height

    Time: O(n), Space: O(n)
    """
    stack = []  # Stack of indices, heights are decreasing
    water = 0

    for i, h in enumerate(height):
        while stack and height[stack[-1]] < h:
            bottom = stack.pop()

            if not stack:
                break  # No left wall, water flows out

            left_wall_idx = stack[-1]
            left_wall_height = height[left_wall_idx]
            right_wall_height = h
            bottom_height = height[bottom]

            width = i - left_wall_idx - 1
            bounded_height = min(left_wall_height, right_wall_height) - bottom_height
            water += width * bounded_height

        stack.append(i)

    return water
```

### 7.2 Valley Completion on Pop

Each pop operation finalizes a container segment:

```
Heights: [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]

When we reach height 2 at index 3:
  Stack before: [1, 2] (heights [1, 0])
  Pop index 2 (height 0): This is the valley bottom
    Left wall: index 1 (height 1)
    Right wall: index 3 (height 2)
    Width: 3 - 1 - 1 = 1
    Bounded height: min(1, 2) - 0 = 1
    Water: 1 × 1 = 1
```

### 7.3 Roles in Valley Resolution

- **Bottom**: The popped element (lowest point of the valley)
- **Left wall**: The element below the bottom in the stack
- **Right wall**: The current element that triggered the pop

---

## 8. Variation: Greedy Monotonic Stack

> **Problem**: Remove K digits to get the smallest number (LeetCode 402).
> **Key Insight**: Maintain a monotonically increasing stack as the "greedy best prefix".

### 8.1 Remove K Digits

```python
def remove_k_digits(num: str, k: int) -> str:
    """
    Remove k digits to create the smallest possible number.

    Algorithm:
    - Maintain monotonically increasing stack (greedy best prefix)
    - Pop larger digits when a smaller digit is seen (local optimality)
    - Handle leading zeros and remaining k

    Time: O(n), Space: O(n)
    """
    stack = []

    for digit in num:
        # Pop larger digits if we can still remove (k > 0)
        while k > 0 and stack and stack[-1] > digit:
            stack.pop()
            k -= 1
        stack.append(digit)

    # If k > 0, remove from the end (stack is increasing, end is largest)
    if k > 0:
        stack = stack[:-k]

    # Remove leading zeros and handle empty result
    result = ''.join(stack).lstrip('0')
    return result if result else '0'
```

### 8.2 Greedy Optimality

The pop decision is locally optimal:
- If we see digit `d` and stack top is `s > d`, removing `s` gives a smaller number
- The monotonic increasing property ensures the "best so far" prefix

### 8.3 Similar Problems

- **Remove Duplicate Letters (LeetCode 316)**: Monotonic stack with character counting
- **Create Maximum Number (LeetCode 321)**: Combine monotonic stacks from two arrays

---

## 9. Off-by-One, Comparison Semantics, and Robustness

### 9.1 Strict vs Non-Strict Monotonicity

| Comparison | Stack Order | When Elements Are Popped | Use Case |
|------------|-------------|--------------------------|----------|
| `<` (strict) | Decreasing | When strictly greater appears | Default NGE |
| `<=` (non-strict) | Decreasing | When greater or equal appears | Contribution with duplicates |
| `>` (strict) | Increasing | When strictly smaller appears | Default NSE |
| `>=` (non-strict) | Increasing | When smaller or equal appears | Histogram with duplicates |

### 9.2 Stable Boundary for Duplicates

When dealing with duplicates, use **asymmetric tie-breaking**:

```python
# Left boundary: strictly smaller (exclusive)
while stack and arr[stack[-1]] >= arr[i]:  # >=

# Right boundary: smaller or equal (inclusive)
while stack and arr[stack[-1]] > arr[i]:   # >
```

This creates a consistent "left-closed, right-open" convention.

### 9.3 Index vs Value Storage

**Always store indices**, not values:

```python
# Canonical: Store indices
stack.append(i)
value = arr[stack[-1]]
distance = i - stack[-1]

# Anti-pattern: Store values (loses position information)
stack.append(arr[i])  # Can't compute distances!
```

### 9.4 Sentinel Usage Patterns

| Sentinel | Purpose | Example |
|----------|---------|---------|
| `heights.append(0)` | Force flush at end | Histogram |
| `stack = [-1]` | Virtual left boundary | Handle empty stack |
| `temperatures.append(float('inf'))` | Force all elements to pop | Ensure completion |

### 9.5 Edge Case Checklist

- [ ] **Empty input**: Return appropriate default (0, [], etc.)
- [ ] **All equal elements**: Check comparison semantics
- [ ] **Single element**: Stack operations should handle gracefully
- [ ] **Strictly increasing/decreasing**: One of the boundaries may be all default
- [ ] **Overflow-safe arithmetic**: Use modular arithmetic for contribution counting
- [ ] **No-boundary cases**: Elements remaining in stack after processing

---

## 10. Termination Guarantees (Amortized Analysis)

### 10.1 Each Index Pushed Once, Popped Once

The key insight for O(n) complexity:

```
Total operations = pushes + pops
                 ≤ n + n = 2n = O(n)

Each index is:
- Pushed exactly once (when we reach it)
- Popped at most once (when a boundary is found)

Therefore, the entire algorithm is O(n) despite the inner while loop.
```

### 10.2 Invariant Preservation

After each iteration:
1. Stack contains indices of elements without their boundary yet
2. Stack is monotonically ordered (by value at those indices)
3. All processed boundaries have been recorded

### 10.3 Progress Guarantee

Each iteration either:
- Pops at least one element (progress on stack size), OR
- Pushes exactly one element and advances to next index

The while loop terminates because the stack shrinks with each pop, and there are only n elements total to pop.

---

## 11. Pattern Comparison Table

| Pattern | Stack Order | Comparison | Resolves | Typical Problems |
|---------|-------------|------------|----------|------------------|
| Next Greater (Right) | Decreasing | `<` | On pop | 496, 503, 739 |
| Previous Greater (Left) | Decreasing | `<` | On peek | 901 |
| Next Smaller (Right) | Increasing | `>` | On pop | 84 |
| Previous Smaller (Left) | Increasing | `>` | On peek | 84, 907 |
| Histogram Area | Increasing | `>=` | On pop | 84, 85 |
| Contribution Counting | Both | Asymmetric | Both | 907, 2104 |
| Trapped Water | Decreasing | `<` | On pop | 42 |
| Greedy Digit Removal | Increasing | `>` | On pop | 402, 316 |

---

## 12. When to Use Monotonic Stack

### 12.1 Problem Indicators

✅ **Use monotonic stack when:**
- Finding "next greater/smaller element" for each position
- Computing spans or distances to boundaries
- Calculating contributions based on interval widths
- Processing histograms or finding maximal rectangles
- Greedy digit/character selection with order constraints

❌ **Don't use monotonic stack when:**
- No boundary/comparison relationship between elements
- Need random access to boundaries (use precomputation)
- Problem requires bidirectional boundaries simultaneously (may need two passes)
- Simpler O(n) traversal suffices

### 12.2 Decision Flowchart

```
Is there a "nearest element satisfying a condition" query?
├── Yes → Is the condition based on comparison (>, <, >=, <=)?
│         ├── Yes → Monotonic Stack
│         │         ├── Finding boundaries → Base template
│         │         ├── Computing areas/spans → Histogram pattern
│         │         ├── Counting subarrays → Contribution pattern
│         │         ├── Trapping water/valleys → Container pattern
│         │         └── Greedy selection → Greedy monotonic stack
│         └── No → Other technique (hash map, etc.)
└── No → Monotonic stack probably doesn't apply
```

---

## 13. LeetCode Problem Mapping

### 13.1 Next Greater / Next Smaller Family

| Problem ID | Problem Name | Sub-Pattern |
|------------|--------------|-------------|
| 496 | Next Greater Element I | NGE with hash map |
| 503 | Next Greater Element II | Circular NGE |
| 739 | Daily Temperatures | NGE distance |
| 901 | Online Stock Span | Previous greater span |

### 13.2 Histogram / Rectangle Family

| Problem ID | Problem Name | Sub-Pattern |
|------------|--------------|-------------|
| 84 | Largest Rectangle in Histogram | Interval expansion |
| 85 | Maximal Rectangle | Matrix to histogram |

### 13.3 Contribution / Counting Family

| Problem ID | Problem Name | Sub-Pattern |
|------------|--------------|-------------|
| 907 | Sum of Subarray Minimums | Min contribution |
| 2104 | Sum of Subarray Ranges | Max - min contribution |

### 13.4 Container / Valley Family

| Problem ID | Problem Name | Sub-Pattern |
|------------|--------------|-------------|
| 42 | Trapping Rain Water | Valley resolution |

### 13.5 Greedy Monotonic Family

| Problem ID | Problem Name | Sub-Pattern |
|------------|--------------|-------------|
| 402 | Remove K Digits | Greedy increasing |
| 316 | Remove Duplicate Letters | Greedy with constraints |
| 321 | Create Maximum Number | Dual greedy |

---

## 14. Template Quick Reference

### 14.1 Next Greater Element (Right)

```python
def next_greater(arr):
    n, result, stack = len(arr), [-1] * len(arr), []
    for i in range(n):
        while stack and arr[stack[-1]] < arr[i]:
            result[stack.pop()] = arr[i]
        stack.append(i)
    return result
```

### 14.2 Previous Smaller Element (Left)

```python
def prev_smaller(arr):
    n, result, stack = len(arr), [-1] * len(arr), []
    for i in range(n):
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        result[i] = arr[stack[-1]] if stack else -1
        stack.append(i)
    return result
```

### 14.3 Largest Rectangle in Histogram

```python
def largest_rectangle(heights):
    heights, stack, max_area = heights + [0], [-1], 0
    for i, h in enumerate(heights):
        while stack[-1] != -1 and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            max_area = max(max_area, height * (i - stack[-1] - 1))
        stack.append(i)
    return max_area
```

### 14.4 Trapping Rain Water

```python
def trap(height):
    stack, water = [], 0
    for i, h in enumerate(height):
        while stack and height[stack[-1]] < h:
            bottom = stack.pop()
            if stack:
                w = i - stack[-1] - 1
                bounded = min(height[stack[-1]], h) - height[bottom]
                water += w * bounded
        stack.append(i)
    return water
```

### 14.5 Sum of Subarray Minimums

```python
def sum_subarray_mins(arr):
    n, MOD = len(arr), 10**9 + 7
    left, right, stack = [0]*n, [0]*n, []
    for i in range(n):
        while stack and arr[stack[-1]] >= arr[i]: stack.pop()
        left[i] = i - stack[-1] if stack else i + 1
        stack.append(i)
    stack = []
    for i in range(n-1, -1, -1):
        while stack and arr[stack[-1]] > arr[i]: stack.pop()
        right[i] = stack[-1] - i if stack else n - i
        stack.append(i)
    return sum(arr[i] * left[i] * right[i] for i in range(n)) % MOD
```

---

*Document generated for NeetCode Practice Framework — API Kernel: MonotonicStack*
