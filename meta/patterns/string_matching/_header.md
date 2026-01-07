# String Matching Patterns: Complete Reference

> **API Kernel**: `StringMatching`
> **Core Mechanism**: Efficient substring search using preprocessing (KMP failure function, rolling hash) to avoid redundant character comparisons.

This document presents the **canonical String Matching templates** covering KMP algorithm and Rabin-Karp rolling hash. These techniques are fundamental for pattern matching problems where brute-force O(mn) is too slow.

---

## Core Concepts

### The String Matching Problem

Given a **text** `t` of length n and a **pattern** `p` of length m, find all occurrences of `p` in `t`.

```
Naive approach: O(n * m) - slide pattern and compare each position
KMP approach:   O(n + m) - preprocess pattern to skip redundant comparisons
Rabin-Karp:     O(n + m) average - use rolling hash for fast comparison
```

### KMP: The Failure Function

The key insight of KMP is the **failure function** (also called prefix function or LPS array):

```
failure[i] = length of longest proper prefix of p[0:i+1] that is also a suffix

Example: pattern = "ABABAC"
Index:   0  1  2  3  4  5
Char:    A  B  A  B  A  C
LPS:     0  0  1  2  3  0

Explanation:
- failure[0] = 0: "A" has no proper prefix
- failure[1] = 0: "AB" has no matching prefix/suffix
- failure[2] = 1: "ABA" -> "A" is both prefix and suffix
- failure[3] = 2: "ABAB" -> "AB" is both prefix and suffix
- failure[4] = 3: "ABABA" -> "ABA" is both prefix and suffix
- failure[5] = 0: "ABABAC" -> no matching prefix/suffix
```

### KMP Search Algorithm

```python
def kmp_search(text: str, pattern: str) -> list[int]:
    """
    Find all occurrences of pattern in text using KMP algorithm.

    Key insight: When mismatch occurs at position j in pattern,
    we don't restart from 0. Instead, we jump to failure[j-1]
    because that prefix has already been matched.

    Time: O(n + m) where n = len(text), m = len(pattern)
    Space: O(m) for the failure function
    """
    if not pattern:
        return [0]
    if not text or len(pattern) > len(text):
        return []

    # Build failure function
    pattern_length = len(pattern)
    failure = [0] * pattern_length

    # Compute failure function using self-matching
    prefix_length = 0
    for i in range(1, pattern_length):
        # Backtrack until we find a match or reach 0
        while prefix_length > 0 and pattern[i] != pattern[prefix_length]:
            prefix_length = failure[prefix_length - 1]

        if pattern[i] == pattern[prefix_length]:
            prefix_length += 1

        failure[i] = prefix_length

    # Search for pattern in text
    matches = []
    pattern_idx = 0

    for text_idx, text_char in enumerate(text):
        # Backtrack pattern pointer on mismatch
        while pattern_idx > 0 and text_char != pattern[pattern_idx]:
            pattern_idx = failure[pattern_idx - 1]

        if text_char == pattern[pattern_idx]:
            pattern_idx += 1

        if pattern_idx == pattern_length:
            # Found a match
            matches.append(text_idx - pattern_length + 1)
            # Continue searching (overlapping matches)
            pattern_idx = failure[pattern_idx - 1]

    return matches
```

### Rabin-Karp: Rolling Hash

Rabin-Karp uses a hash function to quickly compare pattern with text windows:

```python
def rabin_karp_search(text: str, pattern: str) -> list[int]:
    """
    Find all occurrences of pattern in text using Rabin-Karp.

    Key insight: Use rolling hash to compute hash of each window in O(1).
    hash(s[i:i+m]) can be computed from hash(s[i-1:i-1+m]) by:
    1. Remove contribution of s[i-1]
    2. Add contribution of s[i+m-1]

    Time: O(n + m) average, O(nm) worst case (hash collisions)
    Space: O(1) excluding output
    """
    if not pattern or len(pattern) > len(text):
        return []

    pattern_length = len(pattern)
    text_length = len(text)
    BASE = 256  # Character set size
    MOD = 10**9 + 7  # Large prime to reduce collisions

    # Compute hash of pattern and first window
    pattern_hash = 0
    window_hash = 0
    highest_power = 1  # BASE^(m-1) mod MOD

    for i in range(pattern_length):
        pattern_hash = (pattern_hash * BASE + ord(pattern[i])) % MOD
        window_hash = (window_hash * BASE + ord(text[i])) % MOD
        if i < pattern_length - 1:
            highest_power = (highest_power * BASE) % MOD

    matches = []

    # Slide the window
    for i in range(text_length - pattern_length + 1):
        if pattern_hash == window_hash:
            # Verify character by character (handle hash collision)
            if text[i:i + pattern_length] == pattern:
                matches.append(i)

        # Compute hash for next window
        if i < text_length - pattern_length:
            # Remove leading char, add trailing char
            window_hash = (window_hash - ord(text[i]) * highest_power) % MOD
            window_hash = (window_hash * BASE + ord(text[i + pattern_length])) % MOD
            window_hash = (window_hash + MOD) % MOD  # Handle negative

    return matches
```

### When to Use Each Algorithm

| Algorithm | Best For | Pros | Cons |
|-----------|----------|------|------|
| **KMP** | Single pattern search | Guaranteed O(n+m), no false positives | Need to build failure function |
| **Rabin-Karp** | Multiple pattern search, fingerprinting | Easy to extend, good average case | Worst case O(nm) on collisions |
| **Z-Algorithm** | Prefix matching, string periods | Elegant, single pass | Less intuitive |

### Common Applications

1. **Find First Occurrence** (LC 28): Basic substring search
2. **Shortest Palindrome** (LC 214): KMP to find longest palindromic prefix
3. **Repeated Substring** (LC 459): KMP failure function property
4. **Repeated String Match** (LC 686): Rolling hash for efficiency
5. **Longest Happy Prefix** (LC 1392): Direct KMP application

