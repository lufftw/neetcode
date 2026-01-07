## Advanced: Wildcard Matching (LeetCode 44)

> **Problem**: Given a string `s` and a pattern `p`, implement wildcard matching with `?` (any single char) and `*` (any sequence including empty).
> **Invariant**: `dp[i][j]` = True if `s[0:i]` matches `p[0:j]`.
> **Delta from Regex**: `*` matches any sequence directly (not "zero or more of preceding").

### Wildcard vs Regex Comparison

| Aspect | Wildcard (`*`) | Regex (`*`) |
|--------|----------------|-------------|
| `*` Meaning | Any sequence (including empty) | Zero or more of PRECEDING char |
| `?` vs `.` | `?` = any single char | `.` = any single char |
| `a*` Meaning | `a` followed by anything | Zero or more `a`'s |
| Complexity | Simpler transitions | More complex (look-back) |

### State Transition Logic

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

### Implementation

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

### Greedy Solution (O(1) Space for Some Cases)

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

### Trace Example

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

### Key Insights

1. **Simpler Than Regex**: `*` is self-contained, no look-back needed
2. **Greedy Works**: Can use backtracking approach for O(1) space
3. **'*' Propagation**: First column all True after initial '*'s
4. **Two Choices for '*'**: Match empty (left) or match one more (up)


