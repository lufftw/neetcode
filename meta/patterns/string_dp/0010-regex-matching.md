## Advanced: Regular Expression Matching (LeetCode 10)

> **Problem**: Given a string `s` and a pattern `p`, implement regex matching with `.` (any single char) and `*` (zero or more of preceding element).
> **Invariant**: `dp[i][j]` = True if `s[0:i]` matches `p[0:j]`.
> **Delta from Base**: Boolean state with special wildcard handling.

### Regex Rules

| Pattern | Meaning | Example |
|---------|---------|---------|
| `a-z` | Matches itself | `a` matches `"a"` |
| `.` | Matches any single character | `.` matches `"x"` |
| `*` | Matches zero or more of preceding | `a*` matches `""`, `"a"`, `"aaa"` |

### State Transition Logic

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

### Implementation

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

### Space-Optimized Implementation

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

### Trace Example

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

### Key Insights

1. **'*' Modifies Preceding**: Always look at p[j-2] when processing '*'
2. **Two Choices for '*'**: Zero occurrences (skip) or one+ (consume and stay)
3. **Greedy Won't Work**: Must try all possibilities via DP
4. **Pattern Preprocessing**: Could simplify patterns like "a**" or "a*a*" but DP handles naturally


