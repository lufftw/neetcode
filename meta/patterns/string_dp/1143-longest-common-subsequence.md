# 1143. Longest Common Subsequence

## Problem Link
https://leetcode.com/problems/longest-common-subsequence/

## Difficulty
Medium

## Tags
- String
- Dynamic Programming

## Pattern
String DP - LCS (Longest Common Subsequence)

## API Kernel
`StringDP`

## Problem Summary
Given two strings `text1` and `text2`, return the length of their longest common subsequence. A subsequence is a sequence that can be derived from another sequence by deleting some or no elements without changing the order of the remaining elements.

## Key Insight

The LCS problem has optimal substructure:
- If the last characters match: `LCS(s[0:i], t[0:j]) = 1 + LCS(s[0:i-1], t[0:j-1])`
- If they don't match: `LCS(s[0:i], t[0:j]) = max(LCS(s[0:i-1], t[0:j]), LCS(s[0:i], t[0:j-1]))`

When characters match, we include them in the LCS. When they don't, we try excluding one character from either string.

## Template Mapping

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

## Complexity
- Time: O(m * n) where m, n are lengths of the two strings
- Space: O(m * n), can be optimized to O(min(m, n))

## Why This Problem First?

LCS is the **canonical** String DP problem:
1. Simple state definition: `dp[i][j]` = LCS length for prefixes
2. Clean transitions: match adds 1, mismatch takes max
3. No complex base cases
4. Foundation for all other String DP variants

## Common Mistakes

1. **Off-by-one errors** - Remember `dp[i][j]` corresponds to `s[0:i]` and `t[0:j]`, so access `s[i-1]` and `t[j-1]`
2. **Forgetting base cases** - First row and column are implicitly 0 (empty string has LCS 0)
3. **Wrong transition for mismatch** - Must take max of two options, not three

## Related Problems
- LC 516: Longest Palindromic Subsequence (LCS with reversed string)
- LC 583: Delete Operation for Two Strings (Uses LCS)
- LC 1092: Shortest Common Supersequence (Build string from LCS)
