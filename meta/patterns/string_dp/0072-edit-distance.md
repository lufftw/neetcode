## Variant: Edit Distance (LeetCode 72)

> **Problem**: Given two strings `word1` and `word2`, return the minimum number of operations to convert `word1` to `word2`. Operations: insert, delete, replace.
> **Invariant**: `dp[i][j]` = minimum edit distance for `word1[0:i]` and `word2[0:j]`.
> **Delta from Base**: Add three edit operations instead of just match/skip.

### How This Differs From LCS

| Aspect | LCS | Edit Distance |
|--------|-----|---------------|
| Objective | Maximize matches | Minimize operations |
| Operations | Match, Skip | Insert, Delete, Replace |
| Base Case | 0 (empty = no match) | Length (need all inserts/deletes) |
| Transition | max() | min() + 1 |

### State Transition Logic

```
If word1[i-1] == word2[j-1]:
    dp[i][j] = dp[i-1][j-1]         // Match: no operation needed
Else:
    dp[i][j] = 1 + min(
        dp[i-1][j-1],               // Replace word1[i-1] with word2[j-1]
        dp[i-1][j],                 // Delete word1[i-1]
        dp[i][j-1]                  // Insert word2[j-1]
    )
```

### Implementation

```python
class SolutionEditDistance:
    def minDistance(self, word1: str, word2: str) -> int:
        """
        Calculate minimum edit distance (Levenshtein distance) between two strings.

        The three operations and their DP transitions:
        - Replace: dp[i-1][j-1] + 1 (transform word1[i-1] to word2[j-1])
        - Delete:  dp[i-1][j] + 1   (remove word1[i-1])
        - Insert:  dp[i][j-1] + 1   (add word2[j-1] to word1)

        Time: O(m * n)
        Space: O(m * n), can be optimized to O(n)
        """
        source_length = len(word1)
        target_length = len(word2)

        # dp[i][j] = min operations to convert word1[0:i] to word2[0:j]
        edit_distance: list[list[int]] = [
            [0] * (target_length + 1)
            for _ in range(source_length + 1)
        ]

        # Base case: converting to/from empty string
        # Empty -> word2[0:j] requires j insertions
        for j in range(target_length + 1):
            edit_distance[0][j] = j

        # word1[0:i] -> empty requires i deletions
        for i in range(source_length + 1):
            edit_distance[i][0] = i

        # Fill table with minimum operations
        for i in range(1, source_length + 1):
            for j in range(1, target_length + 1):
                source_char = word1[i - 1]
                target_char = word2[j - 1]

                if source_char == target_char:
                    # Characters match: no operation needed
                    edit_distance[i][j] = edit_distance[i - 1][j - 1]
                else:
                    # Take minimum of three operations
                    replace_cost = edit_distance[i - 1][j - 1] + 1
                    delete_cost = edit_distance[i - 1][j] + 1
                    insert_cost = edit_distance[i][j - 1] + 1

                    edit_distance[i][j] = min(replace_cost, delete_cost, insert_cost)

        return edit_distance[source_length][target_length]
```

### Space-Optimized Implementation

```python
class SolutionEditDistanceOptimized:
    def minDistance(self, word1: str, word2: str) -> int:
        """
        Space-optimized edit distance using single row + diagonal variable.

        Tricky part: We need dp[i-1][j-1] (diagonal) but we're overwriting it.
        Solution: Save diagonal before overwriting.

        Time: O(m * n)
        Space: O(n)
        """
        source_length = len(word1)
        target_length = len(word2)

        # Previous row: represents dp[i-1][*]
        previous_row: list[int] = list(range(target_length + 1))

        for i in range(1, source_length + 1):
            # Save dp[i-1][0] before overwriting (needed for diagonal)
            diagonal = previous_row[0]
            previous_row[0] = i  # Base case: i deletions

            for j in range(1, target_length + 1):
                # Save current value (will be diagonal for next iteration)
                next_diagonal = previous_row[j]

                if word1[i - 1] == word2[j - 1]:
                    previous_row[j] = diagonal
                else:
                    previous_row[j] = 1 + min(
                        diagonal,           # replace
                        previous_row[j],    # delete (was dp[i-1][j])
                        previous_row[j - 1] # insert
                    )

                diagonal = next_diagonal

        return previous_row[target_length]
```

### Trace Example

```
word1 = "horse", word2 = "ros"

DP Table:
        ""   r    o    s
    ┌────┬────┬────┬────┐
 "" │ 0  │ 1  │ 2  │ 3  │  ← insertions needed
    ├────┼────┼────┼────┤
 h  │ 1  │ 1  │ 2  │ 3  │  ← replace h->r
    ├────┼────┼────┼────┤
 o  │ 2  │ 2  │ 1  │ 2  │  ← 'o' matches
    ├────┼────┼────┼────┤
 r  │ 3  │ 2  │ 2  │ 2  │  ← 'r' matches (but different position)
    ├────┼────┼────┼────┤
 s  │ 4  │ 3  │ 3  │ 2  │  ← 's' matches
    ├────┼────┼────┼────┤
 e  │ 5  │ 4  │ 4  │ 3  │  ← delete 'e'
    └────┴────┴────┴────┘

Answer: dp[5][3] = 3
Operations: horse -> rorse (replace 'h') -> rose (delete 'r') -> ros (delete 'e')
```

### Key Insights

1. **Symmetric**: edit_distance(a, b) == edit_distance(b, a)
2. **Triangle Inequality**: edit_distance(a, c) <= edit_distance(a, b) + edit_distance(b, c)
3. **Applications**: Spell checking, DNA alignment, plagiarism detection
4. **Variants**: Weighted operations, only certain operations allowed


