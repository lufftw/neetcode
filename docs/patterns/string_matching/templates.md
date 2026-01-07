# String Matching Patterns: Complete Reference

> **API Kernel**: `StringMatching`
> **Core Mechanism**: Efficient substring search using preprocessing (KMP failure function, rolling hash) to avoid redundant character comparisons.

This document presents the **canonical String Matching templates** covering KMP algorithm and Rabin-Karp rolling hash. These techniques are fundamental for pattern matching problems where brute-force O(mn) is too slow.

---

## Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Base Template: Find the Index of First Occurrence (LeetCode 28)](#2-base-template-find-the-index-of-first-occurrence-leetcode-28)
3. [Variant: Shortest Palindrome (LeetCode 214)](#3-variant-shortest-palindrome-leetcode-214)
4. [Variant: Repeated Substring Pattern (LeetCode 459)](#4-variant-repeated-substring-pattern-leetcode-459)
5. [Variant: Longest Happy Prefix (LeetCode 1392)](#5-variant-longest-happy-prefix-leetcode-1392)
6. [Pattern Comparison Table](#6-pattern-comparison-table)
7. [Decision Tree](#7-decision-tree)
8. [Pattern Selection Guide](#8-pattern-selection-guide)
9. [Problem Type Recognition](#9-problem-type-recognition)
10. [Universal Templates](#10-universal-templates)
11. [Quick Reference](#11-quick-reference)

---

## 1. Core Concepts

### 1.1 The String Matching Problem

Given a **text** `t` of length n and a **pattern** `p` of length m, find all occurrences of `p` in `t`.

```
Naive approach: O(n * m) - slide pattern and compare each position
KMP approach:   O(n + m) - preprocess pattern to skip redundant comparisons
Rabin-Karp:     O(n + m) average - use rolling hash for fast comparison
```

### 1.2 KMP: The Failure Function

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

### 1.3 KMP Search Algorithm

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

### 1.4 Rabin-Karp: Rolling Hash

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

### 1.5 When to Use Each Algorithm

| Algorithm | Best For | Pros | Cons |
|-----------|----------|------|------|
| **KMP** | Single pattern search | Guaranteed O(n+m), no false positives | Need to build failure function |
| **Rabin-Karp** | Multiple pattern search, fingerprinting | Easy to extend, good average case | Worst case O(nm) on collisions |
| **Z-Algorithm** | Prefix matching, string periods | Elegant, single pass | Less intuitive |

### 1.6 Common Applications

1. **Find First Occurrence** (LC 28): Basic substring search
2. **Shortest Palindrome** (LC 214): KMP to find longest palindromic prefix
3. **Repeated Substring** (LC 459): KMP failure function property
4. **Repeated String Match** (LC 686): Rolling hash for efficiency
5. **Longest Happy Prefix** (LC 1392): Direct KMP application

---

## 2. Base Template: Find the Index of First Occurrence (LeetCode 28)

> **Problem**: Given two strings `haystack` and `needle`, return the index of the first occurrence of `needle` in `haystack`, or -1 if `needle` is not part of `haystack`.
> **Invariant**: Use KMP failure function to skip redundant comparisons.
> **Role**: BASE TEMPLATE for `StringMatching` API Kernel.

### 2.1 Why This Is The Base Template

LC 28 is the purest form of string matching:
- **Single pattern search**: Find one pattern in text
- **First occurrence only**: No need to find all matches
- **Foundation for variants**: KMP failure function is the key building block

### 2.2 Implementation

```python
class SolutionKMP:
    def strStr(self, haystack: str, needle: str) -> int:
        """
        Find first occurrence of needle in haystack using KMP.

        The KMP algorithm preprocesses the pattern to build a failure function.
        On mismatch, instead of restarting, we use the failure function to
        skip characters that we know will match.

        Time: O(m + n) where m = len(haystack), n = len(needle)
        Space: O(n) for the failure function
        """
        if not needle:
            return 0

        needle_length = len(needle)
        haystack_length = len(haystack)

        if needle_length > haystack_length:
            return -1

        # Build failure function (LPS array)
        # failure[i] = length of longest proper prefix of needle[0:i+1]
        # that is also a suffix
        failure: list[int] = [0] * needle_length

        prefix_length = 0
        for i in range(1, needle_length):
            # Backtrack until match or reach start
            while prefix_length > 0 and needle[i] != needle[prefix_length]:
                prefix_length = failure[prefix_length - 1]

            if needle[i] == needle[prefix_length]:
                prefix_length += 1

            failure[i] = prefix_length

        # Search using failure function
        needle_idx = 0

        for haystack_idx in range(haystack_length):
            haystack_char = haystack[haystack_idx]

            # On mismatch, use failure function to skip
            while needle_idx > 0 and haystack_char != needle[needle_idx]:
                needle_idx = failure[needle_idx - 1]

            if haystack_char == needle[needle_idx]:
                needle_idx += 1

            if needle_idx == needle_length:
                # Found first match
                return haystack_idx - needle_length + 1

        return -1
```

### 2.3 Alternative: Rabin-Karp Implementation

```python
class SolutionRabinKarp:
    def strStr(self, haystack: str, needle: str) -> int:
        """
        Find first occurrence using Rabin-Karp rolling hash.

        Use polynomial rolling hash to compare windows in O(1) average.
        Verify on hash match to handle collisions.

        Time: O(m + n) average, O(mn) worst case
        Space: O(1)
        """
        if not needle:
            return 0

        needle_length = len(needle)
        haystack_length = len(haystack)

        if needle_length > haystack_length:
            return -1

        BASE = 256
        MOD = 10**9 + 7

        # Compute initial hashes
        needle_hash = 0
        window_hash = 0
        highest_power = 1

        for i in range(needle_length):
            needle_hash = (needle_hash * BASE + ord(needle[i])) % MOD
            window_hash = (window_hash * BASE + ord(haystack[i])) % MOD
            if i < needle_length - 1:
                highest_power = (highest_power * BASE) % MOD

        # Slide and compare
        for i in range(haystack_length - needle_length + 1):
            if needle_hash == window_hash:
                # Verify to avoid false positives
                if haystack[i:i + needle_length] == needle:
                    return i

            # Update hash for next window
            if i < haystack_length - needle_length:
                window_hash = (window_hash - ord(haystack[i]) * highest_power) % MOD
                window_hash = (window_hash * BASE + ord(haystack[i + needle_length])) % MOD
                window_hash = (window_hash + MOD) % MOD

        return -1
```

### 2.4 Trace Example (KMP)

```
haystack = "ABABDABACDABABCABAB"
needle = "ABABCABAB"

Build failure function for "ABABCABAB":
Index:   0  1  2  3  4  5  6  7  8
Char:    A  B  A  B  C  A  B  A  B
failure: 0  0  1  2  0  1  2  3  4

Search:
Position 0-3: "ABAB" matches needle[0:4]
Position 4: 'D' != 'C', backtrack to failure[3] = 2
Position 4: 'D' != 'A', backtrack to failure[1] = 0
Position 4: 'D' != 'A', needle_idx = 0
...continue...
Position 10-18: "ABABCABAB" matches completely!

Return: 10
```

### 2.5 Key Insights

1. **Failure Function**: Core of KMP - tells us where to resume on mismatch
2. **No Backtracking in Text**: Text pointer never goes backward, guaranteeing O(n)
3. **Self-Matching**: Failure function is computed by matching pattern against itself
4. **Z-Algorithm Alternative**: Z-array can solve same problems with different approach

---

## 3. Variant: Shortest Palindrome (LeetCode 214)

> **Problem**: Given a string `s`, prepend characters to make it a palindrome and return the shortest such palindrome.
> **Invariant**: Use KMP to find the longest palindromic prefix.
> **Delta from Base**: Apply KMP on `s + '#' + reverse(s)` to find longest prefix that is also suffix.

### 3.1 Key Insight

The shortest palindrome is formed by:
1. Finding the longest palindromic prefix of `s`
2. Prepending the reverse of the remaining suffix

To find longest palindromic prefix, concatenate `s + '#' + reverse(s)` and compute KMP failure function. The value at the last position gives us the answer.

### 3.2 Implementation

```python
class SolutionKMP:
    def shortestPalindrome(self, s: str) -> str:
        """
        Find shortest palindrome by prepending characters to s.

        Key insight: Longest palindromic prefix of s equals the longest
        proper prefix of (s + '#' + reverse(s)) that is also a suffix.

        The '#' separator prevents false matches across the boundary.

        Time: O(n)
        Space: O(n)
        """
        if not s or len(s) <= 1:
            return s

        # Create concatenated string with separator
        reversed_s = s[::-1]
        concat = s + '#' + reversed_s

        # Build failure function
        concat_length = len(concat)
        failure: list[int] = [0] * concat_length

        prefix_length = 0
        for i in range(1, concat_length):
            while prefix_length > 0 and concat[i] != concat[prefix_length]:
                prefix_length = failure[prefix_length - 1]

            if concat[i] == concat[prefix_length]:
                prefix_length += 1

            failure[i] = prefix_length

        # failure[-1] = length of longest palindromic prefix
        palindrome_prefix_length = failure[-1]

        # Prepend reverse of non-palindromic suffix
        suffix_to_prepend = reversed_s[:len(s) - palindrome_prefix_length]

        return suffix_to_prepend + s
```

### 3.3 Alternative: Rolling Hash Approach

```python
class SolutionRollingHash:
    def shortestPalindrome(self, s: str) -> str:
        """
        Use rolling hash to find longest palindromic prefix.

        Compute forward and backward hashes simultaneously.
        When they match at position i, s[0:i+1] is a palindrome.

        Time: O(n)
        Space: O(1)
        """
        if not s or len(s) <= 1:
            return s

        BASE = 29
        MOD = 10**9 + 7

        forward_hash = 0
        backward_hash = 0
        power = 1
        longest_palindrome_end = 0

        for i, char in enumerate(s):
            char_val = ord(char) - ord('a') + 1

            # Forward hash: h = h * BASE + char
            forward_hash = (forward_hash * BASE + char_val) % MOD

            # Backward hash: h = h + char * BASE^i
            backward_hash = (backward_hash + char_val * power) % MOD

            if forward_hash == backward_hash:
                # Potential palindromic prefix (may need verification)
                longest_palindrome_end = i

            power = (power * BASE) % MOD

        # Prepend reverse of suffix after longest palindromic prefix
        suffix = s[longest_palindrome_end + 1:]
        return suffix[::-1] + s
```

### 3.4 Trace Example

```
s = "aacecaaa"
reversed = "aaacecaa"
concat = "aacecaaa#aaacecaa"

Failure function:
Index: 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16
Char:  a  a  c  e  c  a  a  a  #  a  a  a  c  e  c  a  a
LPS:   0  1  0  0  0  1  2  2  0  1  2  2  3  4  5  6  7

failure[-1] = 7
Longest palindromic prefix = "aacecaa" (length 7)
Remaining suffix = "a"
Prepend reverse of "a" = "a"

Result: "a" + "aacecaaa" = "aaacecaaa"
```

### 3.5 Key Insights

1. **Separator Is Critical**: '#' prevents matching across s and reverse(s)
2. **Failure Function Property**: failure[-1] = longest proper prefix = suffix
3. **Rolling Hash Alternative**: No separator needed, but may have false positives
4. **Why Not Brute Force**: Checking each prefix for palindrome would be O(n²)

---

## 4. Variant: Repeated Substring Pattern (LeetCode 459)

> **Problem**: Given a string `s`, check if it can be constructed by taking a substring of it and appending multiple copies of the substring together.
> **Invariant**: Use KMP failure function property for periodic strings.
> **Delta from Base**: Check if `n % (n - failure[n-1]) == 0` and the period divides n.

### 4.1 Key Insight

For a string to be constructed from repeated substrings:
- The pattern length must divide the string length evenly
- Using KMP: if `failure[n-1] > 0` and `n % (n - failure[n-1]) == 0`, the string is periodic

The minimum period length is `n - failure[n-1]`.

### 4.2 Implementation

```python
class SolutionKMP:
    def repeatedSubstringPattern(self, s: str) -> bool:
        """
        Check if string is built from repeated substrings using KMP.

        Property: For periodic string, failure[n-1] = n - period_length.
        So period_length = n - failure[n-1].
        String is periodic if period_length divides n and period_length < n.

        Time: O(n)
        Space: O(n)
        """
        string_length = len(s)

        if string_length <= 1:
            return False

        # Build failure function
        failure: list[int] = [0] * string_length

        prefix_length = 0
        for i in range(1, string_length):
            while prefix_length > 0 and s[i] != s[prefix_length]:
                prefix_length = failure[prefix_length - 1]

            if s[i] == s[prefix_length]:
                prefix_length += 1

            failure[i] = prefix_length

        # Check periodicity
        longest_prefix_suffix = failure[-1]

        if longest_prefix_suffix == 0:
            return False

        period_length = string_length - longest_prefix_suffix

        # Valid if period divides string length and is not the full string
        return string_length % period_length == 0
```

### 4.3 Alternative: Concatenation Trick

```python
class SolutionConcatenation:
    def repeatedSubstringPattern(self, s: str) -> bool:
        """
        Elegant trick: s + s contains s at non-boundary position iff s is periodic.

        If s = "abab", then s + s = "abababab"
        Remove first and last char: "bababa"
        This still contains "abab" because it's periodic!

        Time: O(n) with efficient string search
        Space: O(n)
        """
        doubled = s + s
        # Remove first and last character to avoid trivial matches
        return s in doubled[1:-1]
```

### 4.4 Trace Example

```
s = "abab"

Build failure function:
Index: 0  1  2  3
Char:  a  b  a  b
LPS:   0  0  1  2

failure[-1] = 2
period_length = 4 - 2 = 2
4 % 2 == 0 ✓

The string is built from "ab" repeated twice.

s = "abcab"

Build failure function:
Index: 0  1  2  3  4
Char:  a  b  c  a  b
LPS:   0  0  0  1  2

failure[-1] = 2
period_length = 5 - 2 = 3
5 % 3 != 0 ✗

Not periodic.
```

### 4.5 Key Insights

1. **KMP Property**: failure[n-1] reveals periodic structure
2. **Period Formula**: period = n - failure[n-1]
3. **Concatenation Trick**: Simpler but uses built-in string search
4. **Edge Cases**: Single character returns False, must have period < n

---

## 5. Variant: Longest Happy Prefix (LeetCode 1392)

> **Problem**: A string is called a happy prefix if it is both a prefix and suffix (excluding entire string). Return the longest happy prefix of the given string.
> **Invariant**: Direct application of KMP failure function.
> **Delta from Base**: Return s[0:failure[n-1]] directly.

### 5.1 Key Insight

This is the most direct application of the KMP failure function:
- `failure[n-1]` gives exactly the length of the longest proper prefix that is also a suffix
- Just return the first `failure[n-1]` characters

### 5.2 Implementation

```python
class SolutionKMP:
    def longestPrefix(self, s: str) -> str:
        """
        Find longest happy prefix using KMP failure function.

        The failure function at position n-1 gives exactly what we need:
        the length of the longest proper prefix that is also a suffix.

        Time: O(n)
        Space: O(n)
        """
        string_length = len(s)

        if string_length <= 1:
            return ""

        # Build failure function
        failure: list[int] = [0] * string_length

        prefix_length = 0
        for i in range(1, string_length):
            while prefix_length > 0 and s[i] != s[prefix_length]:
                prefix_length = failure[prefix_length - 1]

            if s[i] == s[prefix_length]:
                prefix_length += 1

            failure[i] = prefix_length

        # The answer is directly failure[n-1]
        happy_prefix_length = failure[-1]

        return s[:happy_prefix_length]
```

### 5.3 Alternative: Rolling Hash

```python
class SolutionRollingHash:
    def longestPrefix(self, s: str) -> str:
        """
        Find longest happy prefix using rolling hash.

        Compute prefix and suffix hashes simultaneously.
        Track longest match where both hashes are equal.

        Time: O(n)
        Space: O(1)
        """
        string_length = len(s)

        if string_length <= 1:
            return ""

        BASE = 31
        MOD = 10**9 + 7

        prefix_hash = 0
        suffix_hash = 0
        power = 1
        longest_length = 0

        # Compare prefix s[0:i+1] with suffix s[n-i-1:n]
        for i in range(string_length - 1):
            prefix_char = ord(s[i]) - ord('a') + 1
            suffix_char = ord(s[string_length - 1 - i]) - ord('a') + 1

            # Prefix hash: h = h * BASE + char (left to right)
            prefix_hash = (prefix_hash * BASE + prefix_char) % MOD

            # Suffix hash: h = h + char * power (right to left, building from end)
            suffix_hash = (suffix_hash + suffix_char * power) % MOD

            power = (power * BASE) % MOD

            if prefix_hash == suffix_hash:
                longest_length = i + 1

        return s[:longest_length]
```

### 5.4 Trace Example

```
s = "ababab"

Build failure function:
Index: 0  1  2  3  4  5
Char:  a  b  a  b  a  b
LPS:   0  0  1  2  3  4

failure[-1] = 4
Longest happy prefix = "abab"

Verification:
- Prefix: s[0:4] = "abab" ✓
- Suffix: s[2:6] = "abab" ✓
```

### 5.5 Key Insights

1. **Direct Application**: failure[-1] is exactly what we need
2. **Proper Prefix**: Must exclude entire string (handled by failure function)
3. **Rolling Hash Alternative**: Useful when you need to avoid preprocessing
4. **Empty String**: Return "" if no happy prefix exists

---

## 6. Pattern Comparison Table

| Problem | Algorithm | Key Technique | Time | Space |
|---------|-----------|---------------|------|-------|
| **LC 28: Find Index** | KMP / Rabin-Karp | Direct pattern search | O(n+m) | O(m) |
| **LC 214: Shortest Palindrome** | KMP | `s + '#' + reverse(s)` | O(n) | O(n) |
| **LC 459: Repeated Substring** | KMP | Period = n - failure[n-1] | O(n) | O(n) |
| **LC 1392: Longest Happy Prefix** | KMP | Return s[0:failure[n-1]] | O(n) | O(n) |

### 6.1 Algorithm Selection Guide

| Use Case | Recommended Algorithm | Reason |
|----------|----------------------|--------|
| Single pattern search | KMP | Guaranteed O(n+m), simple |
| Multiple pattern search | Rabin-Karp | Hash fingerprinting |
| Finding periods | KMP failure function | Built-in property |
| Palindrome problems | KMP with concatenation | Elegant reduction |

### 6.2 Failure Function Applications

| Application | How to Use failure[] |
|-------------|---------------------|
| Pattern search | Backtrack on mismatch |
| String period | Period = n - failure[n-1] |
| Longest prefix=suffix | Answer = failure[n-1] |
| Palindromic prefix | Use `s + '#' + rev(s)` |

### 6.3 Time Complexity Comparison

| Algorithm | Preprocessing | Search | Total | Worst Case |
|-----------|--------------|--------|-------|------------|
| Naive | O(1) | O(nm) | O(nm) | O(nm) |
| KMP | O(m) | O(n) | O(n+m) | O(n+m) |
| Rabin-Karp | O(m) | O(n) avg | O(n+m) avg | O(nm) |
| Z-Algorithm | O(m) | O(n) | O(n+m) | O(n+m) |

---

## 7. Decision Tree

```
Start: String matching/search problem?
            │
            ▼
    ┌───────────────────┐
    │ What's the goal?  │
    └───────────────────┘
            │
    ┌───────┼───────┬───────────┐
    ▼       ▼       ▼           ▼
Find      Check   Find        Find
pattern   period  palindrome  prefix=suffix
    │       │     prefix      │
    ▼       ▼       │         ▼
Use KMP   Period    ▼       Direct
or R-K    formula  KMP+rev  failure[-1]
```

## 8. Pattern Selection Guide

### 8.1 Use KMP (LC 28, 1392) when:
- Searching for a pattern in text
- Need guaranteed O(n+m) time
- Finding longest prefix=suffix
- Working with failure function properties

### 8.2 Use Rabin-Karp when:
- Searching multiple patterns
- Need average-case efficiency
- Hash fingerprinting is useful
- Willing to accept worst-case O(nm)

### 8.3 Use Period Formula (LC 459) when:
- Checking if string is built from repeating unit
- Finding minimum period length
- Detecting cyclic patterns

### 8.4 Use Concatenation Trick (LC 214) when:
- Finding palindromic prefixes
- Combining KMP with string reversal
- Need to find overlapping structures

## 9. Problem Type Recognition

| Keywords/Clues | Pattern |
|----------------|---------|
| "find first occurrence" | KMP search |
| "repeated substring" | KMP period |
| "shortest palindrome" | KMP + reverse |
| "happy prefix" | KMP failure[-1] |
| "pattern matching" | KMP or Rabin-Karp |

---

## 10. Universal Templates

### 10.1 Template 1: KMP Failure Function

```python
def build_failure(pattern: str) -> list[int]:
    """
    Build KMP failure function (LPS array).
    failure[i] = length of longest proper prefix of pattern[0:i+1]
                 that is also a suffix.
    Time: O(m), Space: O(m)
    """
    m = len(pattern)
    failure = [0] * m

    prefix_length = 0
    for i in range(1, m):
        while prefix_length > 0 and pattern[i] != pattern[prefix_length]:
            prefix_length = failure[prefix_length - 1]

        if pattern[i] == pattern[prefix_length]:
            prefix_length += 1

        failure[i] = prefix_length

    return failure
```

**Use for**: LC 28, 214, 459, 1392

---

### 10.2 Template 2: KMP Search

```python
def kmp_search(text: str, pattern: str) -> int:
    """
    Find first occurrence of pattern in text.
    Time: O(n+m), Space: O(m)
    """
    if not pattern:
        return 0
    if len(pattern) > len(text):
        return -1

    failure = build_failure(pattern)
    pattern_idx = 0

    for text_idx, char in enumerate(text):
        while pattern_idx > 0 and char != pattern[pattern_idx]:
            pattern_idx = failure[pattern_idx - 1]

        if char == pattern[pattern_idx]:
            pattern_idx += 1

        if pattern_idx == len(pattern):
            return text_idx - len(pattern) + 1

    return -1
```

**Use for**: LC 28, and as building block for others

---

### 10.3 Template 3: Rabin-Karp Rolling Hash

```python
def rabin_karp(text: str, pattern: str) -> int:
    """
    Find first occurrence using rolling hash.
    Time: O(n+m) average, Space: O(1)
    """
    if not pattern:
        return 0
    m, n = len(pattern), len(text)
    if m > n:
        return -1

    BASE, MOD = 256, 10**9 + 7

    pattern_hash = window_hash = 0
    power = 1

    for i in range(m):
        pattern_hash = (pattern_hash * BASE + ord(pattern[i])) % MOD
        window_hash = (window_hash * BASE + ord(text[i])) % MOD
        if i < m - 1:
            power = (power * BASE) % MOD

    for i in range(n - m + 1):
        if pattern_hash == window_hash and text[i:i+m] == pattern:
            return i

        if i < n - m:
            window_hash = ((window_hash - ord(text[i]) * power) * BASE
                          + ord(text[i + m])) % MOD
            window_hash = (window_hash + MOD) % MOD

    return -1
```

**Use for**: LC 28 (alternative), multiple pattern search

---

### 10.4 Template 4: String Period Check

```python
def is_periodic(s: str) -> bool:
    """
    Check if string is built from repeated substrings.
    Time: O(n), Space: O(n)
    """
    n = len(s)
    if n <= 1:
        return False

    failure = build_failure(s)
    period = n - failure[-1]

    return failure[-1] > 0 and n % period == 0
```

**Use for**: LC 459

---

### 10.5 Template 5: Longest Prefix = Suffix

```python
def longest_happy_prefix(s: str) -> str:
    """
    Find longest proper prefix that is also suffix.
    Time: O(n), Space: O(n)
    """
    if len(s) <= 1:
        return ""

    failure = build_failure(s)
    return s[:failure[-1]]
```

**Use for**: LC 1392

---

## 11. Quick Reference

| Problem Type | Template | Key Line |
|-------------|----------|----------|
| Pattern search | Template 2 | Return on `pattern_idx == len(pattern)` |
| Period check | Template 4 | `n % (n - failure[-1]) == 0` |
| Prefix=suffix | Template 5 | Return `s[:failure[-1]]` |
| Palindrome prefix | Use concat `s + '#' + rev(s)` | failure[-1] of concat |



---



*Document generated for NeetCode Practice Framework — API Kernel: StringMatching*
