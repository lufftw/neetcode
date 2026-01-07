## LeetCode Problem Mapping

### Core String DP Problems

| LC# | Problem | Pattern | Difficulty |
|-----|---------|---------|------------|
| **1143** | Longest Common Subsequence | LCS Base | Medium |
| **72** | Edit Distance | Levenshtein | Medium |
| **516** | Longest Palindromic Subsequence | LCS + Interval | Medium |
| **10** | Regular Expression Matching | Regex DP | Hard |
| **44** | Wildcard Matching | Pattern DP | Hard |

### Related Problems by Pattern

#### LCS Family
| LC# | Problem | Delta from Base |
|-----|---------|-----------------|
| 1143 | Longest Common Subsequence | Base template |
| 583 | Delete Operation for Two Strings | LCS-based deletion count |
| 1092 | Shortest Common Supersequence | LCS + reconstruction |
| 712 | Minimum ASCII Delete Sum | Weighted LCS variant |

#### Edit Distance Family
| LC# | Problem | Delta from Base |
|-----|---------|-----------------|
| 72 | Edit Distance | Base template |
| 161 | One Edit Distance | O(n) special case |
| 392 | Is Subsequence | Simplified matching |

#### Palindrome Family
| LC# | Problem | Delta from Base |
|-----|---------|-----------------|
| 516 | Longest Palindromic Subsequence | LCS with reverse |
| 5 | Longest Palindromic Substring | Expand from center / DP |
| 647 | Palindromic Substrings | Count all palindromes |
| 1312 | Minimum Insertion for Palindrome | n - LPS(s) |

#### Pattern Matching Family
| LC# | Problem | Delta from Base |
|-----|---------|-----------------|
| 10 | Regular Expression Matching | Base with `.` and `*` |
| 44 | Wildcard Matching | Simpler `*` semantics |

### Problem Selection Strategy

**For Learning String DP**:
1. Start with LC 1143 (LCS) - purest form
2. Then LC 72 (Edit Distance) - adds operations
3. Then LC 516 (Palindrome) - LCS reduction
4. Finally LC 10/44 (Matching) - boolean DP

**For Interview Prep**:
- LC 72 Edit Distance (very common)
- LC 1143 LCS (fundamental)
- LC 10 Regex Matching (Google/Meta favorite)

