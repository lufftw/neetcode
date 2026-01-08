# 88. Merge Sorted Array

## Problem Link
https://leetcode.com/problems/merge-sorted-array/

## Difficulty
Easy

## Tags
- Array
- Two Pointers
- Sorting

## Pattern
KWayMerge - In-Place Backward Merge

## API Kernel
`MergeSortedSequences`

## Problem Summary

Merge nums2 into nums1 in-place. nums1 has enough space (length m + n) to hold additional elements.

## Key Insight

**Merge from the end** to avoid overwriting elements we haven't processed yet. Start filling from position m+n-1, comparing largest elements first.

```
nums1 = [1,2,3,_,_,_], m = 3
nums2 = [2,5,6], n = 3

Merge from end:
pos 5: 6 > 3 → nums1[5] = 6
pos 4: 5 > 3 → nums1[4] = 5
pos 3: 3 > 2 → nums1[3] = 3
pos 2: 2 >= 2 → nums1[2] = 2 (from nums2)
pos 1: 2 > (empty) → nums1[1] = 2 (from nums1)
...

Result: [1,2,2,3,5,6]
```

## Template Mapping

```python
from typing import List

class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Modify nums1 in-place to contain merged result.

        Key insight: Fill from the end to avoid overwriting.
        """
        # Pointers to last elements of each array
        p1 = m - 1      # Last element in nums1's original data
        p2 = n - 1      # Last element in nums2
        write = m + n - 1  # Write position (end of nums1)

        # Merge from end: place larger element at write position
        while p1 >= 0 and p2 >= 0:
            if nums1[p1] > nums2[p2]:
                nums1[write] = nums1[p1]
                p1 -= 1
            else:
                nums1[write] = nums2[p2]
                p2 -= 1
            write -= 1

        # If nums2 has remaining elements, copy them
        # (If nums1 has remaining, they're already in place)
        while p2 >= 0:
            nums1[write] = nums2[p2]
            p2 -= 1
            write -= 1
```

## Complexity
- Time: O(m + n)
- Space: O(1) - in-place

## Why This Problem Third?

Merge Sorted Array teaches the **backward merge technique**:

1. **In-place constraint**: Can't use extra space for output
2. **Backward fill insight**: Prevents overwriting unprocessed elements
3. **One remaining copy**: Only nums2 leftovers need copying
4. **Array variant**: Same pattern as linked list, different data structure

## Delta from Linked List Merge

| Aspect | Linked List | Array |
|--------|-------------|-------|
| Direction | Forward | Backward (in-place) |
| New space | Reuse nodes | Already allocated |
| Leftover handling | Attach remaining | Copy remaining |

## Common Mistakes

1. **Merging forward** - Overwrites elements before processing
2. **Forgetting nums2 leftovers** - Must copy remaining nums2 elements
3. **Wrong pointer initialization** - p1 = m-1, p2 = n-1, write = m+n-1
4. **Off-by-one errors** - Use `>= 0` not `> 0` in while conditions

## Related Problems
- LC 21: Merge Two Sorted Lists (linked list version)
- LC 23: Merge K Sorted Lists (generalization)
- LC 977: Squares of a Sorted Array (merge sorted subarrays)


