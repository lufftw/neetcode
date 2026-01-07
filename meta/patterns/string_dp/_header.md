# String DP Patterns: Complete Reference

> **API Kernel**: `StringDP`
> **Core Mechanism**: Two-dimensional state transition over string pairs, where `dp[i][j]` represents the optimal solution for prefixes `s[0:i]` and `t[0:j]`.

This document presents the **canonical String DP templates** and all major variations. String DP is fundamentally different from linear DP (1D sequences) or knapsack DP (subset selection) — it focuses on **pairwise string comparison** with a 2D state space.

---

## Core Concepts

### The String DP State Space

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

### Universal Template Structure

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

### Three Fundamental Transition Patterns

| Pattern | Direction | Meaning | Example |
|---------|-----------|---------|---------|
| **Match/Substitute** | ↖ Diagonal | Characters align or are replaced | LCS, Edit Distance |
| **Skip String S** | ↑ Vertical | Skip current char in s | LCS (no match), Regex `*` |
| **Skip String T** | ← Horizontal | Skip current char in t | Edit Distance (insert) |

### Space Optimization

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


