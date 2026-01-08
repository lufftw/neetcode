# 21. Merge Two Sorted Lists

## Problem Link
https://leetcode.com/problems/merge-two-sorted-lists/

## Difficulty
Easy

## Tags
- Linked List
- Recursion

## Pattern
KWayMerge - Two Pointer (K=2)

## API Kernel
`MergeSortedSequences`

## Problem Summary

Merge two sorted linked lists and return the merged list as a sorted list.

## Key Insight

This is the **K=2 special case** of K-way merge. When K=2, we don't need a heap - simple two-pointer comparison suffices. This is also the building block for divide-and-conquer K-way merge.

```
list1: 1 → 2 → 4
list2: 1 → 3 → 4

Step by step:
1 <= 1: pick list1[0] → [1]
1 <= 2: pick list2[0] → [1,1]
2 <= 3: pick list1[1] → [1,1,2]
3 <= 4: pick list2[1] → [1,1,2,3]
4 <= 4: pick list1[2] → [1,1,2,3,4]
append remaining list2[2] → [1,1,2,3,4,4]
```

## Template Mapping

```python
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        # Dummy node simplifies edge cases
        dummy = ListNode()
        tail = dummy

        # Two-pointer merge: compare heads, advance smaller
        while list1 and list2:
            if list1.val <= list2.val:
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next

        # Attach remaining (at most one list has elements)
        tail.next = list1 if list1 else list2

        return dummy.next
```

## Alternative: Recursive

```python
class SolutionRecursive:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        if not list1:
            return list2
        if not list2:
            return list1

        if list1.val <= list2.val:
            list1.next = self.mergeTwoLists(list1.next, list2)
            return list1
        else:
            list2.next = self.mergeTwoLists(list1, list2.next)
            return list2
```

## Complexity
- Iterative: O(n + m) time, O(1) space
- Recursive: O(n + m) time, O(n + m) stack space

## Why This Problem Second?

Merge Two Sorted Lists establishes the **two-pointer merge foundation**:

1. **Simplest merge case**: Only two sequences to compare
2. **No heap overhead**: Direct comparison is optimal for K=2
3. **Building block**: Used in divide-and-conquer K-way merge
4. **Dummy node pattern**: Avoids special-casing the head

## Common Mistakes

1. **Special-casing the first node** - Use dummy node instead
2. **Forgetting to attach remaining elements** - After loop, one list may have elements
3. **Returning wrong node** - Return `dummy.next`, not `dummy`

## Related Problems
- LC 23: Merge K Sorted Lists (generalization)
- LC 88: Merge Sorted Array (array version)
- LC 148: Sort List (uses merge as subroutine)


