## Base Template: Permutations (LeetCode 46)

> **Problem**: Given an array of distinct integers, return all possible permutations.  
> **Sub-Pattern**: Permutation Enumeration with used tracking.  
> **Key Insight**: At each position, try all unused elements.

### Implementation

```python
def permute(nums: list[int]) -> list[list[int]]:
    """
    Generate all permutations of distinct integers.
    
    Algorithm:
    - Build permutation position by position
    - Track which elements have been used with a boolean array
    - At each position, try every unused element
    - When path length equals nums length, we have a complete permutation
    
    Time Complexity: O(n! × n)
        - n! permutations to generate
        - O(n) to copy each permutation
    
    Space Complexity: O(n)
        - Recursion depth is n
        - Used array is O(n)
        - Output space not counted
    
    Args:
        nums: Array of distinct integers
        
    Returns:
        All possible permutations
    """
    results: list[list[int]] = []
    n = len(nums)
    
    # State: Current permutation being built
    path: list[int] = []
    
    # Tracking: Which elements are already used in current path
    used: list[bool] = [False] * n
    
    def backtrack() -> None:
        # BASE CASE: Permutation is complete
        if len(path) == n:
            results.append(path[:])  # Append a copy
            return
        
        # RECURSIVE CASE: Try each unused element
        for i in range(n):
            if used[i]:
                continue  # Skip already used elements
            
            # CHOOSE: Add element to permutation
            path.append(nums[i])
            used[i] = True
            
            # EXPLORE: Recurse to fill next position
            backtrack()
            
            # UNCHOOSE: Remove element (backtrack)
            path.pop()
            used[i] = False
    
    backtrack()
    return results
```

### Why This Works

The `used` array ensures each element appears exactly once in each permutation. The decision tree has:
- Level 0: n choices
- Level 1: n-1 choices  
- Level k: n-k choices
- Total leaves: n!

### Trace Example

```
Input: [1, 2, 3]

backtrack(path=[], used=[F,F,F])
├─ CHOOSE 1 → backtrack(path=[1], used=[T,F,F])
│  ├─ CHOOSE 2 → backtrack(path=[1,2], used=[T,T,F])
│  │  └─ CHOOSE 3 → backtrack(path=[1,2,3], used=[T,T,T])
│  │                 → SOLUTION: [1,2,3]
│  └─ CHOOSE 3 → backtrack(path=[1,3], used=[T,F,T])
│     └─ CHOOSE 2 → backtrack(path=[1,3,2], used=[T,T,T])
│                    → SOLUTION: [1,3,2]
├─ CHOOSE 2 → ... → [2,1,3], [2,3,1]
└─ CHOOSE 3 → ... → [3,1,2], [3,2,1]

Output: [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]
```

### Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Forgetting to copy | All results point to same list | Use `path[:]` or `list(path)` |
| Not unmarking used | Elements appear multiple times | Always set `used[i] = False` after recursion |
| Modifying during iteration | Concurrent modification errors | Iterate over indices, not elements |

