## Variation: Combinations (LeetCode 77)

> **Problem**: Given n and k, return all combinations of k numbers from [1..n].  
> **Sub-Pattern**: Fixed-size subset enumeration.  
> **Delta from Subsets**: Only collect when path length equals k.

### Implementation

```python
def combine(n: int, k: int) -> list[list[int]]:
    """
    Generate all combinations of k numbers from range [1, n].
    
    Algorithm:
    - Similar to subsets, but only collect when path has exactly k elements
    - Use start_index to enforce canonical ordering
    - Add pruning: stop early if remaining elements can't fill path to k
    
    Pruning Optimization:
    - If we need (k - len(path)) more elements, we need at least that many
      elements remaining in [i, n]
    - Elements remaining = n - i + 1
    - Prune when: n - i + 1 < k - len(path)
    - Equivalently: stop loop when i > n - (k - len(path)) + 1
    
    Time Complexity: O(k × C(n,k))
    Space Complexity: O(k)
    
    Args:
        n: Range upper bound [1..n]
        k: Size of each combination
        
    Returns:
        All combinations of k numbers from [1..n]
    """
    results: list[list[int]] = []
    path: list[int] = []
    
    def backtrack(start: int) -> None:
        # BASE CASE: Combination is complete
        if len(path) == k:
            results.append(path[:])
            return
        
        # PRUNING: Calculate upper bound for current loop
        # We need (k - len(path)) more elements
        # Available elements from start to n is (n - start + 1)
        # Stop when available < needed
        need = k - len(path)
        
        for i in range(start, n - need + 2):  # n - need + 1 + 1 for range
            path.append(i)
            backtrack(i + 1)
            path.pop()
    
    backtrack(1)
    return results
```

### Pruning Analysis

```
n=4, k=2

Without pruning:
start=1: try 1,2,3,4
  start=2: try 2,3,4
  start=3: try 3,4
  start=4: try 4     ← only 1 element left, need 1 more → works
  start=5: empty     ← wasted call

With pruning (need=2, loop until n-need+2=4):
start=1: try 1,2,3 (not 4, because 4→[] would fail)
  ...

This eliminates branches that can't possibly lead to valid combinations.
```

