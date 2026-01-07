## Universal Templates

### Template 1: KMP Failure Function

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

### Template 2: KMP Search

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

### Template 3: Rabin-Karp Rolling Hash

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

### Template 4: String Period Check

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

### Template 5: Longest Prefix = Suffix

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

## Quick Reference

| Problem Type | Template | Key Line |
|-------------|----------|----------|
| Pattern search | Template 2 | Return on `pattern_idx == len(pattern)` |
| Period check | Template 4 | `n % (n - failure[-1]) == 0` |
| Prefix=suffix | Template 5 | Return `s[:failure[-1]]` |
| Palindrome prefix | Use concat `s + '#' + rev(s)` | failure[-1] of concat |

