## Variation: Permutation in String (LeetCode 567)

> **Problem**: Check if `s2` contains any permutation of `s1`.  
> **Invariant**: Window has exact same character frequencies as `s1`.  
> **Delta from Base**: Fixed window size; exact frequency match.

### Implementation

```python
def check_inclusion(s1: str, s2: str) -> bool:
    """
    Check if s2 contains any permutation of s1.
    
    A permutation means same characters with same frequencies.
    We use a fixed-size sliding window of length len(s1).
    
    Algorithm:
    - Build frequency map of s1 (the pattern)
    - Slide a window of size len(s1) over s2
    - Check if window frequency matches pattern frequency
    
    Time Complexity: O(|s1| + |s2|) - build pattern + single pass over s2
    Space Complexity: O(1) - at most 26 lowercase letters
    
    Args:
        s1: Pattern string (looking for its permutation)
        s2: Source string to search in
        
    Returns:
        True if s2 contains a permutation of s1
    """
    if len(s1) > len(s2):
        return False
    
    pattern_length = len(s1)
    
    # State: Frequency maps
    pattern_frequency: dict[str, int] = {}
    window_frequency: dict[str, int] = {}
    
    # Build pattern frequency map
    for char in s1:
        pattern_frequency[char] = pattern_frequency.get(char, 0) + 1
    
    # Optimization: Track how many characters have matching frequencies
    chars_matched = 0
    chars_to_match = len(pattern_frequency)
    
    for right, char in enumerate(s2):
        # EXPAND: Add character to window
        window_frequency[char] = window_frequency.get(char, 0) + 1
        
        # Update match count for added character
        if char in pattern_frequency:
            if window_frequency[char] == pattern_frequency[char]:
                chars_matched += 1
            elif window_frequency[char] == pattern_frequency[char] + 1:
                # We just exceeded the required count
                chars_matched -= 1
        
        # CONTRACT: Remove leftmost character when window exceeds pattern length
        if right >= pattern_length:
            left_char = s2[right - pattern_length]
            
            # Update match count for removed character
            if left_char in pattern_frequency:
                if window_frequency[left_char] == pattern_frequency[left_char]:
                    chars_matched -= 1
                elif window_frequency[left_char] == pattern_frequency[left_char] + 1:
                    # Removing brings us back to exact match
                    chars_matched += 1
            
            window_frequency[left_char] -= 1
            if window_frequency[left_char] == 0:
                del window_frequency[left_char]
        
        # CHECK: If all characters match, we found a permutation
        if chars_matched == chars_to_match:
            return True
    
    return False
```

### Key Difference: Fixed Window Size

Unlike variable-size windows, this problem uses a **fixed window** of size `len(s1)`:

```
Pattern: "ab" (length 2)
Source:  "eidbaooo"
          ├┤        Window 0: "ei" - No match
           ├┤       Window 1: "id" - No match
            ├┤      Window 2: "db" - No match
             ├┤     Window 3: "ba" - MATCH! (permutation of "ab")
```


