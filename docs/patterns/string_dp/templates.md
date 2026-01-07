# String DP Patterns: Complete Reference

> **API Kernel**: `StringDP`
> **Core Mechanism**: Two-dimensional state transition over string pairs, where `dp[i][j]` represents the optimal solution for prefixes `s[0:i]` and `t[0:j]`.

This document presents the **canonical String DP templates** and all major variations. String DP is fundamentally different from linear DP (1D sequences) or knapsack DP (subset selection) — it focuses on **pairwise string comparison** with a 2D state space.

---

## Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Base Template: Longest Common Subsequence (LeetCode 1143)](#2-base-template-longest-common-subsequence-leetcode-1143)
3. [Variant: Edit Distance (LeetCode 72)](#3-variant-edit-distance-leetcode-72)
4. [Variant: Longest Palindromic Subsequence (LeetCode 516)](#4-variant-longest-palindromic-subsequence-leetcode-516)
5. [Advanced: Regular Expression Matching (LeetCode 10)](#5-advanced-regular-expression-matching-leetcode-10)
6. [Advanced: Wildcard Matching (LeetCode 44)](#6-advanced-wildcard-matching-leetcode-44)
7. [Pattern Comparison Table](#7-pattern-comparison-table)
8. [Decision Tree](#8-decision-tree)
9. [Pattern Selection Guide](#9-pattern-selection-guide)
10. [Problem Type Recognition](#10-problem-type-recognition)
11. [Complexity Guide](#11-complexity-guide)
12. [LeetCode Problem Mapping](#12-leetcode-problem-mapping)
13. [Universal Templates](#13-universal-templates)
14. [Quick Reference](#14-quick-reference)

---

## 1. Core Concepts

### 1.1 The String DP State Space

Every String DP problem operates on a 2D state table where rows and columns represent prefixes of two strings:

```
String DP State Table:
        ""   t[0]  t[1]  t[2]  ...  t[n-1]
    ┌────┬────┬────┬────┬────┬────┬────┐
 "" │ 0  │    │    │    │    │    │    │
    ├────┼────┼────┼────┼────┼────┼────┤
s[0]│    │ ↖  │ ←  │    │    │    │    │
    ├────┼────┼────┼────┼────┼────┼────┤
s[1]│    │ ↑  │ ↖↑←│    │    │    │    │
    ├────┼────┼────┼────┼────┼────┼────┤
... │    │    │    │    │    │    │    │
    ├────┼────┼────┼────┼────┼────┼────┤
s[m]│    │    │    │    │    │    │ ANS│
    └────┴────┴────┴────┴────┴────┴────┘

Transition Directions:
↖ = match/substitute (diagonal)
← = operation on string t (horizontal)
↑ = operation on string s (vertical)
```

### 1.2 Universal Template Structure

```python
def string_dp_template(s: str, t: str) -> int:
    """
    Generic String DP template.

    Key components:
    1. State: dp[i][j] = solution for s[0:i] and t[0:j]
    2. Base Case: Initialize dp[0][*] and dp[*][0]
    3. Transition: Define how dp[i][j] relates to dp[i-1][j-1], dp[i-1][j], dp[i][j-1]
    4. Answer: Usually dp[m][n] where m, n are string lengths
    """
    m, n = len(s), len(t)

    # State table with (m+1) x (n+1) dimensions for empty string handling
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # BASE CASE: Initialize first row and column
    for i in range(m + 1):
        dp[i][0] = base_case_s(i)
    for j in range(n + 1):
        dp[0][j] = base_case_t(j)

    # TRANSITION: Fill table row by row
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i - 1] == t[j - 1]:
                # Characters match: inherit from diagonal
                dp[i][j] = match_transition(dp[i - 1][j - 1])
            else:
                # Characters differ: combine from all directions
                dp[i][j] = mismatch_transition(
                    dp[i - 1][j - 1],  # diagonal (substitute)
                    dp[i - 1][j],      # up (operation on s)
                    dp[i][j - 1]       # left (operation on t)
                )

    return dp[m][n]
```

### 1.3 Three Fundamental Transition Patterns

| Pattern | Direction | Meaning | Example |
|---------|-----------|---------|---------|
| **Match/Substitute** | ↖ Diagonal | Characters align or are replaced | LCS, Edit Distance |
| **Skip String S** | ↑ Vertical | Skip current char in s | LCS (no match), Regex `*` |
| **Skip String T** | ← Horizontal | Skip current char in t | Edit Distance (insert) |

### 1.4 Space Optimization

Since `dp[i][j]` only depends on `dp[i-1][*]` and `dp[i][j-1]`, we can reduce space from O(mn) to O(n):

```python
def string_dp_space_optimized(s: str, t: str) -> int:
    m, n = len(s), len(t)

    # Only keep current and previous row
    prev = [base_case_t(j) for j in range(n + 1)]
    curr = [0] * (n + 1)

    for i in range(1, m + 1):
        curr[0] = base_case_s(i)
        for j in range(1, n + 1):
            if s[i - 1] == t[j - 1]:
                curr[j] = match_transition(prev[j - 1])
            else:
                curr[j] = mismatch_transition(prev[j - 1], prev[j], curr[j - 1])
        prev, curr = curr, prev

    return prev[n]
```

---

## 2. Base Template: Longest Common Subsequence (LeetCode 1143)

> **Problem**: Given two strings `text1` and `text2`, return the length of their longest common subsequence.
> **Invariant**: `dp[i][j]` = length of LCS for `text1[0:i]` and `text2[0:j]`.
> **Role**: BASE TEMPLATE for `StringDP` API Kernel.

### 2.1 Why This Is The Base Template

LCS is the purest form of String DP:
- **No modification operations**: Just match or skip
- **Two clear choices**: Match (diagonal) or skip one string (up/left)
- **Maximum objective**: Maximize common length

Every other String DP problem builds on this foundation by adding operations (edit distance) or constraints (regex).

### 2.2 State Transition Logic

```
If text1[i-1] == text2[j-1]:
    dp[i][j] = dp[i-1][j-1] + 1     // Match: extend LCS by 1
Else:
    dp[i][j] = max(dp[i-1][j],      // Skip char in text1
                   dp[i][j-1])       // Skip char in text2
```

### 2.3 Implementation

```python
class SolutionLCS:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        """
        Find the longest common subsequence of two strings.

        Algorithm:
        - Build 2D DP table where dp[i][j] = LCS length for text1[0:i], text2[0:j]
        - When characters match: extend LCS from diagonal
        - When they don't: take best of skipping either character

        Time: O(m * n) where m, n are string lengths
        Space: O(m * n), can be optimized to O(min(m, n))
        """
        string_length_1, string_length_2 = len(text1), len(text2)

        # dp[i][j] = LCS length for text1[0:i] and text2[0:j]
        # Extra row/column for empty string base cases
        lcs_table: list[list[int]] = [
            [0] * (string_length_2 + 1)
            for _ in range(string_length_1 + 1)
        ]

        # Base case: LCS with empty string is 0 (already initialized)

        # Fill table: compare each character pair
        for idx_1 in range(1, string_length_1 + 1):
            for idx_2 in range(1, string_length_2 + 1):
                char_1 = text1[idx_1 - 1]
                char_2 = text2[idx_2 - 1]

                if char_1 == char_2:
                    # Characters match: extend LCS from previous diagonal
                    lcs_table[idx_1][idx_2] = lcs_table[idx_1 - 1][idx_2 - 1] + 1
                else:
                    # No match: take best of skipping either character
                    skip_from_text1 = lcs_table[idx_1 - 1][idx_2]
                    skip_from_text2 = lcs_table[idx_1][idx_2 - 1]
                    lcs_table[idx_1][idx_2] = max(skip_from_text1, skip_from_text2)

        return lcs_table[string_length_1][string_length_2]
```

### 2.4 Space-Optimized Implementation

```python
class SolutionLCSOptimized:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        """
        Space-optimized LCS using two rows instead of full table.

        Key insight: Each cell only depends on:
        - Previous row, same column (up)
        - Same row, previous column (left)
        - Previous row, previous column (diagonal)

        Time: O(m * n)
        Space: O(min(m, n))
        """
        # Ensure text2 is the shorter string for space optimization
        if len(text1) < len(text2):
            text1, text2 = text2, text1

        string_length_2 = len(text2)

        # Only need previous row and current row
        previous_row: list[int] = [0] * (string_length_2 + 1)
        current_row: list[int] = [0] * (string_length_2 + 1)

        for idx_1, char_1 in enumerate(text1, 1):
            for idx_2, char_2 in enumerate(text2, 1):
                if char_1 == char_2:
                    # Match: extend from diagonal (previous row, previous column)
                    current_row[idx_2] = previous_row[idx_2 - 1] + 1
                else:
                    # No match: max of up (previous row) and left (current row)
                    current_row[idx_2] = max(previous_row[idx_2], current_row[idx_2 - 1])

            # Swap rows for next iteration
            previous_row, current_row = current_row, previous_row

        return previous_row[string_length_2]
```

### 2.5 Trace Example

```
text1 = "abcde", text2 = "ace"

DP Table:
        ""   a    c    e
    ┌────┬────┬────┬────┐
 "" │ 0  │ 0  │ 0  │ 0  │
    ├────┼────┼────┼────┤
 a  │ 0  │ 1  │ 1  │ 1  │  ← 'a' matches
    ├────┼────┼────┼────┤
 b  │ 0  │ 1  │ 1  │ 1  │  ← 'b' doesn't match, carry max
    ├────┼────┼────┼────┤
 c  │ 0  │ 1  │ 2  │ 2  │  ← 'c' matches
    ├────┼────┼────┼────┤
 d  │ 0  │ 1  │ 2  │ 2  │  ← 'd' doesn't match
    ├────┼────┼────┼────┤
 e  │ 0  │ 1  │ 2  │ 3  │  ← 'e' matches
    └────┴────┴────┴────┘

Answer: dp[5][3] = 3 (LCS is "ace")
```

### 2.6 Key Insights

1. **Subsequence vs Substring**: Subsequence allows skipping; substring must be contiguous
2. **Optimal Substructure**: LCS of two strings depends on LCS of their prefixes
3. **No Greedy Solution**: Must consider all possibilities via DP
4. **Reconstruction**: Can trace back through table to find actual LCS string

---

## 3. Variant: Edit Distance (LeetCode 72)

> **Problem**: Given two strings `word1` and `word2`, return the minimum number of operations to convert `word1` to `word2`. Operations: insert, delete, replace.
> **Invariant**: `dp[i][j]` = minimum edit distance for `word1[0:i]` and `word2[0:j]`.
> **Delta from Base**: Add three edit operations instead of just match/skip.

### 3.1 How This Differs From LCS

| Aspect | LCS | Edit Distance |
|--------|-----|---------------|
| Objective | Maximize matches | Minimize operations |
| Operations | Match, Skip | Insert, Delete, Replace |
| Base Case | 0 (empty = no match) | Length (need all inserts/deletes) |
| Transition | max() | min() + 1 |

### 3.2 State Transition Logic

```
If word1[i-1] == word2[j-1]:
    dp[i][j] = dp[i-1][j-1]         // Match: no operation needed
Else:
    dp[i][j] = 1 + min(
        dp[i-1][j-1],               // Replace word1[i-1] with word2[j-1]
        dp[i-1][j],                 // Delete word1[i-1]
        dp[i][j-1]                  // Insert word2[j-1]
    )
```

### 3.3 Implementation

```python
class SolutionEditDistance:
    def minDistance(self, word1: str, word2: str) -> int:
        """
        Calculate minimum edit distance (Levenshtein distance) between two strings.

        The three operations and their DP transitions:
        - Replace: dp[i-1][j-1] + 1 (transform word1[i-1] to word2[j-1])
        - Delete:  dp[i-1][j] + 1   (remove word1[i-1])
        - Insert:  dp[i][j-1] + 1   (add word2[j-1] to word1)

        Time: O(m * n)
        Space: O(m * n), can be optimized to O(n)
        """
        source_length = len(word1)
        target_length = len(word2)

        # dp[i][j] = min operations to convert word1[0:i] to word2[0:j]
        edit_distance: list[list[int]] = [
            [0] * (target_length + 1)
            for _ in range(source_length + 1)
        ]

        # Base case: converting to/from empty string
        # Empty -> word2[0:j] requires j insertions
        for j in range(target_length + 1):
            edit_distance[0][j] = j

        # word1[0:i] -> empty requires i deletions
        for i in range(source_length + 1):
            edit_distance[i][0] = i

        # Fill table with minimum operations
        for i in range(1, source_length + 1):
            for j in range(1, target_length + 1):
                source_char = word1[i - 1]
                target_char = word2[j - 1]

                if source_char == target_char:
                    # Characters match: no operation needed
                    edit_distance[i][j] = edit_distance[i - 1][j - 1]
                else:
                    # Take minimum of three operations
                    replace_cost = edit_distance[i - 1][j - 1] + 1
                    delete_cost = edit_distance[i - 1][j] + 1
                    insert_cost = edit_distance[i][j - 1] + 1

                    edit_distance[i][j] = min(replace_cost, delete_cost, insert_cost)

        return edit_distance[source_length][target_length]
```

### 3.4 Space-Optimized Implementation

```python
class SolutionEditDistanceOptimized:
    def minDistance(self, word1: str, word2: str) -> int:
        """
        Space-optimized edit distance using single row + diagonal variable.

        Tricky part: We need dp[i-1][j-1] (diagonal) but we're overwriting it.
        Solution: Save diagonal before overwriting.

        Time: O(m * n)
        Space: O(n)
        """
        source_length = len(word1)
        target_length = len(word2)

        # Previous row: represents dp[i-1][*]
        previous_row: list[int] = list(range(target_length + 1))

        for i in range(1, source_length + 1):
            # Save dp[i-1][0] before overwriting (needed for diagonal)
            diagonal = previous_row[0]
            previous_row[0] = i  # Base case: i deletions

            for j in range(1, target_length + 1):
                # Save current value (will be diagonal for next iteration)
                next_diagonal = previous_row[j]

                if word1[i - 1] == word2[j - 1]:
                    previous_row[j] = diagonal
                else:
                    previous_row[j] = 1 + min(
                        diagonal,           # replace
                        previous_row[j],    # delete (was dp[i-1][j])
                        previous_row[j - 1] # insert
                    )

                diagonal = next_diagonal

        return previous_row[target_length]
```

### 3.5 Trace Example

```
word1 = "horse", word2 = "ros"

DP Table:
        ""   r    o    s
    ┌────┬────┬────┬────┐
 "" │ 0  │ 1  │ 2  │ 3  │  ← insertions needed
    ├────┼────┼────┼────┤
 h  │ 1  │ 1  │ 2  │ 3  │  ← replace h->r
    ├────┼────┼────┼────┤
 o  │ 2  │ 2  │ 1  │ 2  │  ← 'o' matches
    ├────┼────┼────┼────┤
 r  │ 3  │ 2  │ 2  │ 2  │  ← 'r' matches (but different position)
    ├────┼────┼────┼────┤
 s  │ 4  │ 3  │ 3  │ 2  │  ← 's' matches
    ├────┼────┼────┼────┤
 e  │ 5  │ 4  │ 4  │ 3  │  ← delete 'e'
    └────┴────┴────┴────┘

Answer: dp[5][3] = 3
Operations: horse -> rorse (replace 'h') -> rose (delete 'r') -> ros (delete 'e')
```

### 3.6 Key Insights

1. **Symmetric**: edit_distance(a, b) == edit_distance(b, a)
2. **Triangle Inequality**: edit_distance(a, c) <= edit_distance(a, b) + edit_distance(b, c)
3. **Applications**: Spell checking, DNA alignment, plagiarism detection
4. **Variants**: Weighted operations, only certain operations allowed

---

## 4. Variant: Longest Palindromic Subsequence (LeetCode 516)

> **Problem**: Given a string `s`, find the longest palindromic subsequence's length in `s`.
> **Invariant**: `dp[i][j]` = length of longest palindromic subsequence in `s[i:j+1]`.
> **Delta from Base**: Compare string with its reverse, or use interval DP on single string.

### 4.1 Two Approaches

1. **LCS Approach**: LPS(s) = LCS(s, reverse(s))
2. **Interval DP Approach**: Direct computation on substring intervals

### 4.2 Approach 1: Reduce to LCS

```python
class SolutionLPSviaLCS:
    def longestPalindromeSubseq(self, s: str) -> int:
        """
        Reduce to LCS: Longest palindromic subsequence equals
        LCS of string with its reverse.

        Intuition: A palindrome reads the same forward and backward.
        The common subsequence of s and reverse(s) is palindromic.

        Time: O(n^2)
        Space: O(n)
        """
        reversed_string = s[::-1]
        string_length = len(s)

        # Space-optimized LCS
        previous_row: list[int] = [0] * (string_length + 1)

        for idx_original in range(1, string_length + 1):
            current_row: list[int] = [0] * (string_length + 1)
            for idx_reversed in range(1, string_length + 1):
                if s[idx_original - 1] == reversed_string[idx_reversed - 1]:
                    current_row[idx_reversed] = previous_row[idx_reversed - 1] + 1
                else:
                    current_row[idx_reversed] = max(
                        previous_row[idx_reversed],
                        current_row[idx_reversed - 1]
                    )
            previous_row = current_row

        return previous_row[string_length]
```

### 4.3 Approach 2: Interval DP (Direct)

```python
class SolutionLPSInterval:
    def longestPalindromeSubseq(self, s: str) -> int:
        """
        Direct interval DP approach.

        State: dp[i][j] = LPS length for substring s[i:j+1]
        Transition:
        - If s[i] == s[j]: dp[i][j] = dp[i+1][j-1] + 2
        - Else: dp[i][j] = max(dp[i+1][j], dp[i][j-1])

        Key insight: Fill table by increasing interval length.

        Time: O(n^2)
        Space: O(n^2), can be optimized to O(n)
        """
        string_length = len(s)

        if string_length <= 1:
            return string_length

        # dp[i][j] = LPS length for s[i:j+1]
        palindrome_length: list[list[int]] = [
            [0] * string_length
            for _ in range(string_length)
        ]

        # Base case: single character is palindrome of length 1
        for i in range(string_length):
            palindrome_length[i][i] = 1

        # Fill by increasing interval length
        for interval_length in range(2, string_length + 1):
            for start in range(string_length - interval_length + 1):
                end = start + interval_length - 1

                if s[start] == s[end]:
                    # Endpoints match: extend inner palindrome by 2
                    inner_length = palindrome_length[start + 1][end - 1] if start + 1 <= end - 1 else 0
                    palindrome_length[start][end] = inner_length + 2
                else:
                    # Endpoints don't match: take best of excluding either
                    exclude_start = palindrome_length[start + 1][end]
                    exclude_end = palindrome_length[start][end - 1]
                    palindrome_length[start][end] = max(exclude_start, exclude_end)

        return palindrome_length[0][string_length - 1]
```

### 4.4 Space-Optimized Interval DP

```python
class SolutionLPSOptimized:
    def longestPalindromeSubseq(self, s: str) -> int:
        """
        Space-optimized: Only need previous diagonal values.

        We iterate by interval length, so we only need values from
        the previous length. Use 1D array with careful update order.

        Time: O(n^2)
        Space: O(n)
        """
        string_length = len(s)

        # dp[j] = LPS length ending at position j for current start
        current_row: list[int] = [1] * string_length

        for start in range(string_length - 2, -1, -1):
            # previous_diagonal saves dp[start+1][end-1] before overwrite
            previous_diagonal = 0

            for end in range(start + 1, string_length):
                # Save current value (will be diagonal for next end)
                temp = current_row[end]

                if s[start] == s[end]:
                    current_row[end] = previous_diagonal + 2
                else:
                    current_row[end] = max(current_row[end], current_row[end - 1])

                previous_diagonal = temp

        return current_row[string_length - 1]
```

### 4.5 Trace Example (Interval DP)

```
s = "bbbab"

Fill by interval length:

Length 1 (base case):
  i:    0   1   2   3   4
  s:    b   b   b   a   b
dp[i]: [1] [1] [1] [1] [1]

Length 2:
dp[0][1] = s[0]==s[1]? 2 : max(dp[1][1],dp[0][0]) = 2  (b==b)
dp[1][2] = 2  (b==b)
dp[2][3] = 1  (b!=a, max(1,1))
dp[3][4] = 1  (a!=b)

Length 3:
dp[0][2] = s[0]==s[2]? dp[1][1]+2 = 3  (b==b)
dp[1][3] = 2  (b!=a)
dp[2][4] = 2  (b==b)

Length 4:
dp[0][3] = 3  (b!=a, max(dp[1][3], dp[0][2]) = max(2,3) = 3)
dp[1][4] = 3  (b==b, dp[2][3]+2 = 1+2 = 3)

Length 5:
dp[0][4] = s[0]==s[4]? dp[1][3]+2 = 4  (b==b)

Answer: 4 (subsequence "bbbb")
```

### 4.6 Key Insights

1. **LCS Reduction**: LPS is a special case of LCS with string and its reverse
2. **Interval DP Pattern**: State depends on inner intervals, fill by length
3. **Space Trade-off**: O(n) space possible with careful update order
4. **Palindrome Property**: Endpoints must match to extend a palindrome

---

## 5. Advanced: Regular Expression Matching (LeetCode 10)

> **Problem**: Given a string `s` and a pattern `p`, implement regex matching with `.` (any single char) and `*` (zero or more of preceding element).
> **Invariant**: `dp[i][j]` = True if `s[0:i]` matches `p[0:j]`.
> **Delta from Base**: Boolean state with special wildcard handling.

### 5.1 Regex Rules

| Pattern | Meaning | Example |
|---------|---------|---------|
| `a-z` | Matches itself | `a` matches `"a"` |
| `.` | Matches any single character | `.` matches `"x"` |
| `*` | Matches zero or more of preceding | `a*` matches `""`, `"a"`, `"aaa"` |

### 5.2 State Transition Logic

```
For dp[i][j] where s[0:i] matches p[0:j]:

Case 1: p[j-1] is a letter or '.'
    If s[i-1] matches p[j-1] (same char or '.'):
        dp[i][j] = dp[i-1][j-1]
    Else:
        dp[i][j] = False

Case 2: p[j-1] is '*' (must look at p[j-2])
    Option A: Use zero occurrences of p[j-2]
        dp[i][j] = dp[i][j-2]

    Option B: Use one or more occurrences (if s[i-1] matches p[j-2])
        dp[i][j] = dp[i-1][j]  // consume s[i-1], keep pattern
```

### 5.3 Implementation

```python
class SolutionRegex:
    def isMatch(self, s: str, p: str) -> bool:
        """
        Implement regular expression matching with '.' and '*'.

        The '*' operator is the key challenge:
        - It modifies the PRECEDING character
        - It can match zero or more occurrences
        - We must consider both "use it" and "skip it" cases

        Time: O(m * n) where m = len(s), n = len(p)
        Space: O(m * n)
        """
        text_length = len(s)
        pattern_length = len(p)

        # dp[i][j] = True if s[0:i] matches p[0:j]
        is_match: list[list[bool]] = [
            [False] * (pattern_length + 1)
            for _ in range(text_length + 1)
        ]

        # Base case: empty string matches empty pattern
        is_match[0][0] = True

        # Base case: empty string vs pattern with '*'
        # Pattern like "a*b*c*" can match empty string
        for j in range(2, pattern_length + 1):
            if p[j - 1] == '*':
                # '*' can eliminate its preceding character
                is_match[0][j] = is_match[0][j - 2]

        # Fill DP table
        for i in range(1, text_length + 1):
            for j in range(1, pattern_length + 1):
                pattern_char = p[j - 1]

                if pattern_char == '*':
                    # Get the character before '*'
                    preceding_char = p[j - 2]

                    # Option 1: Use zero occurrences (skip char + '*')
                    zero_match = is_match[i][j - 2]

                    # Option 2: Use one+ occurrences (if current char matches preceding)
                    char_matches = (preceding_char == '.' or preceding_char == s[i - 1])
                    one_or_more_match = char_matches and is_match[i - 1][j]

                    is_match[i][j] = zero_match or one_or_more_match

                elif pattern_char == '.' or pattern_char == s[i - 1]:
                    # Direct match: inherit from diagonal
                    is_match[i][j] = is_match[i - 1][j - 1]

                # else: mismatch, stays False

        return is_match[text_length][pattern_length]
```

### 5.4 Space-Optimized Implementation

```python
class SolutionRegexOptimized:
    def isMatch(self, s: str, p: str) -> bool:
        """
        Space-optimized regex matching using two rows.

        Key insight: Each cell depends on:
        - Same row, j-2 (for '*' zero match)
        - Previous row, j (for '*' one+ match)
        - Previous row, j-1 (for direct match)

        Time: O(m * n)
        Space: O(n)
        """
        text_length = len(s)
        pattern_length = len(p)

        previous_row: list[bool] = [False] * (pattern_length + 1)
        previous_row[0] = True

        # Initialize: empty string vs pattern
        for j in range(2, pattern_length + 1):
            if p[j - 1] == '*':
                previous_row[j] = previous_row[j - 2]

        for i in range(1, text_length + 1):
            current_row: list[bool] = [False] * (pattern_length + 1)
            # current_row[0] = False (non-empty string can't match empty pattern)

            for j in range(1, pattern_length + 1):
                pattern_char = p[j - 1]

                if pattern_char == '*':
                    preceding_char = p[j - 2]

                    zero_match = current_row[j - 2]
                    char_matches = (preceding_char == '.' or preceding_char == s[i - 1])
                    one_or_more_match = char_matches and previous_row[j]

                    current_row[j] = zero_match or one_or_more_match

                elif pattern_char == '.' or pattern_char == s[i - 1]:
                    current_row[j] = previous_row[j - 1]

            previous_row = current_row

        return previous_row[pattern_length]
```

### 5.5 Trace Example

```
s = "aab", p = "c*a*b"

DP Table (True=T, False=F):
          ""   c    *    a    *    b
      ┌────┬────┬────┬────┬────┬────┐
   "" │ T  │ F  │ T  │ F  │ T  │ F  │
      ├────┼────┼────┼────┼────┼────┤
   a  │ F  │ F  │ F  │ T  │ T  │ F  │
      ├────┼────┼────┼────┼────┼────┤
   a  │ F  │ F  │ F  │ F  │ T  │ F  │
      ├────┼────┼────┼────┼────┼────┤
   b  │ F  │ F  │ F  │ F  │ F  │ T  │
      └────┴────┴────┴────┴────┴────┘

Explanation:
- dp[0][2]=T: "c*" matches "" (zero c's)
- dp[0][4]=T: "c*a*" matches "" (zero c's, zero a's)
- dp[1][3]=T: "a" matches "c*a" (zero c's, one a)
- dp[1][4]=T: "a" matches "c*a*" (extends from dp[0][4] with one a)
- dp[2][4]=T: "aa" matches "c*a*" (two a's)
- dp[3][5]=T: "aab" matches "c*a*b"

Answer: True
```

### 5.6 Key Insights

1. **'*' Modifies Preceding**: Always look at p[j-2] when processing '*'
2. **Two Choices for '*'**: Zero occurrences (skip) or one+ (consume and stay)
3. **Greedy Won't Work**: Must try all possibilities via DP
4. **Pattern Preprocessing**: Could simplify patterns like "a**" or "a*a*" but DP handles naturally

---

## 6. Advanced: Wildcard Matching (LeetCode 44)

> **Problem**: Given a string `s` and a pattern `p`, implement wildcard matching with `?` (any single char) and `*` (any sequence including empty).
> **Invariant**: `dp[i][j]` = True if `s[0:i]` matches `p[0:j]`.
> **Delta from Regex**: `*` matches any sequence directly (not "zero or more of preceding").

### 6.1 Wildcard vs Regex Comparison

| Aspect | Wildcard (`*`) | Regex (`*`) |
|--------|----------------|-------------|
| `*` Meaning | Any sequence (including empty) | Zero or more of PRECEDING char |
| `?` vs `.` | `?` = any single char | `.` = any single char |
| `a*` Meaning | `a` followed by anything | Zero or more `a`'s |
| Complexity | Simpler transitions | More complex (look-back) |

### 6.2 State Transition Logic

```
For dp[i][j] where s[0:i] matches p[0:j]:

Case 1: p[j-1] is a letter or '?'
    If s[i-1] matches p[j-1] (same char or '?'):
        dp[i][j] = dp[i-1][j-1]
    Else:
        dp[i][j] = False

Case 2: p[j-1] is '*'
    dp[i][j] = dp[i][j-1]     // '*' matches empty sequence
             or dp[i-1][j]    // '*' matches s[i-1] and continues
```

### 6.3 Implementation

```python
class SolutionWildcard:
    def isMatch(self, s: str, p: str) -> bool:
        """
        Implement wildcard pattern matching with '?' and '*'.

        Key insight for '*':
        - '*' can match empty: dp[i][j-1]
        - '*' can match current char and more: dp[i-1][j]

        The second case is powerful: if s[0:i-1] matches p[0:j],
        then s[0:i] also matches because '*' can extend.

        Time: O(m * n)
        Space: O(m * n)
        """
        text_length = len(s)
        pattern_length = len(p)

        # dp[i][j] = True if s[0:i] matches p[0:j]
        is_match: list[list[bool]] = [
            [False] * (pattern_length + 1)
            for _ in range(text_length + 1)
        ]

        # Base case: empty matches empty
        is_match[0][0] = True

        # Base case: empty string can match pattern of only '*'s
        for j in range(1, pattern_length + 1):
            if p[j - 1] == '*':
                is_match[0][j] = is_match[0][j - 1]
            else:
                break  # Once we hit non-'*', no more matches possible

        # Fill DP table
        for i in range(1, text_length + 1):
            for j in range(1, pattern_length + 1):
                pattern_char = p[j - 1]
                text_char = s[i - 1]

                if pattern_char == '*':
                    # '*' matches empty OR '*' matches current char and continues
                    match_empty = is_match[i][j - 1]
                    match_one_more = is_match[i - 1][j]
                    is_match[i][j] = match_empty or match_one_more

                elif pattern_char == '?' or pattern_char == text_char:
                    # Direct match: carry result from diagonal
                    is_match[i][j] = is_match[i - 1][j - 1]

                # else: mismatch, stays False

        return is_match[text_length][pattern_length]
```

### 6.4 Greedy Solution (O(1) Space for Some Cases)

```python
class SolutionWildcardGreedy:
    def isMatch(self, s: str, p: str) -> bool:
        """
        Greedy approach with backtracking on '*'.

        Strategy:
        - Match character by character
        - When hitting '*', remember position and try matching empty first
        - If later mismatch, backtrack to last '*' and match one more char

        Time: O(m * n) worst case, O(m + n) average
        Space: O(1)
        """
        text_idx = 0
        pattern_idx = 0
        text_length = len(s)
        pattern_length = len(p)

        # Position of last '*' and corresponding text position
        last_star_idx = -1
        last_star_match = 0

        while text_idx < text_length:
            # Case 1: Characters match or '?'
            if (pattern_idx < pattern_length and
                (p[pattern_idx] == s[text_idx] or p[pattern_idx] == '?')):
                text_idx += 1
                pattern_idx += 1

            # Case 2: '*' found - remember and match empty initially
            elif pattern_idx < pattern_length and p[pattern_idx] == '*':
                last_star_idx = pattern_idx
                last_star_match = text_idx
                pattern_idx += 1  # Move past '*', match empty

            # Case 3: Mismatch - backtrack to last '*' if exists
            elif last_star_idx != -1:
                pattern_idx = last_star_idx + 1
                last_star_match += 1  # '*' matches one more char
                text_idx = last_star_match

            else:
                return False

        # Skip trailing '*' in pattern
        while pattern_idx < pattern_length and p[pattern_idx] == '*':
            pattern_idx += 1

        return pattern_idx == pattern_length
```

### 6.5 Trace Example

```
s = "adceb", p = "*a*b"

DP Table (True=T, False=F):
          ""   *    a    *    b
      ┌────┬────┬────┬────┬────┐
   "" │ T  │ T  │ F  │ F  │ F  │
      ├────┼────┼────┼────┼────┤
   a  │ F  │ T  │ T  │ T  │ F  │
      ├────┼────┼────┼────┼────┤
   d  │ F  │ T  │ F  │ T  │ F  │
      ├────┼────┼────┼────┼────┤
   c  │ F  │ T  │ F  │ T  │ F  │
      ├────┼────┼────┼────┼────┤
   e  │ F  │ T  │ F  │ T  │ F  │
      ├────┼────┼────┼────┼────┤
   b  │ F  │ T  │ F  │ T  │ T  │
      └────┴────┴────┴────┴────┘

Trace:
- dp[0][1]=T: "*" matches ""
- dp[1][1]=T: "*" matches "a"
- dp[1][2]=T: "*a" matches "a"
- dp[1][3]=T: "*a*" matches "a"
- Column 1 all T: "*" matches any prefix
- dp[5][4]=T: "*a*" matches "adceb"
- dp[5][5]=T: "*a*b" matches "adceb"

Answer: True (pattern matches as "*"→"", "a"→"a", "*"→"dce", "b"→"b")
```

### 6.6 Key Insights

1. **Simpler Than Regex**: `*` is self-contained, no look-back needed
2. **Greedy Works**: Can use backtracking approach for O(1) space
3. **'*' Propagation**: First column all True after initial '*'s
4. **Two Choices for '*'**: Match empty (left) or match one more (up)

---

## 7. Pattern Comparison Table

| Problem | State `dp[i][j]` | Base Case | Match Transition | Mismatch Transition | Objective |
|---------|------------------|-----------|------------------|---------------------|-----------|
| **LCS** | LCS length for s[0:i], t[0:j] | 0 | `dp[i-1][j-1] + 1` | `max(dp[i-1][j], dp[i][j-1])` | Maximize |
| **Edit Distance** | Min ops for s[0:i] → t[0:j] | i or j | `dp[i-1][j-1]` | `1 + min(diagonal, up, left)` | Minimize |
| **Palindrome Subseq** | LPS length for s[i:j+1] | 1 (single char) | `dp[i+1][j-1] + 2` | `max(dp[i+1][j], dp[i][j-1])` | Maximize |
| **Regex Match** | s[0:i] matches p[0:j]? | True for empty | `dp[i-1][j-1]` | False (or `*` logic) | Boolean |
| **Wildcard Match** | s[0:i] matches p[0:j]? | True for empty | `dp[i-1][j-1]` | False (or `*` logic) | Boolean |

### 7.1 Transition Direction Summary

```
LCS / Edit Distance / Regex / Wildcard:
    ┌─────┬─────┐
    │ ↖   │  ←  │
    ├─────┼─────┤
    │  ↑  │ cur │
    └─────┴─────┘

↖ = diagonal (match/substitute)
← = horizontal (insert / skip in t)
↑ = vertical (delete / skip in s)

Palindrome Subsequence (Interval DP):
    ┌─────────────────┐
    │   dp[i+1][j-1]  │  (inner interval)
    ├─────┬─────┬─────┤
    │     │     │     │
    └─────┴─────┴─────┘
       ↑           ↑
   dp[i+1][j]   dp[i][j-1]
```

### 7.2 Complexity Comparison

| Problem | Time | Space | Space-Optimized |
|---------|------|-------|-----------------|
| LCS | O(mn) | O(mn) | O(min(m,n)) |
| Edit Distance | O(mn) | O(mn) | O(n) |
| Palindrome Subseq | O(n²) | O(n²) | O(n) |
| Regex Match | O(mn) | O(mn) | O(n) |
| Wildcard Match | O(mn) | O(mn) | O(n) or O(1)* |

*Wildcard can achieve O(1) space with greedy + backtracking.

### 7.3 Special Character Handling

| Char | Regex Meaning | Wildcard Meaning |
|------|---------------|------------------|
| `.` | Any single char | N/A |
| `?` | N/A | Any single char |
| `*` | Zero+ of PRECEDING char | Any sequence (including empty) |

---

## 8. Decision Tree

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

## 9. Pattern Selection Guide

### 9.1 Use LCS (LC 1143) when:
- Finding common elements between two sequences
- Subsequence (not substring) problems
- Building longest/shortest common supersequence

### 9.2 Use Edit Distance (LC 72) when:
- Converting one string to another
- Counting minimum operations
- Operations: insert, delete, replace

### 9.3 Use Palindrome DP (LC 516) when:
- Finding palindromic subsequences
- Single string problems
- Can reduce to LCS with reversed string

### 9.4 Use Regex Matching (LC 10) when:
- Pattern has wildcards (`.`, `*`)
- Boolean matching result
- Complex pattern rules

## 10. Problem Type Recognition

| Keywords/Clues | Pattern |
|----------------|---------|
| "longest common subsequence" | LCS |
| "minimum operations to convert" | Edit Distance |
| "palindrome subsequence" | LCS with reverse |
| "pattern matching with wildcards" | Regex/Wildcard DP |
| "delete operations for two strings" | LCS-based |

## 11. Complexity Guide

| Pattern | Time | Space | Space-Optimized |
|---------|------|-------|-----------------|
| LCS | O(mn) | O(mn) | O(min(m,n)) |
| Edit Distance | O(mn) | O(mn) | O(min(m,n)) |
| Palindrome | O(n²) | O(n²) | O(n) |
| Regex | O(mn) | O(mn) | O(n) |

---

## 12. LeetCode Problem Mapping

### 12.1 Core String DP Problems

| LC# | Problem | Pattern | Difficulty |
|-----|---------|---------|------------|
| **1143** | Longest Common Subsequence | LCS Base | Medium |
| **72** | Edit Distance | Levenshtein | Medium |
| **516** | Longest Palindromic Subsequence | LCS + Interval | Medium |
| **10** | Regular Expression Matching | Regex DP | Hard |
| **44** | Wildcard Matching | Pattern DP | Hard |

### 12.2 Related Problems by Pattern

#### LCS Family
| LC# | Problem | Delta from Base |
|-----|---------|-----------------|
| 1143 | Longest Common Subsequence | Base template |
| 583 | Delete Operation for Two Strings | LCS-based deletion count |
| 1092 | Shortest Common Supersequence | LCS + reconstruction |
| 712 | Minimum ASCII Delete Sum | Weighted LCS variant |

#### Edit Distance Family
| LC# | Problem | Delta from Base |
|-----|---------|-----------------|
| 72 | Edit Distance | Base template |
| 161 | One Edit Distance | O(n) special case |
| 392 | Is Subsequence | Simplified matching |

#### Palindrome Family
| LC# | Problem | Delta from Base |
|-----|---------|-----------------|
| 516 | Longest Palindromic Subsequence | LCS with reverse |
| 5 | Longest Palindromic Substring | Expand from center / DP |
| 647 | Palindromic Substrings | Count all palindromes |
| 1312 | Minimum Insertion for Palindrome | n - LPS(s) |

#### Pattern Matching Family
| LC# | Problem | Delta from Base |
|-----|---------|-----------------|
| 10 | Regular Expression Matching | Base with `.` and `*` |
| 44 | Wildcard Matching | Simpler `*` semantics |

### 12.3 Problem Selection Strategy

**For Learning String DP**:
1. Start with LC 1143 (LCS) - purest form
2. Then LC 72 (Edit Distance) - adds operations
3. Then LC 516 (Palindrome) - LCS reduction
4. Finally LC 10/44 (Matching) - boolean DP

**For Interview Prep**:
- LC 72 Edit Distance (very common)
- LC 1143 LCS (fundamental)
- LC 10 Regex Matching (Google/Meta favorite)

---

## 13. Universal Templates

### 13.1 Template 1: Longest Common Subsequence (LCS)

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

### 13.2 Template 2: Edit Distance

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

### 13.3 Template 3: Regex/Pattern Matching

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

### 13.4 Template 4: Space-Optimized LCS

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

## 14. Quick Reference

| Problem Type | Template | Key Transition |
|-------------|----------|----------------|
| Common subsequence | Template 1 | `max(left, up)` |
| String transformation | Template 2 | `1 + min(3 ops)` |
| Pattern matching | Template 3 | Handle `*` specially |
| Space-critical | Template 4 | Rolling array |



---



*Document generated for NeetCode Practice Framework — API Kernel: StringDP*
