# Sliding Window Patterns: Complete Reference

> **API Kernel**: `SubstringSlidingWindow`  
> **Core Mechanism**: Maintain a dynamic window `[left, right]` over a sequence while preserving an invariant.

This document presents the **canonical sliding window template** and all its major variations. Each implementation follows consistent naming conventions and includes detailed logic explanations.

---

## Core Concepts

### The Sliding Window Invariant

Every sliding window algorithm maintains an **invariant** — a condition that must always be true for the current window `[left, right]`.

```
Window State:
┌─────────────────────────────────────────┐
│  ... [ left ─────── window ─────── right ] ...  │
│       └─────── invariant holds ───────┘         │
└─────────────────────────────────────────┘
```

### Universal Template Structure

```python
def sliding_window_template(sequence):
    """
    Generic sliding window template.
    
    Key components:
    1. State: Data structure tracking window contents
    2. Invariant: Condition that must hold for valid window
    3. Expand: Always move right pointer forward
    4. Contract: Move left pointer to restore invariant
    5. Update: Record answer when window is valid
    """
    state = initialize_state()
    left = 0
    answer = initial_answer()
    
    for right, element in enumerate(sequence):
        # EXPAND: Add element at right to window state
        update_state_add(state, element)
        
        # CONTRACT: Shrink window until invariant is restored
        while invariant_violated(state):
            update_state_remove(state, sequence[left])
            left += 1
        
        # UPDATE: Record answer for current valid window
        answer = update_answer(answer, left, right)
    
    return answer
```

### Two Window Strategies

| Strategy | When to Use | Example Problems |
|----------|-------------|------------------|
| **Maximize Window** | Find longest/largest valid window | LeetCode 3, 340, 424 |
| **Minimize Window** | Find shortest valid window | LeetCode 76, 209 |

## Table of Contents

