# String DP - Intuition Guide

## The Mental Model: Filling a Grid

Imagine you have two strings written along the edges of a grid:
- First string `s` along the rows (top to bottom)
- Second string `t` along the columns (left to right)

Each cell `(i, j)` represents the answer for comparing `s[0:i]` with `t[0:j]`.

```
        ""  a   b   c
    ┌───┬───┬───┬───┐
""  │ 0 │ 0 │ 0 │ 0 │
    ├───┼───┼───┼───┤
a   │ 0 │ 1 │ 1 │ 1 │
    ├───┼───┼───┼───┤
c   │ 0 │ 1 │ 1 │ 2 │
    └───┴───┴───┴───┘
```

You fill this grid row by row, and each cell only needs its neighbors:
- Diagonal (top-left): both strings shrink
- Up: first string shrinks
- Left: second string shrinks

## Why String DP?

String DP works because string comparison has **optimal substructure**:
- The best answer for long strings depends only on answers for shorter strings
- We can systematically build from empty strings to full strings

## Core Insight

The transition depends on whether current characters match:

```
Match:      s[i-1] == t[j-1]
            → Look diagonal (both consumed)

Mismatch:   s[i-1] != t[j-1]
            → Look up, left, or diagonal (try all options)
```

## Pattern 1: LCS (Longest Common Subsequence)

**The insight**: If characters match, include them. If not, try skipping either character.

```
s = "ace", t = "abcde"

        ""  a   b   c   d   e
    ┌───┬───┬───┬───┬───┬───┐
""  │ 0 │ 0 │ 0 │ 0 │ 0 │ 0 │
    ├───┼───┼───┼───┼───┼───┤
a   │ 0 │ 1 │ 1 │ 1 │ 1 │ 1 │  a=a: +1
    ├───┼───┼───┼───┼───┼───┤
c   │ 0 │ 1 │ 1 │ 2 │ 2 │ 2 │  c=c: +1
    ├───┼───┼───┼───┼───┼───┤
e   │ 0 │ 1 │ 1 │ 2 │ 2 │ 3 │  e=e: +1
    └───┴───┴───┴───┴───┴───┘
                        └── Answer: 3
```

The code:
```python
if s[i-1] == t[j-1]:
    dp[i][j] = dp[i-1][j-1] + 1  # Include this character
else:
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])  # Skip one char
```

## Pattern 2: Edit Distance

**The insight**: Each cell is the minimum edits to transform. Three operations mean three choices.

```
s = "horse", t = "ros"

        ""  r   o   s
    ┌───┬───┬───┬───┐
""  │ 0 │ 1 │ 2 │ 3 │  Insert all
    ├───┼───┼───┼───┤
h   │ 1 │ 1 │ 2 │ 3 │  h≠r: min(replace, delete, insert)
    ├───┼───┼───┼───┤
o   │ 2 │ 2 │ 1 │ 2 │  o=o: diagonal (no cost)
    ├───┼───┼───┼───┤
r   │ 3 │ 2 │ 2 │ 2 │  r≠s: +1
    ├───┼───┼───┼───┤
s   │ 4 │ 3 │ 3 │ 2 │  s=s: diagonal
    ├───┼───┼───┼───┤
e   │ 5 │ 4 │ 4 │ 3 │  Answer: 3
    └───┴───┴───┴───┘
```

The code:
```python
if s[i-1] == t[j-1]:
    dp[i][j] = dp[i-1][j-1]  # No operation needed
else:
    dp[i][j] = 1 + min(
        dp[i-1][j-1],  # Replace s[i-1] with t[j-1]
        dp[i-1][j],    # Delete s[i-1]
        dp[i][j-1]     # Insert t[j-1]
    )
```

## Pattern 3: Palindrome Subsequence

**The insight**: A palindrome reads the same forwards and backwards.

The LPS of string `s` = LCS of `s` and `reverse(s)`.

```
s = "bbbab"
t = "babbb" (reversed)

LCS = "bbbb" (length 4)
```

Why does this work? Any common subsequence between `s` and its reverse must appear in both directions, making it a palindrome.

## Pattern 4: Regex Matching

**The insight**: Handle `*` by considering "use it" vs "skip it".

```
s = "aab", p = "c*a*b"

c*  → 0 or more 'c' (we use 0)
a*  → 0 or more 'a' (we use 2)
b   → exactly 'b' (we use 1)

Result: MATCH
```

The tricky part is `*`:
```python
if p[j-1] == '*':
    # Option 1: Use zero of p[j-2]
    dp[i][j] = dp[i][j-2]

    # Option 2: Use one or more of p[j-2]
    if p[j-2] == '.' or p[j-2] == s[i-1]:
        dp[i][j] = dp[i][j] or dp[i-1][j]
```

## Common Mistakes

### Mistake 1: Off-by-one indexing

```python
# ❌ Wrong: dp indices and string indices are off by 1
if s[i] == t[j]:

# ✅ Right: dp[i][j] corresponds to s[0:i], so character is s[i-1]
if s[i-1] == t[j-1]:
```

### Mistake 2: Wrong base cases for Edit Distance

```python
# ❌ Wrong: Forgetting base cases
dp = [[0] * (n+1) for _ in range(m+1)]

# ✅ Right: Empty string requires i deletions or j insertions
for i in range(m+1):
    dp[i][0] = i
for j in range(n+1):
    dp[0][j] = j
```

### Mistake 3: Regex `*` looks at wrong index

```python
# ❌ Wrong: Looking at j-1 for the character before *
if p[j-1] == s[i-1]:

# ✅ Right: * is at j-1, so the character is at j-2
if p[j-2] == s[i-1]:
```

## Quick Pattern Recognition

| Clue | Pattern |
|------|---------|
| "longest common subsequence" | LCS |
| "minimum operations to convert" | Edit Distance |
| "palindrome subsequence" | LCS with reverse |
| "match pattern with . or *" | Regex DP |
| "delete operation for two strings" | LCS-based |

## Visual Summary

```
String DP: Compare s[0:i] with t[0:j]

           ┌─────────────┐
           │ dp[i-1][j-1]│───► Match: usually this
           └──────┬──────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
┌────────┐  ┌─────────────┐  ┌────────┐
│dp[i-1] │  │  dp[i][j]   │  │dp[i]   │
│  [j]   │  │  (current)  │  │ [j-1]  │
└────────┘  └─────────────┘  └────────┘
Delete s[i]                  Insert t[j]
    │                             │
    └──────────┬──────────────────┘
               │
               ▼
         Mismatch: combine
         these options
```
