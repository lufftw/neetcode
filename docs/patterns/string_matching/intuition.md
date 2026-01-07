# String Matching - Intuition Guide

## The Mental Model: Preprocessing for Speed

Imagine searching for a word in a book:
- **Naive approach**: Start at page 1, check every position for your word
- **Smart approach**: Build an index first, then use it to skip irrelevant sections

**String Matching algorithms preprocess** the pattern (or text) to enable faster searching.

## Why Does Naive Search Fail?

Consider searching for "AAAB" in "AAAAAAB":

```
Text:    A A A A A A B
Pattern: A A A B
         ✓ ✓ ✓ ✗ (mismatch at position 3)

Naive: Shift by 1, restart from scratch
         A A A B
         ↑ start over

KMP: We matched "AAA" before failing. Use that information!
     The failure function tells us: shift to align with longest proper prefix
```

**Key insight**: Don't throw away match information when you fail.

## KMP: The Failure Function Intuition

### What is the Failure Function?

For pattern "AABAACAAB":

```
Index:    0  1  2  3  4  5  6  7  8
Pattern:  A  A  B  A  A  C  A  A  B
LPS:      0  1  0  1  2  0  1  2  3
          │  │     │  │     │  │  │
          │  └─A   │  │     │  │  └─AAB prefix matches AAB suffix
          │        │  └─AA  │  └─AA
          └─no proper prefix = suffix
```

**LPS[i]** = length of the longest **proper** prefix of pattern[0..i] that's also a suffix.

### Why Does This Help?

When we mismatch at position j, we've already matched pattern[0..j-1]:

```
Text:    ... X X X A A B A A C A A X ...
Pattern:             A A B A A C A A B
                                   ↑ mismatch at j=8

We matched "AABAACAA" before failing.
LPS[7] = 2 means: "AA" is both prefix and suffix

So we can shift to align the prefix "AA" where the suffix was:
Text:    ... X X X A A B A A C A A X ...
Pattern:                       A A B A A C A A B
                               ↑ continue from j=2
```

**No need to re-examine characters we've already matched!**

## Rabin-Karp: The Rolling Hash Intuition

### The Basic Idea

Instead of comparing characters, compare fingerprints (hashes).

```
Pattern: "ABC" → hash = 65*256² + 66*256 + 67 = 4276803

Text: "XYZABCDEF"
Window 1: "XYZ" → hash ≠ pattern_hash
Window 2: "YZA" → hash ≠ pattern_hash
Window 3: "ZAB" → hash ≠ pattern_hash
Window 4: "ABC" → hash == pattern_hash → verify!
```

### Why "Rolling"?

Computing hash from scratch each window = O(m) per window = O(nm) total.

**Rolling hash** updates in O(1):

```
hash("YZA") = (hash("XYZ") - 'X' * 256²) * 256 + 'A'
            = (prev_hash - leftmost_char * highest_power) * base + new_char
```

**Intuition**: It's like a conveyor belt. Push new char in, old char falls out.

## Pattern 1: Find Needle in Haystack (LC 28) - Base Case

The canonical string matching problem:

```python
# KMP approach
def strStr(haystack, needle):
    # 1. Build failure function for needle
    # 2. Match haystack against needle using failure function

# Rabin-Karp approach
def strStr(haystack, needle):
    # 1. Compute hash of needle
    # 2. Slide window, update hash in O(1)
    # 3. On hash match, verify characters
```

**When to use which?**
- KMP: Guaranteed O(n+m), no hash collisions
- Rabin-Karp: Better when searching for multiple patterns

## Pattern 2: Shortest Palindrome (LC 214) - Concatenation Trick

**Problem**: Add minimum characters to front to make string a palindrome.

**Key insight**: Find longest palindrome prefix, then prepend the reverse of what's left.

```
s = "aacecaaa"
Longest palindrome prefix: "aacecaa" (7 chars)
Remaining: "a"
Answer: reverse("a") + s = "a" + "aacecaaa" = "aaacecaaa"
```

**The KMP trick**: Compute LPS of `s + '#' + reverse(s)`

