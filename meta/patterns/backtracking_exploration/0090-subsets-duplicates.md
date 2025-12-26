## Variation: Subsets with Duplicates (LeetCode 90)

> **Problem**: Given an array with duplicates, return all unique subsets.  
> **Delta from Subsets**: Sort + same-level deduplication.  
> **Key Insight**: Skip duplicate values at the same recursion level.

### Implementation

```python
def subsets_with_dup(nums: list[int]) -> list[list[int]]:
    """
    Generate all unique subsets from integers that may contain duplicates.
    
    Algorithm:
    - Sort to bring duplicates together
    - Use same-level deduplication: skip if current equals previous
      in the same iteration loop
    
    Deduplication Condition:
    - Skip nums[i] if i > start_index AND nums[i] == nums[i-1]
    - This prevents choosing the same value twice at the same tree level
    
    Time Complexity: O(n × 2^n) worst case
    Space Complexity: O(n)
    
    Args:
        nums: Array of integers (may contain duplicates)
        
    Returns:
        All unique subsets
    """
    results: list[list[int]] = []
    n = len(nums)
    
    # CRITICAL: Sort to bring duplicates together
    nums.sort()
    
    path: list[int] = []
    
    def backtrack(start_index: int) -> None:
        results.append(path[:])
        
        for i in range(start_index, n):
            # DEDUPLICATION: Skip duplicates at same level
            # i > start_index ensures we're not skipping the first occurrence
            if i > start_index and nums[i] == nums[i - 1]:
                continue
            
            path.append(nums[i])
            backtrack(i + 1)
            path.pop()
    
    backtrack(0)
    return results
```

### Deduplication Visualization

```
Input: [1, 2, 2] (sorted)

Without deduplication:
[]
├─ [1] → [1,2] → [1,2,2]
│      → [1,2]  ← choosing second 2
├─ [2] → [2,2]
└─ [2]  ← DUPLICATE of above!

With deduplication (skip if i > start and nums[i] == nums[i-1]):
[]
├─ [1] → [1,2] → [1,2,2]
│                        ↑ i=2, start=2, 2==2 but i==start, proceed
│      → [1,2]  skipped (i=2 > start=1, 2==2)
├─ [2] → [2,2]
└─ skip (i=2 > start=0, 2==2)

Result: [[], [1], [1,2], [1,2,2], [2], [2,2]]
```

