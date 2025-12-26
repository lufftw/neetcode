## Variation: Combination Sum (LeetCode 39)

> **Problem**: Find combinations that sum to target. Elements can be reused.  
> **Sub-Pattern**: Target search with element reuse.  
> **Key Insight**: Don't increment start_index when allowing reuse.

### Implementation

```python
def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    """
    Find all combinations that sum to target. Each number can be used unlimited times.
    
    Algorithm:
    - Track remaining target (target - current sum)
    - When remaining = 0, found a valid combination
    - Allow reuse by NOT incrementing start_index when recursing
    - Prune when remaining < 0 (overshot target)
    
    Key Difference from Combinations:
    - Reuse allowed: recurse with same index i, not i+1
    - This means we can pick the same element multiple times
    
    Time Complexity: O(n^(t/m)) where t=target, m=min(candidates)
        - Branching factor up to n at each level
        - Depth up to t/m (using smallest element repeatedly)
    
    Space Complexity: O(t/m) for recursion depth
    
    Args:
        candidates: Array of distinct positive integers
        target: Target sum
        
    Returns:
        All unique combinations that sum to target
    """
    results: list[list[int]] = []
    path: list[int] = []
    
    # Optional: Sort for consistent output order
    candidates.sort()
    
    def backtrack(start_index: int, remaining: int) -> None:
        # BASE CASE: Found valid combination
        if remaining == 0:
            results.append(path[:])
            return
        
        # PRUNING: Overshot target
        if remaining < 0:
            return
        
        for i in range(start_index, len(candidates)):
            # PRUNING: If current candidate exceeds remaining, 
            # all subsequent (if sorted) will too
            if candidates[i] > remaining:
                break
            
            path.append(candidates[i])
            
            # REUSE ALLOWED: Recurse with same index i
            backtrack(i, remaining - candidates[i])
            
            path.pop()
    
    backtrack(0, target)
    return results
```

### Reuse vs No-Reuse Comparison

| Aspect | With Reuse (LC 39) | Without Reuse (LC 40) |
|--------|-------------------|----------------------|
| Recurse with | `backtrack(i, ...)` | `backtrack(i+1, ...)` |
| Same element | Can appear multiple times | Can appear at most once |
| Deduplication | Not needed (distinct) | Needed (may have duplicates) |

