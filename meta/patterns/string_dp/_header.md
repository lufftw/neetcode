# String DP Pattern

## API Kernel: `StringDP`

> **Core Mechanism**: Use 2D DP table where `dp[i][j]` represents the optimal result for substrings `s[0:i]` and `t[0:j]`.

## Why String DP?

String DP solves problems where:
- You need to compare, align, or match two strings
- The answer depends on subsequences or substrings of both strings
- Optimal substructure exists between prefixes of the strings

## Core Insight

The key insight is that comparing two strings of lengths `m` and `n` can be broken into subproblems comparing their prefixes. The state `dp[i][j]` depends on:
- `dp[i-1][j-1]` - both strings shrink by one character
- `dp[i-1][j]` - only the first string shrinks
- `dp[i][j-1]` - only the second string shrinks

This creates a systematic way to build up the answer from smaller subproblems.

## Universal Template Structure

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

## Pattern Variants

| Pattern | State | Transition | Example |
|---------|-------|------------|---------|
| **LCS** | Length of LCS for prefixes | Match: `+1`, Mismatch: `max(left, up)` | LC 1143 |
| **Edit Distance** | Min edits to transform | Match: `same`, Mismatch: `1 + min(3 ops)` | LC 72 |
| **Palindrome** | LCS(s, reverse(s)) | Same as LCS | LC 516 |
| **Regex Match** | Boolean: can match? | Complex transitions based on pattern | LC 10 |
