## Universal Templates

### Template 1: Longest Common Subsequence (LCS)

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

### Template 2: Edit Distance

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

### Template 3: Regex/Pattern Matching

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

### Template 4: Space-Optimized LCS

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

## Quick Reference

| Problem Type | Template | Key Transition |
|-------------|----------|----------------|
| Common subsequence | Template 1 | `max(left, up)` |
| String transformation | Template 2 | `1 + min(3 ops)` |
| Pattern matching | Template 3 | Handle `*` specially |
| Space-critical | Template 4 | Rolling array |
