## Variation: Palindrome Partitioning (LeetCode 131)

> **Problem**: Partition a string such that every substring is a palindrome.  
> **Sub-Pattern**: String segmentation with validity check.  
> **Key Insight**: Try all cut positions, validate each segment.

### Implementation

```python
def partition(s: str) -> list[list[str]]:
    """
    Partition string so every part is a palindrome.
    
    Algorithm:
    - Try cutting at each position from current start
    - Check if prefix is palindrome; if yes, recurse on suffix
    - When start reaches end of string, we have a valid partition
    
    Key Insight:
    - Each "choice" is where to cut the string
    - Only proceed if the cut-off prefix is a palindrome
    
    Optimization:
    - Precompute palindrome status with DP for O(1) checks
    - Without precompute: O(n) per check, O(n^3) total
    - With precompute: O(n^2) preprocessing, O(1) per check
    
    Time Complexity: O(n × 2^n) worst case
        - 2^(n-1) possible partitions (n-1 cut positions)
        - O(n) to copy each partition
    
    Space Complexity: O(n) for recursion
    
    Args:
        s: Input string
        
    Returns:
        All palindrome partitionings
    """
    results: list[list[str]] = []
    path: list[str] = []
    n = len(s)
    
    # Precompute: is_palindrome[i][j] = True if s[i:j+1] is palindrome
    is_palindrome = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j]:
                if j - i <= 2:
                    is_palindrome[i][j] = True
                else:
                    is_palindrome[i][j] = is_palindrome[i + 1][j - 1]
    
    def backtrack(start: int) -> None:
        # BASE CASE: Reached end of string
        if start == n:
            results.append(path[:])
            return
        
        # Try each end position for current segment
        for end in range(start, n):
            # VALIDITY CHECK: Only proceed if palindrome
            if not is_palindrome[start][end]:
                continue
            
            path.append(s[start:end + 1])
            backtrack(end + 1)
            path.pop()
    
    backtrack(0)
    return results
```

