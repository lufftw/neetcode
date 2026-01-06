# String DP Pattern

## Table of Contents

1. [API Kernel: `StringDP`](#1-api-kernel-stringdp)
2. [Why String DP?](#2-why-string-dp)
3. [Core Insight](#3-core-insight)
4. [Universal Template Structure](#4-universal-template-structure)
5. [Pattern Variants](#5-pattern-variants)
6. [Problem Link](#6-problem-link)
7. [Difficulty](#7-difficulty)
8. [Tags](#8-tags)
9. [Pattern](#9-pattern)
10. [API Kernel](#10-api-kernel)
11. [Problem Summary](#11-problem-summary)
12. [Key Insight](#12-key-insight)
13. [Template Mapping](#13-template-mapping)
14. [Complexity](#14-complexity)
15. [Why This Problem First?](#15-why-this-problem-first)
16. [Common Mistakes](#16-common-mistakes)
17. [Related Problems](#17-related-problems)
18. [Problem Link](#18-problem-link)
19. [Difficulty](#19-difficulty)
20. [Tags](#20-tags)
21. [Pattern](#21-pattern)
22. [API Kernel](#22-api-kernel)
23. [Problem Summary](#23-problem-summary)
24. [Key Insight](#24-key-insight)
25. [Template Mapping](#25-template-mapping)
26. [Complexity](#26-complexity)
27. [Why This Problem Second?](#27-why-this-problem-second)
28. [Common Mistakes](#28-common-mistakes)
29. [Related Problems](#29-related-problems)
30. [Problem Link](#30-problem-link)
31. [Difficulty](#31-difficulty)
32. [Tags](#32-tags)
33. [Pattern](#33-pattern)
34. [API Kernel](#34-api-kernel)
35. [Problem Summary](#35-problem-summary)
36. [Key Insight](#36-key-insight)
37. [Template Mapping](#37-template-mapping)
38. [Complexity](#38-complexity)
39. [Why This Problem Third?](#39-why-this-problem-third)
40. [Common Mistakes](#40-common-mistakes)
41. [Related Problems](#41-related-problems)
42. [Problem Link](#42-problem-link)
43. [Difficulty](#43-difficulty)
44. [Tags](#44-tags)
45. [Pattern](#45-pattern)
46. [API Kernel](#46-api-kernel)
47. [Problem Summary](#47-problem-summary)
48. [Key Insight](#48-key-insight)
49. [Template Mapping](#49-template-mapping)
50. [Complexity](#50-complexity)
51. [Why This Problem Fourth?](#51-why-this-problem-fourth)
52. [Common Mistakes](#52-common-mistakes)
53. [Related Problems](#53-related-problems)
54. [Problem Comparison](#54-problem-comparison)
55. [Pattern Evolution](#55-pattern-evolution)
56. [Key Differences](#56-key-differences)
57. [Decision Tree](#57-decision-tree)
58. [Pattern Selection Guide](#58-pattern-selection-guide)
59. [Problem Type Recognition](#59-problem-type-recognition)
60. [Complexity Guide](#60-complexity-guide)
61. [Universal Templates](#61-universal-templates)
62. [Quick Reference](#62-quick-reference)

---

## 1. API Kernel: `StringDP`

> **Core Mechanism**: Use 2D DP table where `dp[i][j]` represents the optimal result for substrings `s[0:i]` and `t[0:j]`.

## 2. Why String DP?

String DP solves problems where:
- You need to compare, align, or match two strings
- The answer depends on subsequences or substrings of both strings
- Optimal substructure exists between prefixes of the strings

## 3. Core Insight

The key insight is that comparing two strings of lengths `m` and `n` can be broken into subproblems comparing their prefixes. The state `dp[i][j]` depends on:
- `dp[i-1][j-1]` - both strings shrink by one character
- `dp[i-1][j]` - only the first string shrinks
- `dp[i][j-1]` - only the second string shrinks

This creates a systematic way to build up the answer from smaller subproblems.

## 4. Universal Template Structure

```python
def string_dp_template(s: str, t: str) -> int:
    m, n = len(s), len(t)

    # dp[i][j] = result for s[0:i] and t[0:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases: empty strings
    for i in range(m + 1):
        dp[i][0] = base_case_first_string(i)
    for j in range(n + 1):
        dp[0][j] = base_case_second_string(j)

    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i-1] == t[j-1]:
                dp[i][j] = match_transition(dp[i-1][j-1])
            else:
                dp[i][j] = mismatch_transition(dp[i-1][j-1], dp[i-1][j], dp[i][j-1])

    return dp[m][n]
```

## 5. Pattern Variants

| Pattern | State | Transition | Example |
|---------|-------|------------|---------|
| **LCS** | Length of LCS for prefixes | Match: `+1`, Mismatch: `max(left, up)` | LC 1143 |
| **Edit Distance** | Min edits to transform | Match: `same`, Mismatch: `1 + min(3 ops)` | LC 72 |
| **Palindrome** | LCS(s, reverse(s)) | Same as LCS | LC 516 |
| **Regex Match** | Boolean: can match? | Complex transitions based on pattern | LC 10 |

---

# 1143. Longest Common Subsequence

## 6. Problem Link
https://leetcode.com/problems/longest-common-subsequence/

## 7. Difficulty
Medium

## 8. Tags
- String
- Dynamic Programming

## 9. Pattern
String DP - LCS (Longest Common Subsequence)

## 10. API Kernel
`StringDP`

## 11. Problem Summary
Given two strings `text1` and `text2`, return the length of their longest common subsequence. A subsequence is a sequence that can be derived from another sequence by deleting some or no elements without changing the order of the remaining elements.

## 12. Key Insight

The LCS problem has optimal substructure:
- If the last characters match: `LCS(s[0:i], t[0:j]) = 1 + LCS(s[0:i-1], t[0:j-1])`
- If they don't match: `LCS(s[0:i], t[0:j]) = max(LCS(s[0:i-1], t[0:j]), LCS(s[0:i], t[0:j-1]))`

When characters match, we include them in the LCS. When they don't, we try excluding one character from either string.

## 13. Template Mapping

```python
def longestCommonSubsequence(text1: str, text2: str) -> int:
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[m][n]
```

## 14. Complexity
- Time: O(m * n) where m, n are lengths of the two strings
- Space: O(m * n), can be optimized to O(min(m, n))

## 15. Why This Problem First?

LCS is the **canonical** String DP problem:
1. Simple state definition: `dp[i][j]` = LCS length for prefixes
2. Clean transitions: match adds 1, mismatch takes max
3. No complex base cases
4. Foundation for all other String DP variants

## 16. Common Mistakes

1. **Off-by-one errors** - Remember `dp[i][j]` corresponds to `s[0:i]` and `t[0:j]`, so access `s[i-1]` and `t[j-1]`
2. **Forgetting base cases** - First row and column are implicitly 0 (empty string has LCS 0)
3. **Wrong transition for mismatch** - Must take max of two options, not three

## 17. Related Problems
- LC 516: Longest Palindromic Subsequence (LCS with reversed string)
- LC 583: Delete Operation for Two Strings (Uses LCS)
- LC 1092: Shortest Common Supersequence (Build string from LCS)

---

# 72. Edit Distance

## 18. Problem Link
https://leetcode.com/problems/edit-distance/

## 19. Difficulty
Medium

## 20. Tags
- String
- Dynamic Programming

## 21. Pattern
String DP - Edit Distance (Levenshtein Distance)

## 22. API Kernel
`StringDP`

## 23. Problem Summary
Given two strings `word1` and `word2`, return the minimum number of operations required to convert `word1` to `word2`. You can perform three operations: insert a character, delete a character, or replace a character.

## 24. Key Insight

Edit distance has optimal substructure with three operations:
- **Insert**: `dp[i][j] = dp[i][j-1] + 1` (insert `word2[j-1]` at end of `word1[0:i]`)
- **Delete**: `dp[i][j] = dp[i-1][j] + 1` (delete `word1[i-1]`)
- **Replace**: `dp[i][j] = dp[i-1][j-1] + 1` (replace `word1[i-1]` with `word2[j-1]`)

If characters match, no operation needed: `dp[i][j] = dp[i-1][j-1]`.

## 25. Template Mapping

```python
def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases: transform to/from empty string
    for i in range(m + 1):
        dp[i][0] = i  # Delete all characters
    for j in range(n + 1):
        dp[0][j] = j  # Insert all characters

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]  # No operation
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j-1],  # Replace
                    dp[i-1][j],    # Delete
                    dp[i][j-1]     # Insert
                )

    return dp[m][n]
```

## 26. Complexity
- Time: O(m * n)
- Space: O(m * n), can be optimized to O(min(m, n))

## 27. Why This Problem Second?

Edit Distance builds on LCS:
1. Same 2D state structure
2. Adds meaningful base cases (not just 0)
3. Introduces operation counting instead of length
4. Three transitions instead of two

## 28. Common Mistakes

1. **Forgetting base cases** - Empty string requires `i` deletions or `j` insertions
2. **Wrong transition direction** - Insert adds to `word1`, so look at `dp[i][j-1]`
3. **Not checking equality first** - Always check if characters match before operations

## 29. Related Problems
- LC 583: Delete Operation for Two Strings (Edit distance with only deletes)
- LC 712: Minimum ASCII Delete Sum (Edit distance with ASCII cost)
- LC 161: One Edit Distance (Special case)

---

# 516. Longest Palindromic Subsequence

## 30. Problem Link
https://leetcode.com/problems/longest-palindromic-subsequence/

## 31. Difficulty
Medium

## 32. Tags
- String
- Dynamic Programming

## 33. Pattern
String DP - Palindrome via LCS

## 34. API Kernel
`StringDP`

## 35. Problem Summary
Given a string `s`, find the longest palindromic subsequence's length in `s`. A subsequence is a sequence that can be derived from another sequence by deleting some or no elements without changing the order of the remaining elements.

## 36. Key Insight

A palindrome reads the same forwards and backwards. The **longest palindromic subsequence** is exactly the **LCS of `s` and `reverse(s)`**.

Why? Any common subsequence between `s` and its reverse must be a palindrome (it appears in both forward and backward directions).

Alternative: Direct interval DP approach where `dp[i][j]` = LPS of `s[i:j+1]`.

## 37. Template Mapping

```python
# Approach 1: LCS with reversed string
def longestPalindromeSubseq(s: str) -> int:
    n = len(s)
    t = s[::-1]
    dp = [[0] * (n + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[n][n]


# Approach 2: Interval DP
def longestPalindromeSubseq_interval(s: str) -> int:
    n = len(s)
    dp = [[0] * n for _ in range(n)]

    for i in range(n):
        dp[i][i] = 1  # Single character

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = dp[i+1][j-1] + 2
            else:
                dp[i][j] = max(dp[i+1][j], dp[i][j-1])

    return dp[0][n-1]
```

## 38. Complexity
- Time: O(n^2)
- Space: O(n^2), can be optimized to O(n)

## 39. Why This Problem Third?

LPS shows how LCS generalizes:
1. Demonstrates reduction technique (LPS -> LCS)
2. Introduces interval DP as an alternative
3. Bridge between String DP and Interval DP patterns

## 40. Common Mistakes

1. **Forgetting that LCS works** - Many try complex approaches when LCS with reverse is simpler
2. **Interval DP order** - Must fill by increasing length, not by row
3. **Base case for interval** - Single characters have LPS = 1

## 41. Related Problems
- LC 5: Longest Palindromic Substring (Contiguous, not subsequence)
- LC 647: Palindromic Substrings (Count all palindromic substrings)
- LC 1312: Minimum Insertion Steps (Make string palindrome)

---

# 10. Regular Expression Matching

## 42. Problem Link
https://leetcode.com/problems/regular-expression-matching/

## 43. Difficulty
Hard

## 44. Tags
- String
- Dynamic Programming
- Recursion

## 45. Pattern
String DP - Regex Matching

## 46. API Kernel
`StringDP`

## 47. Problem Summary
Given an input string `s` and a pattern `p`, implement regular expression matching with support for `.` (matches any single character) and `*` (matches zero or more of the preceding element).

## 48. Key Insight

The key is handling `*` correctly:
- `*` means "zero or more of the previous character"
- For pattern `a*`, we can either:
  1. Use zero `a`s: skip `a*` entirely, check `dp[i][j-2]`
  2. Use one+ `a`s: if `s[i-1]` matches `a`, check `dp[i-1][j]`

The `.` wildcard just matches any character.

## 49. Template Mapping

```python
def isMatch(s: str, p: str) -> bool:
    m, n = len(s), len(p)

    # dp[i][j] = True if s[0:i] matches p[0:j]
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True  # Empty matches empty

    # Base case: empty string can match patterns like a*, a*b*, etc.
    for j in range(2, n + 1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-2]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j-1] == '*':
                # Option 1: Use zero of preceding element
                dp[i][j] = dp[i][j-2]

                # Option 2: Use one or more (if current char matches)
                if p[j-2] == '.' or p[j-2] == s[i-1]:
                    dp[i][j] = dp[i][j] or dp[i-1][j]
            elif p[j-1] == '.' or p[j-1] == s[i-1]:
                # Direct match or wildcard
                dp[i][j] = dp[i-1][j-1]

    return dp[m][n]
```

## 50. Complexity
- Time: O(m * n)
- Space: O(m * n)

## 51. Why This Problem Fourth?

Regex Matching is the capstone problem:
1. Complex transitions with multiple cases
2. Non-trivial base cases (empty string matching `a*b*`)
3. Requires careful handling of `*` looking back at `j-2`
4. Tests complete mastery of String DP

## 52. Common Mistakes

1. **Handling `*` incorrectly** - Must look at `p[j-2]` (the character before `*`)
2. **Base case for `*` patterns** - Empty string can match `a*`, `a*b*`, etc.
3. **Order of checks** - Must check for `*` first, then normal match
4. **Off-by-one with `*`** - When checking zero occurrences, use `dp[i][j-2]`, not `dp[i][j-1]`

## 53. Related Problems
- LC 44: Wildcard Matching (Similar but `*` matches any sequence)
- LC 115: Distinct Subsequences (Count matching subsequences)
- LC 97: Interleaving String (Another complex String DP)

---

## 54. Problem Comparison

| Problem | Core Pattern | State `dp[i][j]` | Match Transition | Mismatch Transition |
|---------|-------------|------------------|------------------|---------------------|
| **LC 1143 LCS** | Find longest common | Length of LCS | `dp[i-1][j-1] + 1` | `max(dp[i-1][j], dp[i][j-1])` |
| **LC 72 Edit Distance** | Min operations | Min edits needed | `dp[i-1][j-1]` | `1 + min(3 options)` |
| **LC 516 Palindrome** | LCS with reverse | Length of LPS | Same as LCS | Same as LCS |
| **LC 10 Regex** | Pattern matching | Boolean: matches? | `dp[i-1][j-1]` | `False` (unless `*`) |

## 55. Pattern Evolution

```
LC 1143 LCS (Base)
    │
    │ Add operation counting
    │ Add non-zero base cases
    ↓
LC 72 Edit Distance
    │
    │ Apply to single string
    │ s vs reverse(s)
    ↓
LC 516 Palindrome Subsequence
    │
    │ Add complex pattern matching
    │ Handle . and * wildcards
    ↓
LC 10 Regex Matching
```

## 56. Key Differences

### 56.1 Base Cases

| Problem | `dp[i][0]` | `dp[0][j]` |
|---------|-----------|-----------|
| LCS | 0 | 0 |
| Edit Distance | `i` | `j` |
| Palindrome | 0 | 0 |
| Regex | `False` | `True` if `p[0:j]` is all `x*` patterns |

### 56.2 Optimization Potential

| Problem | Space Optimization | Notes |
|---------|-------------------|-------|
| LCS | O(min(m,n)) | Only need previous row |
| Edit Distance | O(min(m,n)) | Only need previous row |
| Palindrome | O(n) | Single row for LCS approach |
| Regex | O(n) | Only need previous row |

---

## 57. Decision Tree

```
Start: Two strings to compare/transform?
            │
            ▼
    ┌───────────────────┐
    │ What's the goal?  │
    └───────────────────┘
            │
    ┌───────┼───────┬───────────┐
    ▼       ▼       ▼           ▼
Find      Count   Match      Transform
common    edits   pattern    one string
chars               │
    │       │       │           │
    ▼       ▼       ▼           ▼
  LCS    Edit     Regex      Edit
         Dist.   Matching   Distance
```

## 58. Pattern Selection Guide

### 58.1 Use LCS (LC 1143) when:
- Finding common elements between two sequences
- Subsequence (not substring) problems
- Building longest/shortest common supersequence

### 58.2 Use Edit Distance (LC 72) when:
- Converting one string to another
- Counting minimum operations
- Operations: insert, delete, replace

### 58.3 Use Palindrome DP (LC 516) when:
- Finding palindromic subsequences
- Single string problems
- Can reduce to LCS with reversed string

### 58.4 Use Regex Matching (LC 10) when:
- Pattern has wildcards (`.`, `*`)
- Boolean matching result
- Complex pattern rules

## 59. Problem Type Recognition

| Keywords/Clues | Pattern |
|----------------|---------|
| "longest common subsequence" | LCS |
| "minimum operations to convert" | Edit Distance |
| "palindrome subsequence" | LCS with reverse |
| "pattern matching with wildcards" | Regex/Wildcard DP |
| "delete operations for two strings" | LCS-based |

## 60. Complexity Guide

| Pattern | Time | Space | Space-Optimized |
|---------|------|-------|-----------------|
| LCS | O(mn) | O(mn) | O(min(m,n)) |
| Edit Distance | O(mn) | O(mn) | O(min(m,n)) |
| Palindrome | O(n²) | O(n²) | O(n) |
| Regex | O(mn) | O(mn) | O(n) |

---

## 61. Universal Templates

### 61.1 Template 1: Longest Common Subsequence (LCS)

```python
def lcs(s: str, t: str) -> int:
    """
    Find the length of the longest common subsequence.
    Time: O(m*n), Space: O(m*n)
    """
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[m][n]
```

**Use for**: LC 1143, LC 516 (with reverse), LC 583, LC 1092

---

### 61.2 Template 2: Edit Distance

```python
def edit_distance(s: str, t: str) -> int:
    """
    Find minimum operations to convert s to t.
    Operations: insert, delete, replace.
    Time: O(m*n), Space: O(m*n)
    """
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j-1],  # replace
                    dp[i-1][j],    # delete
                    dp[i][j-1]     # insert
                )

    return dp[m][n]
```

**Use for**: LC 72, LC 161, LC 583 (variation)

---

### 61.3 Template 3: Regex/Pattern Matching

```python
def regex_match(s: str, p: str) -> bool:
    """
    Match string s against pattern p with . and * wildcards.
    Time: O(m*n), Space: O(m*n)
    """
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True

    # Handle patterns like a*, a*b*, etc. matching empty string
    for j in range(2, n + 1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-2]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j-1] == '*':
                # Zero occurrences of preceding char
                dp[i][j] = dp[i][j-2]
                # One or more if matching
                if p[j-2] == '.' or p[j-2] == s[i-1]:
                    dp[i][j] = dp[i][j] or dp[i-1][j]
            elif p[j-1] == '.' or p[j-1] == s[i-1]:
                dp[i][j] = dp[i-1][j-1]

    return dp[m][n]
```

**Use for**: LC 10, LC 44 (variation)

---

### 61.4 Template 4: Space-Optimized LCS

```python
def lcs_optimized(s: str, t: str) -> int:
    """
    Space-optimized LCS using O(n) space.
    Time: O(m*n), Space: O(min(m,n))
    """
    if len(s) < len(t):
        s, t = t, s
    m, n = len(s), len(t)

    prev = [0] * (n + 1)
    curr = [0] * (n + 1)

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i-1] == t[j-1]:
                curr[j] = prev[j-1] + 1
            else:
                curr[j] = max(prev[j], curr[j-1])
        prev, curr = curr, prev

    return prev[n]
```

**Use for**: LC 1143, LC 516 when space is critical

---

## 62. Quick Reference

| Problem Type | Template | Key Transition |
|-------------|----------|----------------|
| Common subsequence | Template 1 | `max(left, up)` |
| String transformation | Template 2 | `1 + min(3 ops)` |
| Pattern matching | Template 3 | Handle `*` specially |
| Space-critical | Template 4 | Rolling array |



---



*Document generated for NeetCode Practice Framework — API Kernel: string_dp*
