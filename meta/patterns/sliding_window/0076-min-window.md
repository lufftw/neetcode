## Variation: Minimum Window Substring (LeetCode 76)

> **Problem**: Find the minimum window in `s` that contains all characters of `t`.  
> **Invariant**: Window contains all required characters with sufficient frequency.  
> **Delta from Base**: Track "have vs need" frequencies; minimize instead of maximize.

### Implementation

```python
def min_window(s: str, t: str) -> str:
    """
    Find the minimum window substring of s that contains all characters of t.
    
    Algorithm:
    - Build a frequency map of required characters from t
    - Expand window to include required characters
    - Once all requirements are satisfied, contract to find minimum
    - Track the best (smallest) valid window found
    
    Time Complexity: O(|s| + |t|) - linear in both string lengths
    Space Complexity: O(|t|) - frequency maps bounded by t's unique characters
    
    Args:
        s: Source string to search in
        t: Target string containing required characters
        
    Returns:
        Minimum window substring, or "" if no valid window exists
    """
    if not t or not s:
        return ""
    
    # State: Required character frequencies (what we need)
    need_frequency: dict[str, int] = {}
    for char in t:
        need_frequency[char] = need_frequency.get(char, 0) + 1
    
    # State: Current window character frequencies (what we have)
    have_frequency: dict[str, int] = {}
    
    # Tracking: How many unique characters have met their required frequency
    chars_satisfied = 0
    chars_required = len(need_frequency)
    
    # Answer tracking
    min_length = float('inf')
    min_window_start = 0
    
    left = 0
    
    for right, char in enumerate(s):
        # EXPAND: Add character to window
        have_frequency[char] = have_frequency.get(char, 0) + 1
        
        # Check if this character just satisfied its requirement
        # Important: Only count when we EXACTLY meet the requirement
        # (not when we exceed it, to avoid double counting)
        if char in need_frequency and have_frequency[char] == need_frequency[char]:
            chars_satisfied += 1
        
        # CONTRACT: Once all requirements satisfied, try to minimize window
        while chars_satisfied == chars_required:
            # UPDATE ANSWER: Current window is valid, check if it's the smallest
            window_length = right - left + 1
            if window_length < min_length:
                min_length = window_length
                min_window_start = left
            
            # Remove leftmost character and update state
            left_char = s[left]
            have_frequency[left_char] -= 1
            
            # Check if removing this character breaks the requirement
            # Important: Only decrement when we DROP BELOW the requirement
            if left_char in need_frequency and have_frequency[left_char] < need_frequency[left_char]:
                chars_satisfied -= 1
            
            left += 1
    
    # Return result
    if min_length == float('inf'):
        return ""
    return s[min_window_start : min_window_start + min_length]
```

### Key Insight: Two-Phase Approach

```
Phase 1: EXPAND until window is valid (contains all required chars)
         ──────────────────────────────────────────────────────►
         
Phase 2: CONTRACT to minimize while still valid
         ◄─────────────────────────────────────
         
Phase 3: Record answer, then continue expanding
         ──────────────────────────────────────────────────────►
```

### The "Satisfied Counter" Optimization

Instead of checking `all(have[c] >= need[c] for c in need)` on every iteration (O(|t|)), we maintain `chars_satisfied`:

- Increment when `have[c]` reaches exactly `need[c]`
- Decrement when `have[c]` drops below `need[c]`
- Window is valid when `chars_satisfied == chars_required`

This reduces per-iteration cost from O(|t|) to O(1).


