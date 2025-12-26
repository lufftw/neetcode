## Variation: Combination Sum II (LeetCode 40)

> **Problem**: Find combinations that sum to target. Each element used at most once. Input may have duplicates.  
> **Delta from Combination Sum**: No reuse + duplicate handling.  
> **Key Insight**: Sort + same-level skip for duplicates.

### Implementation

```python
def combination_sum2(candidates: list[int], target: int) -> list[list[int]]:
    """
    Find all unique combinations that sum to target. Each number used at most once.
    Input may contain duplicates.
    
    Algorithm:
    - Sort to bring duplicates together
    - Use start_index to prevent reuse (i+1 when recursing)
    - Same-level deduplication: skip if current == previous at same level
    
    Deduplication Rule:
    - Skip candidates[i] if i > start_index AND candidates[i] == candidates[i-1]
    - This prevents generating duplicate combinations
    
    Time Complexity: O(2^n) worst case
    Space Complexity: O(n)
    
    Args:
        candidates: Array of positive integers (may have duplicates)
        target: Target sum
        
    Returns:
        All unique combinations summing to target
    """
    results: list[list[int]] = []
    path: list[int] = []
    
    # CRITICAL: Sort for deduplication
    candidates.sort()
    
    def backtrack(start_index: int, remaining: int) -> None:
        if remaining == 0:
            results.append(path[:])
            return
        
        if remaining < 0:
            return
        
        for i in range(start_index, len(candidates)):
            # DEDUPLICATION: Skip same value at same level
            if i > start_index and candidates[i] == candidates[i - 1]:
                continue
            
            # PRUNING: Current exceeds remaining (sorted, so break)
            if candidates[i] > remaining:
                break
            
            path.append(candidates[i])
            
            # NO REUSE: Recurse with i+1
            backtrack(i + 1, remaining - candidates[i])
            
            path.pop()
    
    backtrack(0, target)
    return results
```

