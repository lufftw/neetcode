# 10. Regular Expression Matching

## Problem Link
https://leetcode.com/problems/regular-expression-matching/

## Difficulty
Hard

## Tags
- String
- Dynamic Programming
- Recursion

## Pattern
String DP - Regex Matching

## API Kernel
`StringDP`

## Problem Summary
Given an input string `s` and a pattern `p`, implement regular expression matching with support for `.` (matches any single character) and `*` (matches zero or more of the preceding element).

## Key Insight

The key is handling `*` correctly:
- `*` means "zero or more of the previous character"
- For pattern `a*`, we can either:
  1. Use zero `a`s: skip `a*` entirely, check `dp[i][j-2]`
  2. Use one+ `a`s: if `s[i-1]` matches `a`, check `dp[i-1][j]`

The `.` wildcard just matches any character.

## Template Mapping

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

## Complexity
- Time: O(m * n)
- Space: O(m * n)

## Why This Problem Fourth?

Regex Matching is the capstone problem:
1. Complex transitions with multiple cases
2. Non-trivial base cases (empty string matching `a*b*`)
3. Requires careful handling of `*` looking back at `j-2`
4. Tests complete mastery of String DP

## Common Mistakes

1. **Handling `*` incorrectly** - Must look at `p[j-2]` (the character before `*`)
2. **Base case for `*` patterns** - Empty string can match `a*`, `a*b*`, etc.
3. **Order of checks** - Must check for `*` first, then normal match
4. **Off-by-one with `*`** - When checking zero occurrences, use `dp[i][j-2]`, not `dp[i][j-1]`

## Related Problems
- LC 44: Wildcard Matching (Similar but `*` matches any sequence)
- LC 115: Distinct Subsequences (Count matching subsequences)
- LC 97: Interleaving String (Another complex String DP)
