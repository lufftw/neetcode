## Universal Templates

### Template 1: Burst Balloons Style

```python
def burst_balloons_template(nums: list) -> int:
    """
    Maximum coins from bursting all balloons.
    Time: O(n³), Space: O(n²)
    """
    nums = [1] + nums + [1]
    n = len(nums)

    dp = [[0] * n for _ in range(n)]

    for length in range(2, n):
        for i in range(n - length):
            j = i + length
            for k in range(i + 1, j):
                coins = nums[i] * nums[k] * nums[j]
                dp[i][j] = max(dp[i][j], dp[i][k] + dp[k][j] + coins)

    return dp[0][n - 1]
```

**Use for**: LC 312, problems where removing item affects neighbors

---

### Template 2: Polygon Triangulation Style

```python
def polygon_triangulation_template(values: list) -> int:
    """
    Minimum score to triangulate polygon.
    Time: O(n³), Space: O(n²)
    """
    n = len(values)
    dp = [[0] * n for _ in range(n)]

    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')

            for k in range(i + 1, j):
                cost = values[i] * values[k] * values[j]
                dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j] + cost)

    return dp[0][n - 1]
```

**Use for**: LC 1039, geometric interval DP

---

### Template 3: Cut Stick Style

```python
def cut_stick_template(n: int, cuts: list) -> int:
    """
    Minimum cost to make all cuts.
    Time: O(m³), Space: O(m²)
    """
    cuts = sorted([0] + cuts + [n])
    m = len(cuts)
    dp = [[0] * m for _ in range(m)]

    for gap in range(2, m):
        for i in range(m - gap):
            j = i + gap
            dp[i][j] = float('inf')

            for k in range(i + 1, j):
                cost = cuts[j] - cuts[i]
                dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j] + cost)

    return dp[0][m - 1]
```

**Use for**: LC 1547, cutting/splitting problems

---

### Template 4: Strange Printer Style

```python
def strange_printer_template(s: str) -> int:
    """
    Minimum turns to print string.
    Time: O(n³), Space: O(n²)
    """
    # Remove consecutive duplicates
    s = ''.join(c for i, c in enumerate(s) if i == 0 or c != s[i-1])
    n = len(s)

    if n == 0:
        return 0

    dp = [[0] * n for _ in range(n)]

    for i in range(n):
        dp[i][i] = 1

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = dp[i + 1][j] + 1

            for k in range(i + 1, j + 1):
                if s[k] == s[i]:
                    left = dp[i + 1][k - 1] if k > i + 1 else 0
                    right = dp[k][j]
                    dp[i][j] = min(dp[i][j], left + right)

    return dp[0][n - 1]
```

**Use for**: LC 664, character-matching optimization

---

## Quick Reference

| Problem Type | Template | Key Feature |
|-------------|----------|-------------|
| Remove with neighbor effect | Template 1 | Add boundary elements |
| Polygon/geometric | Template 2 | Edge-based splitting |
| Cutting/splitting | Template 3 | Sort and add boundaries |
| Character matching | Template 4 | Special recurrence |
