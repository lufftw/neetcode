## Variation: Permutations with Duplicates (LeetCode 47)

> **Problem**: Given an array with duplicate integers, return all unique permutations.  
> **Delta from Base**: Add same-level deduplication after sorting.  
> **Key Insight**: Skip duplicate elements at the same tree level.

### Implementation

```python
def permute_unique(nums: list[int]) -> list[list[int]]:
    """
    Generate all unique permutations of integers that may contain duplicates.
    
    Algorithm:
    - Sort the array to bring duplicates together
    - Use same-level deduplication: skip a duplicate if its previous
      occurrence wasn't used (meaning we're at the same decision level)
    
    Deduplication Rule:
    - If nums[i] == nums[i-1] and used[i-1] == False, skip nums[i]
    - This ensures we only use the first occurrence of a duplicate
      at each level of the decision tree
    
    Time Complexity: O(n! × n) in worst case (all unique)
    Space Complexity: O(n)
    
    Args:
        nums: Array of integers (may contain duplicates)
        
    Returns:
        All unique permutations
    """
    results: list[list[int]] = []
    n = len(nums)
    
    # CRITICAL: Sort to bring duplicates together
    nums.sort()
    
    path: list[int] = []
    used: list[bool] = [False] * n
    
    def backtrack() -> None:
        if len(path) == n:
            results.append(path[:])
            return
        
        for i in range(n):
            if used[i]:
                continue
            
            # DEDUPLICATION: Skip duplicates at the same tree level
            # Condition: Current equals previous AND previous is unused
            # (unused previous means we're trying duplicate at same level)
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue
            
            path.append(nums[i])
            used[i] = True
            
            backtrack()
            
            path.pop()
            used[i] = False
    
    backtrack()
    return results
```

### Deduplication Logic Explained

```
Input: [1, 1, 2] (sorted)
Indices: [0, 1, 2]

Without deduplication, we'd get:
- Path using indices [0,1,2] → [1,1,2]
- Path using indices [1,0,2] → [1,1,2]  ← DUPLICATE!

With deduplication (skip if nums[i]==nums[i-1] and !used[i-1]):
- When i=1 and used[0]=False: skip (same level, use i=0 first)
- When i=1 and used[0]=True: proceed (different subtree)

This ensures we always pick the leftmost duplicate first at each level.
```

