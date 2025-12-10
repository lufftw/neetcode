## Variation: At Most K Distinct Characters (LeetCode 340/159)

> **Problem**: Find the length of the longest substring with at most K distinct characters.  
> **Invariant**: Number of distinct characters in window ≤ K.  
> **Delta from Base**: Replace "unique" check with "distinct count ≤ K".

### Implementation

```python
def length_of_longest_substring_k_distinct(s: str, k: int) -> int:
    """
    Find the length of the longest substring with at most K distinct characters.
    
    Algorithm:
    - Maintain a frequency map of characters in the current window
    - When distinct count exceeds K, shrink window from left until count ≤ K
    
    Time Complexity: O(n) - each character added and removed at most once
    Space Complexity: O(K) - at most K+1 entries in the frequency map
    
    Args:
        s: Input string
        k: Maximum number of distinct characters allowed
        
    Returns:
        Length of the longest valid substring
    """
    if k == 0:
        return 0
    
    # State: Frequency map tracking count of each character in window
    char_frequency: dict[str, int] = {}
    
    left = 0
    max_length = 0
    
    for right, char in enumerate(s):
        # EXPAND: Add character to window
        char_frequency[char] = char_frequency.get(char, 0) + 1
        
        # CONTRACT: Shrink window while we have more than K distinct characters
        # Unlike base template, we cannot jump — we must shrink incrementally
        # because removing one character might not restore the invariant
        while len(char_frequency) > k:
            left_char = s[left]
            char_frequency[left_char] -= 1
            
            # Remove character from map when its count reaches zero
            # This is crucial for correct distinct count via len(char_frequency)
            if char_frequency[left_char] == 0:
                del char_frequency[left_char]
            
            left += 1
        
        # UPDATE ANSWER: Window [left, right] has at most K distinct characters
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

### Specialization: At Most 2 Distinct (LeetCode 159)

```python
def length_of_longest_substring_two_distinct(s: str) -> int:
    """
    Find the length of the longest substring with at most 2 distinct characters.
    
    This is a direct application of the K-distinct template with K=2.
    """
    return length_of_longest_substring_k_distinct(s, k=2)
```

### Key Difference from Base Template

| Aspect | Base (Unique) | K-Distinct |
|--------|---------------|------------|
| State | `last_seen_index` | `char_frequency` |
| Invariant | All chars unique | `len(freq) ≤ K` |
| Contract | Single jump | While-loop shrink |
| Why | Jump to exclude duplicate | Must remove chars one by one |


