# 516. Longest Palindromic Subsequence

## Problem Link
https://leetcode.com/problems/longest-palindromic-subsequence/

## Difficulty
Medium

## Tags
- String
- Dynamic Programming

## Pattern
String DP - Palindrome via LCS

## API Kernel
`StringDP`

## Problem Summary
Given a string `s`, find the longest palindromic subsequence's length in `s`. A subsequence is a sequence that can be derived from another sequence by deleting some or no elements without changing the order of the remaining elements.

## Key Insight

A palindrome reads the same forwards and backwards. The **longest palindromic subsequence** is exactly the **LCS of `s` and `reverse(s)`**.

Why? Any common subsequence between `s` and its reverse must be a palindrome (it appears in both forward and backward directions).

Alternative: Direct interval DP approach where `dp[i][j]` = LPS of `s[i:j+1]`.

## Template Mapping

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

## Complexity
- Time: O(n^2)
- Space: O(n^2), can be optimized to O(n)

## Why This Problem Third?

LPS shows how LCS generalizes:
1. Demonstrates reduction technique (LPS -> LCS)
2. Introduces interval DP as an alternative
3. Bridge between String DP and Interval DP patterns

## Common Mistakes

1. **Forgetting that LCS works** - Many try complex approaches when LCS with reverse is simpler
2. **Interval DP order** - Must fill by increasing length, not by row
3. **Base case for interval** - Single characters have LPS = 1

## Related Problems
- LC 5: Longest Palindromic Substring (Contiguous, not subsequence)
- LC 647: Palindromic Substrings (Count all palindromic substrings)
- LC 1312: Minimum Insertion Steps (Make string palindrome)
