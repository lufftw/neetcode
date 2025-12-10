## Variation: Minimum Size Subarray Sum (LeetCode 209)

> **Problem**: Find the minimal length subarray with sum ≥ target.  
> **Invariant**: Window sum ≥ target.  
> **Delta from Base**: Numeric sum instead of character tracking; minimize window.

### Implementation

```python
def min_subarray_len(target: int, nums: list[int]) -> int:
    """
    Find the minimal length of a subarray whose sum is >= target.
    
    Algorithm:
    - Maintain a running sum of the current window
    - Expand window by adding elements
    - Once sum >= target, contract to find minimum length
    - Continue until all elements are processed
    
    Time Complexity: O(n) - each element added and removed at most once
    Space Complexity: O(1) - only tracking sum and pointers
    
    Args:
        target: Target sum to reach or exceed
        nums: Array of positive integers
        
    Returns:
        Minimum length of valid subarray, or 0 if none exists
    """
    n = len(nums)
    if n == 0:
        return 0
    
    # State: Running sum of current window
    window_sum = 0
    
    left = 0
    min_length = float('inf')
    
    for right, num in enumerate(nums):
        # EXPAND: Add element to window sum
        window_sum += num
        
        # CONTRACT: While sum satisfies target, try to minimize window
        # Note: We use 'while' not 'if' because multiple contractions may be possible
        while window_sum >= target:
            # UPDATE ANSWER: Current window is valid
            min_length = min(min_length, right - left + 1)
            
            # Remove leftmost element
            window_sum -= nums[left]
            left += 1
    
    return min_length if min_length != float('inf') else 0
```

### Key Difference: Numeric State

| Aspect | String Patterns | Numeric Sum |
|--------|-----------------|-------------|
| State | Frequency map | Single integer |
| Add element | `freq[c] += 1` | `sum += num` |
| Remove element | `freq[c] -= 1` | `sum -= num` |
| Check invariant | `len(freq) > k` | `sum >= target` |


