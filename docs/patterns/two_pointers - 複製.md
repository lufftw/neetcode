# Two Pointers Patterns: Complete Reference

> **API Kernel**: `TwoPointersTraversal`  
> **Core Mechanism**: Maintain two index pointers traversing a sequence under invariant-preserving rules.

This document presents the **canonical two pointers template** and all its major variations. Each implementation follows consistent naming conventions and includes detailed logic explanations.

---

## Core Concepts

### The Two Pointers Invariant

Every two pointers algorithm maintains an **invariant** — a relationship between the pointers and the problem state that must always be true.

```
Two Pointers State:
┌───────────────────────────────────────────────────────────────┐
│  [ ... left ─────── processed region ─────── right ... ]     │
│        └─────────── invariant holds ────────────┘            │
└───────────────────────────────────────────────────────────────┘
```

### Two Pointers Family Overview

| Sub-Pattern | Pointer Movement | Primary Use Case |
|-------------|-----------------|------------------|
| **Opposite Pointers** | `left→ ... ←right` | Sorted arrays, palindromes, container problems |
| **Same-Direction (Writer)** | `write→ ... read→` | In-place array modification, deduplication |
| **Fast–Slow Pointers** | `slow→ ... fast→→` | Cycle detection, finding midpoints |
| **Partitioning** | Multiple pointers | Dutch flag, sorting by property |
| **Dedup Enumeration** | Nested with skip | Multi-sum problems (3Sum, 4Sum) |
| **Merge Pattern** | `i→ j→ ... write→` | Merging sorted sequences |

### Universal Template Structure

```python
def two_pointers_template(sequence):
    """
    Generic two pointers template.
    
    Key components:
    1. Initialization: Set up pointer positions based on strategy
    2. Invariant: Condition that guides pointer movement
    3. Movement Rules: Deterministic pointer advancement
    4. Termination: Pointers meet or cross
    5. Update: Record answer when condition is satisfied
    """
    left, right = initialize_pointers(sequence)
    answer = initial_answer()
    
    while not termination_condition(left, right):
        # EVALUATE: Check current state against problem goal
        current_value = evaluate(sequence, left, right)
        
        # UPDATE ANSWER: Record if current state is optimal
        answer = update_answer(answer, current_value)
        
        # MOVE: Advance pointers based on invariant
        if should_move_left(current_value, target):
            left += 1
        else:
            right -= 1
    
    return answer
```

---

## Table of Contents