```
s = "aacecaaa"
combined = "aacecaaa#aaacecaa"
LPS[-1] = 7 (length of palindrome prefix)
```

Why? The LPS at the end tells us how much of the original string's prefix matches its reversed suffix - exactly the palindrome prefix length!

## Pattern 3: Repeated Substring (LC 459) - Period Detection

**Problem**: Check if string is made by repeating a smaller substring.

**The beautiful insight**:

```
s = "abcabc"
Period formula: period = len(s) - LPS[-1] = 6 - 3 = 3

If len(s) % period == 0, the string is periodic!
Check: 6 % 3 == 0 ✓, so "abc" repeats twice
```

**Why does this work?**

If LPS[-1] > 0, there's overlap between prefix and suffix:

```
String:  a b c | a b c
Prefix:  a b c |         (length 3)
Suffix:        | a b c   (length 3)
Overlap at LPS[-1] = 3

The non-overlapping part (length = n - LPS[-1] = 3) is the minimal period!
```

## Pattern 4: Longest Happy Prefix (LC 1392) - Direct LPS

This is the most direct application of the failure function:

```
s = "level"
LPS array: [0, 0, 0, 0, 1]
            l  e  v  e  l
                        └─ 'l' = prefix[0], so LPS[4] = 1

Answer: s[0:LPS[-1]] = s[0:1] = "l"
```

The last value of the LPS array directly gives us the answer!

## The Core Templates

### KMP Failure Function

```python
def compute_lps(pattern):
    n = len(pattern)
    lps = [0] * n
    length = 0  # length of previous longest prefix suffix

    i = 1
    while i < n:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]  # Key: fall back, don't increment i
            else:
                lps[i] = 0
                i += 1

    return lps
```

### Rolling Hash

```python
def rolling_hash(text, m):
    BASE = 256
    MOD = 10**9 + 7

    h = 0
    highest_power = pow(BASE, m - 1, MOD)

    for i in range(m):
        h = (h * BASE + ord(text[i])) % MOD

    yield 0, h  # (start_index, hash)

    for i in range(m, len(text)):
        # Remove leftmost, add rightmost
        h = (h - ord(text[i - m]) * highest_power) % MOD
        h = (h * BASE + ord(text[i])) % MOD
        yield i - m + 1, h
```

## Pattern Recognition Checklist

| Question | If Yes → String Matching |
|----------|-------------------------|
| Finding substring in larger string? | ✓ |
| Need to know if prefix equals suffix? | ✓ |
| Checking for periodic/repeating patterns? | ✓ |
| Need palindrome information efficiently? | ✓ |

## Variant Recognition

| Clue | Technique |
|------|-----------|
| "Find first occurrence" | KMP or Rabin-Karp |
| "Count occurrences" | KMP with counter |
| "Shortest palindrome prefix" | KMP on s + '#' + rev(s) |
| "Is string periodic?" | LPS[-1] and divisibility |
| "Longest prefix = suffix" | Direct LPS[-1] |
| "Multiple pattern search" | Rabin-Karp or Aho-Corasick |

## Common Pitfalls

1. **Off-by-one in LPS**: LPS[i] is for substring [0..i], not [0..i-1]
2. **Forgetting separator**: When using `s + rev(s)`, add '#' to prevent false matches
3. **Hash collisions**: Always verify on hash match in Rabin-Karp
4. **Modular arithmetic**: Use `% MOD` after every operation to prevent overflow
5. **Period formula**: It's `n - LPS[-1]`, not `LPS[-1]`

## Complexity

| Algorithm | Time | Space |
|-----------|------|-------|
| KMP | O(n + m) | O(m) |
| Rabin-Karp | O(n + m) average | O(1) |
| Naive | O(nm) | O(1) |

Where n = text length, m = pattern length.

## The Power of Preprocessing

The fundamental insight of string matching: **invest O(m) preprocessing to save O(nm) searching**.

This preprocessing vs. querying trade-off appears throughout algorithm design:
- Binary Search: O(n log n) sort for O(log n) queries
- Segment Tree: O(n) build for O(log n) range queries
- KMP: O(m) LPS computation for O(n) pattern matching
