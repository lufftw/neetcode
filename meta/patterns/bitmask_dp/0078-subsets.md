# 78. Subsets

## Problem Link
https://leetcode.com/problems/subsets/

## Difficulty
Medium

## Tags
- Bitmask
- Subset Enumeration
- Bit Manipulation

## Pattern
Bitmask DP - Subset Enumeration

## API Kernel
`BitmaskDP`

## Problem Summary
Given an integer array `nums` of unique elements, return all possible subsets (the power set).

## Key Insight

Each subset corresponds to a unique bitmask from 0 to 2^n - 1:
- Bit i is set → include nums[i]
- Bit i is clear → exclude nums[i]

This gives O(2^n) subsets directly without recursion.

## Template Mapping

```python
def subsets(nums):
    n = len(nums)
    result = []

    # Enumerate all 2^n bitmasks
    for mask in range(1 << n):
        # Build subset from mask
        subset = []
        for i in range(n):
            if mask & (1 << i):  # Check if bit i is set
                subset.append(nums[i])
        result.append(subset)

    return result
```

## Complexity
- Time: O(n × 2^n) - iterate through all masks, each taking O(n) to decode
- Space: O(n × 2^n) - storing all subsets

## Why This Problem First?

1. **Pure bitmask enumeration** - No DP, just understanding bitmask-to-subset mapping
2. **Foundation for all bitmask DP** - The enumeration loop `for mask in range(1 << n)` is universal
3. **Bit operation practice** - Check bit with `mask & (1 << i)`

## Common Mistakes

1. **Off-by-one in range** - Should be `range(1 << n)`, not `range((1 << n) - 1)`
2. **Wrong bit check** - Use `mask & (1 << i)`, not `mask & i`
3. **Modifying mask during iteration** - Decode mask, don't modify it

## Related Problems
- LC 90: Subsets II (with duplicates)
- LC 784: Letter Case Permutation
- LC 1286: Iterator for Combination
