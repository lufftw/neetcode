## Variation: Find All Anagrams (LeetCode 438)

> **Problem**: Find all start indices of `p`'s anagrams in `s`.  
> **Invariant**: Window has exact same character frequencies as `p`.  
> **Delta from Permutation Check**: Collect all valid positions instead of returning on first.

### Implementation

```python
def find_anagrams(s: str, p: str) -> list[int]:
    """
    Find all start indices of p's anagrams in s.
    
    This is an extension of the permutation check:
    instead of returning True on first match, collect all match positions.
    
    Time Complexity: O(|s| + |p|)
    Space Complexity: O(1) - bounded by alphabet size
    
    Args:
        s: Source string to search in
        p: Pattern string (looking for its anagrams)
        
    Returns:
        List of starting indices where anagrams of p begin in s
    """
    result: list[int] = []
    
    if len(p) > len(s):
        return result
    
    pattern_length = len(p)
    
    # State: Frequency maps
    pattern_frequency: dict[str, int] = {}
    window_frequency: dict[str, int] = {}
    
    for char in p:
        pattern_frequency[char] = pattern_frequency.get(char, 0) + 1
    
    chars_matched = 0
    chars_to_match = len(pattern_frequency)
    
    for right, char in enumerate(s):
        # EXPAND: Add character to window
        window_frequency[char] = window_frequency.get(char, 0) + 1
        
        if char in pattern_frequency:
            if window_frequency[char] == pattern_frequency[char]:
                chars_matched += 1
            elif window_frequency[char] == pattern_frequency[char] + 1:
                chars_matched -= 1
        
        # CONTRACT: Remove leftmost when window is full
        left = right - pattern_length + 1
        if left > 0:
            left_char = s[left - 1]
            
            if left_char in pattern_frequency:
                if window_frequency[left_char] == pattern_frequency[left_char]:
                    chars_matched -= 1
                elif window_frequency[left_char] == pattern_frequency[left_char] + 1:
                    chars_matched += 1
            
            window_frequency[left_char] -= 1
            if window_frequency[left_char] == 0:
                del window_frequency[left_char]
        
        # COLLECT: Record starting index if window is an anagram
        if chars_matched == chars_to_match:
            result.append(left)
    
    return result
```

### Comparison: Permutation vs Anagram

| Aspect | Permutation (LeetCode 567) | Anagram (LeetCode 438) |
|--------|----------------------------|------------------------|
| Return type | `bool` | `list[int]` |
| On match | Return `True` | Append to result |
| After match | N/A | Continue searching |


