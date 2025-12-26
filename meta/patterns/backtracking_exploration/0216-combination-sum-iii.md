## Variation: Combination Sum III (LeetCode 216)

> **Problem**: Find k numbers from [1-9] that sum to n. Each number used at most once.  
> **Delta from Combination Sum II**: Fixed count k + bounded range [1-9].  
> **Key Insight**: Dual constraint — both count and sum must be satisfied.

### Implementation

```python
def combination_sum3(k: int, n: int) -> list[list[int]]:
    """
    Find all combinations of k numbers from [1-9] that sum to n.
    
    Algorithm:
    - Fixed size k (must have exactly k numbers)
    - Fixed sum n (must sum to exactly n)
    - Range is [1-9], all distinct, no reuse
    
    Pruning Strategies:
    1. If current sum exceeds n, stop
    2. If path length exceeds k, stop
    3. If remaining numbers can't fill to k, stop
    
    Time Complexity: O(C(9,k) × k)
    Space Complexity: O(k)
    
    Args:
        k: Number of elements required
        n: Target sum
        
    Returns:
        All valid combinations
    """
    results: list[list[int]] = []
    path: list[int] = []
    
    def backtrack(start: int, remaining: int) -> None:
        # BASE CASE: Have k numbers
        if len(path) == k:
            if remaining == 0:
                results.append(path[:])
            return
        
        # PRUNING: Not enough numbers left to fill path
        if 9 - start + 1 < k - len(path):
            return
        
        for i in range(start, 10):
            # PRUNING: Current number too large
            if i > remaining:
                break
            
            path.append(i)
            backtrack(i + 1, remaining - i)
            path.pop()
    
    backtrack(1, n)
    return results
```