1. [Core Concepts](#core-concepts)
2. [Base Template: Unique Characters (LeetCode 3)](#base-template-unique-characters-leetcode-3)
3. [Variation: Minimum Window Substring (LeetCode 76)](#variation-minimum-window-substring-leetcode-76)
4. [Variation: Minimum Size Subarray Sum (LeetCode 209)](#variation-minimum-size-subarray-sum-leetcode-209)
5. [Variation: At Most K Distinct Characters (LeetCode 340/159)](#variation-at-most-k-distinct-characters-leetcode-340159)
6. [Variation: Find All Anagrams (LeetCode 438)](#variation-find-all-anagrams-leetcode-438)
7. [Variation: Permutation in String (LeetCode 567)](#variation-permutation-in-string-leetcode-567)
8. [Pattern Comparison Table](#pattern-comparison-table)
9. [When to Use Sliding Window](#when-to-use-sliding-window)
10. [Template Quick Reference](#template-quick-reference)

---

## Base Template: Unique Characters (LeetCode 3)

> **Problem**: Find the length of the longest substring without repeating characters.  
> **Invariant**: All characters in window `[left, right]` are unique.  
> **Role**: BASE TEMPLATE for `SubstringSlidingWindow` API Kernel.

### Implementation

```python
def length_of_longest_substring(s: str) -> int:
    """
    Find the length of the longest substring without repeating characters.
    
    Algorithm:
    - Maintain a window where all characters are unique
    - Use a dictionary to track the last seen index of each character
    - When a duplicate is found, jump left pointer past the previous occurrence
    
    Time Complexity: O(n) - each character visited at most twice
    Space Complexity: O(min(n, σ)) - where σ is the alphabet size
    
    Args:
        s: Input string
        
    Returns:
        Length of the longest substring with all unique characters
    """
    # State: Map each character to its most recent index in the string
    last_seen_index: dict[str, int] = {}
    
    # Window boundaries
    left = 0
    max_length = 0
    
    for right, char in enumerate(s):
        # Check if character was seen within the current window
        # Key insight: We only care about occurrences at or after 'left'
        if char in last_seen_index and last_seen_index[char] >= left:
            # CONTRACT: Move left pointer past the previous occurrence
            # This single jump replaces the typical while-loop contraction
            left = last_seen_index[char] + 1
        
        # UPDATE: Record character's position for future duplicate detection
        last_seen_index[char] = right
        
        # UPDATE ANSWER: Current window [left, right] is valid
        # Window length = right - left + 1
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

### Why This Works

The key insight is the **jump optimization**: instead of incrementally shrinking the window with a while-loop, we directly jump `left` to `last_seen_index[char] + 1`.

This is valid because:
1. Any position before `last_seen_index[char]` would still include the duplicate
2. The position `last_seen_index[char] + 1` is the first position that excludes the duplicate
3. All characters between old `left` and new `left` are implicitly "removed" from consideration

### Trace Example

```
Input: "abcabcbb"

Step | right | char | last_seen_index      | left | window    | max_length
-----|-------|------|----------------------|------|-----------|------------
  0  |   0   |  'a' | {a:0}                |  0   | "a"       | 1
  1  |   1   |  'b' | {a:0, b:1}           |  0   | "ab"      | 2
  2  |   2   |  'c' | {a:0, b:1, c:2}      |  0   | "abc"     | 3
  3  |   3   |  'a' | {a:3, b:1, c:2}      |  1   | "bca"     | 3  ← 'a' seen at 0, jump to 1
  4  |   4   |  'b' | {a:3, b:4, c:2}      |  2   | "cab"     | 3  ← 'b' seen at 1, jump to 2
  5  |   5   |  'c' | {a:3, b:4, c:5}      |  3   | "abc"     | 3  ← 'c' seen at 2, jump to 3
  6  |   6   |  'b' | {a:3, b:6, c:5}      |  5   | "cb"      | 3  ← 'b' seen at 4, jump to 5
  7  |   7   |  'b' | {a:3, b:7, c:5}      |  7   | "b"       | 3  ← 'b' seen at 6, jump to 7

Answer: 3 ("abc")
```

---

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

---

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

---

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

---

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

---

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
         ├─┤        Window 0: "ei" - No match
          ├─┤       Window 1: "id" - No match
           ├─┤      Window 2: "db" - No match
            ├─┤     Window 3: "ba" - MATCH! (permutation of "ab")
```

---

## Pattern Comparison Table

| Problem | Invariant | State | Window Size | Goal |
|---------|-----------|-------|-------------|------|
| LeetCode 3 | All unique | `last_index` map | Variable | Maximize |
| LeetCode 340 | ≤K distinct | Frequency map | Variable | Maximize |
| LeetCode 76 | Contains all of t | Need/Have maps | Variable | Minimize |
| LeetCode 567 | Exact match | Frequency map | Fixed | Exists? |
| LeetCode 438 | Exact match | Frequency map | Fixed | All positions |
| LeetCode 209 | Sum ≥ target | Integer sum | Variable | Minimize |

---

## When to Use Sliding Window

### Problem Indicators

✅ **Use sliding window when:**
- Looking for contiguous subarray/substring
- Need to optimize (min/max) some property of the subarray
- Property can be maintained incrementally as window changes
- Adding/removing elements has O(1) state update

❌ **Don't use sliding window when:**
- Elements are not contiguous (use dynamic programming)
- Property requires global knowledge (use prefix sum + binary search)
- Window boundaries depend on non-local information

### Decision Flowchart

```
Is the answer a contiguous subarray/substring?
├── No → Use DP or other technique
└── Yes → Can you maintain window state incrementally?
          ├── No → Consider prefix sum or other technique
          └── Yes → Sliding Window!
                    ├── Fixed size window? → Use fixed window template
                    └── Variable size? → Maximize or Minimize?
                                        ├── Maximize → Expand always, contract on violation
                                        └── Minimize → Expand until valid, contract while valid
```

---

## Template Quick Reference

### Maximize Window (Variable Size)

```python
def maximize_window(sequence):
    state = {}
    left = 0
    max_result = 0
    
    for right, elem in enumerate(sequence):
        # Expand
        add_to_state(state, elem)
        
        # Contract while invalid
        while not is_valid(state):
            remove_from_state(state, sequence[left])
            left += 1
        
        # Update answer
        max_result = max(max_result, right - left + 1)
    
    return max_result
```

### Minimize Window (Variable Size)

```python
def minimize_window(sequence):
    state = {}
    left = 0
    min_result = float('inf')
    
    for right, elem in enumerate(sequence):
        # Expand
        add_to_state(state, elem)
        
        # Contract while valid (to minimize)
        while is_valid(state):
            min_result = min(min_result, right - left + 1)
            remove_from_state(state, sequence[left])
            left += 1
    
    return min_result if min_result != float('inf') else 0
```

### Fixed Size Window

```python
def fixed_window(sequence, k):
    state = {}
    result = []
    
    for right, elem in enumerate(sequence):
        # Expand
        add_to_state(state, elem)
        
        # Contract when window exceeds k
        if right >= k:
            remove_from_state(state, sequence[right - k])
        
        # Check condition when window is exactly k
        if right >= k - 1 and is_valid(state):
            result.append(process(state))
    
    return result
```



---



*Document generated for NeetCode Practice Framework — API Kernel: SubstringSlidingWindow*