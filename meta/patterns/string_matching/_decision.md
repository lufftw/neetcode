## Decision Tree

```
Start: String matching/search problem?
            │
            ▼
    ┌───────────────────┐
    │ What's the goal?  │
    └───────────────────┘
            │
    ┌───────┼───────┬───────────┐
    ▼       ▼       ▼           ▼
Find      Check   Find        Find
pattern   period  palindrome  prefix=suffix
    │       │     prefix      │
    ▼       ▼       │         ▼
Use KMP   Period    ▼       Direct
or R-K    formula  KMP+rev  failure[-1]
```

## Pattern Selection Guide

### Use KMP (LC 28, 1392) when:
- Searching for a pattern in text
- Need guaranteed O(n+m) time
- Finding longest prefix=suffix
- Working with failure function properties

### Use Rabin-Karp when:
- Searching multiple patterns
- Need average-case efficiency
- Hash fingerprinting is useful
- Willing to accept worst-case O(nm)

### Use Period Formula (LC 459) when:
- Checking if string is built from repeating unit
- Finding minimum period length
- Detecting cyclic patterns

### Use Concatenation Trick (LC 214) when:
- Finding palindromic prefixes
- Combining KMP with string reversal
- Need to find overlapping structures

## Problem Type Recognition

| Keywords/Clues | Pattern |
|----------------|---------|
| "find first occurrence" | KMP search |
| "repeated substring" | KMP period |
| "shortest palindrome" | KMP + reverse |
| "happy prefix" | KMP failure[-1] |
| "pattern matching" | KMP or Rabin-Karp |

