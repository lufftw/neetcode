## Variation: Subsets (LeetCode 78)

> **Problem**: Given an array of distinct integers, return all possible subsets.  
> **Sub-Pattern**: Subset enumeration with start-index canonicalization.  
> **Key Insight**: Use a start index to avoid revisiting previous elements.

### Implementation

```python
def subsets(nums: list[int]) -> list[list[int]]:
    """
    Generate all subsets (power set) of distinct integers.
    
    Algorithm:
    - Each subset is a collection of elements with no ordering
    - To avoid duplicates like {1,2} and {2,1}, enforce canonical ordering
    - Use start_index to only consider elements at or after current position
    - Every intermediate path is a valid subset (collect at every node)
    
    Key Insight:
    - Unlike permutations, subsets don't need a "used" array
    - The start_index inherently prevents revisiting previous elements
    
    Time Complexity: O(n × 2^n)
        - 2^n subsets to generate
        - O(n) to copy each subset
    
    Space Complexity: O(n) for recursion depth
    
    Args:
        nums: Array of distinct integers
        
    Returns:
        All possible subsets
    """
    results: list[list[int]] = []
    n = len(nums)
    path: list[int] = []
    
    def backtrack(start_index: int) -> None:
        # COLLECT: Every path (including empty) is a valid subset
        results.append(path[:])
        
        # EXPLORE: Only consider elements from start_index onwards
        for i in range(start_index, n):
            # CHOOSE
            path.append(nums[i])
            
            # EXPLORE: Move start_index forward to enforce ordering
            backtrack(i + 1)
            
            # UNCHOOSE
            path.pop()
    
    backtrack(0)
    return results
```

### Why Start Index Works

```
Input: [1, 2, 3]

Decision tree with start_index:
[]                         ← start=0, collect []
├─ [1]                     ← start=1, collect [1]
│  ├─ [1,2]                ← start=2, collect [1,2]
│  │  └─ [1,2,3]           ← start=3, collect [1,2,3]
│  └─ [1,3]                ← start=3, collect [1,3]
├─ [2]                     ← start=2, collect [2]
│  └─ [2,3]                ← start=3, collect [2,3]
└─ [3]                     ← start=3, collect [3]

Total: 8 subsets = 2^3 ✓
```

The start_index ensures:
- We never pick element i after already having an element j > i
- This enforces a canonical ordering (ascending by index)
- Each subset is generated exactly once