1. [Core Concepts](#core-concepts)
2. [Opposite Pointers (Two-End)](#opposite-pointers-two-end)
3. [Same-Direction Pointers (Writer Pattern)](#same-direction-pointers-writer-pattern)
4. [Fast–Slow Pointers (Cycle Detection)](#fastslow-pointers-cycle-detection)
5. [Partitioning / Dutch National Flag](#partitioning--dutch-national-flag)
6. [Dedup + Sorted Two-Pointer Enumeration](#dedup--sorted-two-pointer-enumeration)
7. [Merge Pattern](#merge-pattern)
8. [Pattern Comparison Table](#pattern-comparison-table)
9. [When to Use Two Pointers](#when-to-use-two-pointers)
10. [LeetCode Problem Mapping](#leetcode-problem-mapping)

---

## Opposite Pointers (Two-End)

> **Strategy**: Start pointers at opposite ends, move toward center.  
> **Invariant**: Valid solution space lies between `left` and `right`.  
> **Termination**: `left >= right` (pointers meet or cross).

### When to Use

- Array is **sorted** and you need pairs with a target sum/property
- Problem involves **symmetric** checks (palindromes)
- Need to **maximize/minimize** a function of two positions (container area)

### Why It Works

With sorted arrays, moving `left` right **increases** the left value, moving `right` left **decreases** the right value. This monotonicity enables efficient search without examining all O(n²) pairs.

### Template

```python
def opposite_pointers_template(arr, target):
    """
    Opposite pointers for sorted array search.
    
    Time Complexity: O(n) - each pointer moves at most n times
    Space Complexity: O(1) - constant extra space
    """
    left, right = 0, len(arr) - 1
    answer = None
    
    while left < right:
        current = compute_value(arr, left, right)
        
        if current == target:
            # Found exact match
            return process_match(arr, left, right)
        elif current < target:
            # Need larger value: move left pointer right
            left += 1
        else:
            # Need smaller value: move right pointer left
            right -= 1
    
    return answer
```

### Complexity Notes

| Aspect | Analysis |
|--------|----------|
| Time | O(n) — each element visited at most once per pointer |
| Space | O(1) — only pointer indices stored |
| Prerequisite | Array must be sorted (or problem has monotonic property) |

### LeetCode Problems

| ID | Problem | Key Insight |
|----|---------|-------------|
| 11 | Container With Most Water | Maximize `min(height[l], height[r]) × (r - l)` |
| 15 | 3Sum | Outer loop + inner opposite pointers |
| 16 | 3Sum Closest | Track closest sum instead of exact match |
| 125 | Valid Palindrome | Compare characters moving inward |
| 167 | Two Sum II | Classic sorted array two-sum |
| 680 | Valid Palindrome II | Allow one character skip |

---

## Same-Direction Pointers (Writer Pattern)

> **Strategy**: Both pointers move in the same direction; one "reads", one "writes".  
> **Invariant**: `arr[0:write]` contains the valid/processed elements.  
> **Termination**: Read pointer reaches end of array.

### When to Use

- **In-place** array modification required
- Need to **remove** elements matching a condition
- Need to **deduplicate** while preserving order
- Memory constraints prohibit extra storage

### Why It Works

The write pointer marks the boundary of "good" elements. The read pointer scans ahead, and only elements satisfying the condition are copied to the write position. Elements at `arr[write:]` are implicitly discarded.

### Template

```python
def same_direction_template(arr, condition):
    """
    Same-direction (reader/writer) pattern for in-place modification.
    
    Time Complexity: O(n) - single pass through array
    Space Complexity: O(1) - in-place modification
    
    Invariant: arr[0:write_index] contains all valid elements seen so far.
    """
    write_index = 0
    
    for read_index in range(len(arr)):
        if condition(arr, read_index, write_index):
            arr[write_index] = arr[read_index]
            write_index += 1
    
    return write_index  # New logical length
```

### Complexity Notes

| Aspect | Analysis |
|--------|----------|
| Time | O(n) — single pass, each element examined once |
| Space | O(1) — in-place modification, no auxiliary storage |
| Property | Stable — preserves relative order of retained elements |

### LeetCode Problems

| ID | Problem | Condition |
|----|---------|-----------|
| 26 | Remove Duplicates from Sorted Array | `arr[read] != arr[write - 1]` |
| 27 | Remove Element | `arr[read] != val` |
| 80 | Remove Duplicates II | `arr[read] != arr[write - 2]` |
| 283 | Move Zeroes | `arr[read] != 0`, then fill zeros |

---

## Fast–Slow Pointers (Cycle Detection)

> **Strategy**: Two pointers at different speeds; fast moves 2×, slow moves 1×.  
> **Invariant**: If cycle exists, fast will eventually catch slow inside the cycle.  
> **Termination**: Fast reaches null (no cycle) or fast meets slow (cycle exists).

### When to Use

- **Cycle detection** in linked lists or sequences
- Finding the **start of a cycle** (Floyd's algorithm phase 2)
- Finding **middle element** of a linked list
- **Happy number** and similar sequence convergence problems

### Why It Works (Floyd's Cycle Detection)

If a cycle exists with length `C`:
- When slow enters the cycle, fast is already inside
- The gap between them decreases by 1 each step (fast gains 1 on slow)
- They must meet within `C` steps after slow enters

To find cycle start:
- When they meet, reset one pointer to head
- Move both at speed 1 — they meet at cycle start
- Math: Meeting point is `λ` steps from cycle start; head is also `λ` steps from start

### Template

```python
def fast_slow_cycle_detection(head):
    """
    Floyd's cycle detection algorithm.
    
    Phase 1: Detect if cycle exists
    Phase 2: Find cycle start (if needed)
    
    Time Complexity: O(n) - at most 2n steps
    Space Complexity: O(1) - only two pointers
    """
    # Phase 1: Detect cycle
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:
            # Cycle detected
            break
    else:
        # No cycle (fast reached end)
        return None
    
    # Phase 2: Find cycle start
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    
    return slow  # Cycle start node
```

### Finding Middle Element

```python
def find_middle(head):
    """
    Find middle element using fast-slow pointers.
    
    When fast reaches end, slow is at middle.
    For even length, returns second middle element.
    """
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    return slow
```

### Complexity Notes

| Aspect | Analysis |
|--------|----------|
| Time | O(n) — fast pointer traverses at most 2n nodes |
| Space | O(1) — only two pointer references |
| Application | Works on any sequence with a "next" function |

### LeetCode Problems

| ID | Problem | Variation |
|----|---------|-----------|
| 141 | Linked List Cycle | Phase 1 only (detect) |
| 142 | Linked List Cycle II | Phase 1 + Phase 2 (find start) |
| 202 | Happy Number | Implicit linked list cycle |
| 287 | Find the Duplicate Number | Cycle detection on value sequence |
| 876 | Middle of the Linked List | Fast reaches end → slow at middle |

---

## Partitioning / Dutch National Flag

> **Strategy**: Multiple pointers divide array into regions by property.  
> **Invariant**: Each region contains elements satisfying a specific condition.  
> **Termination**: Unclassified region is exhausted.

### When to Use

- **Sort by categories** (e.g., 0s/1s/2s, even/odd)
- **Partition** array around a pivot (quicksort)
- **Rearrange** elements by property in-place

### Why It Works

The Dutch National Flag algorithm maintains three regions:
- `[0, low)`: Elements < pivot (e.g., all 0s)
- `[low, mid)`: Elements = pivot (e.g., all 1s)  
- `[high+1, n)`: Elements > pivot (e.g., all 2s)
- `[mid, high]`: Unclassified elements

Each element is examined once and placed in its final region.

### Template (Three-Way Partition)

```python
def dutch_national_flag(arr, pivot=1):
    """
    Dutch National Flag algorithm (three-way partition).
    
    Partitions array into three regions:
    - Elements < pivot
    - Elements == pivot
    - Elements > pivot
    
    Time Complexity: O(n) - single pass
    Space Complexity: O(1) - in-place swaps
    
    Invariant at each step:
    - arr[0:low] contains elements < pivot
    - arr[low:mid] contains elements == pivot
    - arr[high+1:] contains elements > pivot
    - arr[mid:high+1] is unclassified
    """
    low, mid, high = 0, 0, len(arr) - 1
    
    while mid <= high:
        if arr[mid] < pivot:
            # Move to "less than" region
            arr[low], arr[mid] = arr[mid], arr[low]
            low += 1
            mid += 1
        elif arr[mid] > pivot:
            # Move to "greater than" region
            arr[mid], arr[high] = arr[high], arr[mid]
            high -= 1
            # Don't increment mid — swapped element is unclassified
        else:
            # Element equals pivot — already in correct region
            mid += 1
```

### Two-Way Partition (Even/Odd)

```python
def partition_by_parity(arr):
    """
    Partition array so all even numbers come before odd numbers.
    
    Two regions: [0, write) = even, [write, n) = odd
    """
    write = 0
    
    for read in range(len(arr)):
        if arr[read] % 2 == 0:
            arr[write], arr[read] = arr[read], arr[write]
            write += 1
    
    return arr
```

### Complexity Notes

| Aspect | Analysis |
|--------|----------|
| Time | O(n) — each element moved at most twice |
| Space | O(1) — in-place swaps only |
| Stability | Not stable — relative order may change |

### LeetCode Problems

| ID | Problem | Partition Type |
|----|---------|----------------|
| 75 | Sort Colors | Three-way (0, 1, 2) |
| 215 | Kth Largest Element | Quickselect partition |
| 905 | Sort Array By Parity | Two-way (even/odd) |
| 922 | Sort Array By Parity II | Alternating positions |

---

## Dedup + Sorted Two-Pointer Enumeration

> **Strategy**: Nested loops with two-pointer inner search + duplicate skipping.  
> **Invariant**: Each unique combination is processed exactly once.  
> **Use Case**: Multi-sum problems (3Sum, 4Sum, kSum).

### When to Use

- Finding **all unique tuples** summing to target
- Problem requires **no duplicate results**
- Input is sorted or can be sorted

### Why It Works

By sorting first, we can:
1. Use opposite pointers to find pairs efficiently
2. Skip duplicates by checking `if nums[i] == nums[i-1]: continue`
3. Avoid revisiting the same combination

### Template (3Sum)

```python
def three_sum_template(nums, target=0):
    """
    Find all unique triplets that sum to target.
    
    Algorithm:
    1. Sort array
    2. For each element nums[i], find pairs (j, k) where j > i, k > j
    3. Use opposite pointers for inner search
    4. Skip duplicates at all levels
    
    Time Complexity: O(n²) - n iterations × n two-pointer search
    Space Complexity: O(1) extra (excluding output)
    """
    nums.sort()
    n = len(nums)
    result = []
    
    for i in range(n - 2):
        # Skip duplicates for first element
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        # Early termination: smallest possible sum too large
        if nums[i] + nums[i + 1] + nums[i + 2] > target:
            break
        
        # Skip: largest possible sum too small
        if nums[i] + nums[n - 2] + nums[n - 1] < target:
            continue
        
        # Two-pointer search for remaining pair
        left, right = i + 1, n - 1
        
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]
            
            if current_sum == target:
                result.append([nums[i], nums[left], nums[right]])
                
                # Skip duplicates for second element
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                # Skip duplicates for third element
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif current_sum < target:
                left += 1
            else:
                right -= 1
    
    return result
```

### Complexity Notes

| Aspect | Analysis |
|--------|----------|
| Time | O(n^(k-1)) for k-Sum — O(n²) for 3Sum, O(n³) for 4Sum |
| Space | O(1) extra space (excluding sorting and output) |
| Key Insight | Sorting enables both two-pointer search and deduplication |

### LeetCode Problems

| ID | Problem | Variant |
|----|---------|---------|
| 15 | 3Sum | Target = 0 |
| 16 | 3Sum Closest | Minimize `|sum - target|` |
| 18 | 4Sum | Four elements, same approach |
| 167 | Two Sum II | Base case (2Sum sorted) |

---

## Merge Pattern

> **Strategy**: Two pointers on separate sorted sequences, merge into one.  
> **Invariant**: Output contains smallest unprocessed element at each step.  
> **Use Case**: Merging sorted arrays/lists.

### When to Use

- **Merging two sorted arrays** into one sorted result
- **Merge step** of merge sort
- Combining sorted linked lists

### Why It Works

Both input sequences are sorted. At each step, the smallest remaining element is at one of the two pointer positions. Comparing and advancing the smaller one builds the merged result in sorted order.

### Template

```python
def merge_sorted_arrays(arr1, arr2):
    """
    Merge two sorted arrays into one sorted array.
    
    Time Complexity: O(m + n) - each element processed once
    Space Complexity: O(m + n) - output array
    """
    i, j = 0, 0
    result = []
    
    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1
    
    # Append remaining elements
    result.extend(arr1[i:])
    result.extend(arr2[j:])
    
    return result
```

### In-Place Merge (LeetCode 88)

```python
def merge_in_place(nums1, m, nums2, n):
    """
    Merge nums2 into nums1 in-place.
    
    Key insight: Write from the END to avoid overwriting unprocessed elements.
    """
    write = m + n - 1
    i, j = m - 1, n - 1
    
    while j >= 0:
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[write] = nums1[i]
            i -= 1
        else:
            nums1[write] = nums2[j]
            j -= 1
        write -= 1
```

### Complexity Notes

| Aspect | Analysis |
|--------|----------|
| Time | O(m + n) — each element compared at most once |
| Space | O(1) for in-place, O(m + n) for new array |
| Stability | Stable if ties favor left array |

### LeetCode Problems

| ID | Problem | Variant |
|----|---------|---------|
| 21 | Merge Two Sorted Lists | Linked list version |
| 88 | Merge Sorted Array | In-place, write from end |
| 977 | Squares of a Sorted Array | Square then merge from ends |

---

## Pattern Comparison Table

| Pattern | Pointer Init | Movement | Termination | Time |
|---------|--------------|----------|-------------|------|
| Opposite | `0, n-1` | Toward center | `left >= right` | O(n) |
| Same-Direction | `0, 0` | Both forward | `read >= n` | O(n) |
| Fast–Slow | `head, head` | Slow 1×, Fast 2× | Meet or null | O(n) |
| Partitioning | `0, 0, n-1` | By element value | `mid > high` | O(n) |
| Dedup Enum | `i, i+1, n-1` | Nested + opposite | All `i` processed | O(n²) |
| Merge | `0, 0` | Advance smaller | Both exhausted | O(m+n) |

---

## When to Use Two Pointers

### Problem Indicators

✅ **Use two pointers when:**
- Working with **sorted** arrays/lists
- Need to find **pairs or tuples** with a target property
- **In-place** modification is required
- Need to detect **cycles** in sequences
- **Merging** sorted sequences

❌ **Don't use two pointers when:**
- Array is unsorted and sorting is not allowed
- Need all pairs regardless of order (use hash map)
- Problem requires **non-contiguous** elements
- Relationship between elements is not monotonic

### Decision Flowchart

```
Is the array sorted (or can be sorted)?
├── No → Is it a linked list cycle problem?
│        ├── Yes → Fast–Slow Pointers
│        └── No → Consider hash map or other approach
└── Yes → What's the goal?
          ├── Find pair with target sum → Opposite Pointers
          ├── Remove/deduplicate in-place → Same-Direction
          ├── Partition by property → Dutch Flag
          ├── Find all unique tuples → Dedup Enumeration
          └── Merge two sequences → Merge Pattern
```

---

## LeetCode Problem Mapping

### Opposite Pointers (Two-End)

| ID | Problem Name | Difficulty |
|----|--------------|------------|
| 11 | Container With Most Water | Medium |
| 15 | 3Sum | Medium |
| 16 | 3Sum Closest | Medium |
| 42 | Trapping Rain Water | Hard |
| 125 | Valid Palindrome | Easy |
| 167 | Two Sum II - Input Array Is Sorted | Medium |
| 680 | Valid Palindrome II | Easy |

### Same-Direction Pointers (Writer)

| ID | Problem Name | Difficulty |
|----|--------------|------------|
| 26 | Remove Duplicates from Sorted Array | Easy |
| 27 | Remove Element | Easy |
| 80 | Remove Duplicates from Sorted Array II | Medium |
| 283 | Move Zeroes | Easy |

### Fast–Slow Pointers

| ID | Problem Name | Difficulty |
|----|--------------|------------|
| 141 | Linked List Cycle | Easy |
| 142 | Linked List Cycle II | Medium |
| 202 | Happy Number | Easy |
| 287 | Find the Duplicate Number | Medium |
| 876 | Middle of the Linked List | Easy |

### Partitioning / Dutch Flag

| ID | Problem Name | Difficulty |
|----|--------------|------------|
| 75 | Sort Colors | Medium |
| 215 | Kth Largest Element in an Array | Medium |
| 905 | Sort Array By Parity | Easy |
| 922 | Sort Array By Parity II | Easy |

### Merge Pattern

| ID | Problem Name | Difficulty |
|----|--------------|------------|
| 21 | Merge Two Sorted Lists | Easy |
| 88 | Merge Sorted Array | Easy |
| 977 | Squares of a Sorted Array | Easy |

---

## Template Quick Reference

### Opposite Pointers

```python
def opposite_pointers(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        # Process arr[left] and arr[right]
        if condition_move_left:
            left += 1
        else:
            right -= 1
```

### Same-Direction (Writer)

```python
def same_direction(arr):
    write = 0
    for read in range(len(arr)):
        if should_keep(arr[read]):
            arr[write] = arr[read]
            write += 1
    return write
```

### Fast–Slow

```python
def fast_slow(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True  # Cycle
    return False
```

### Dutch Flag

```python
def dutch_flag(arr):
    low, mid, high = 0, 0, len(arr) - 1
    while mid <= high:
        if arr[mid] < pivot:
            arr[low], arr[mid] = arr[mid], arr[low]
            low += 1
            mid += 1
        elif arr[mid] > pivot:
            arr[mid], arr[high] = arr[high], arr[mid]
            high -= 1
        else:
            mid += 1
```

### Merge

```python
def merge(arr1, arr2):
    i, j, result = 0, 0, []
    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1
    return result + arr1[i:] + arr2[j:]
```

---

*Document generated for NeetCode Practice Framework — API Kernel: TwoPointersTraversal*

