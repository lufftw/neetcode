## Variant: Assign Cookies (LeetCode 455)

> **Problem**: Maximize children satisfied with cookies. Child i needs greed[i], cookie j has size[j].
> **Invariant**: Sort both arrays; match smallest satisfiable child with smallest sufficient cookie.
> **Delta from Base**: Sorting + two-pointer greedy matching.

### Implementation

```python
class Solution:
    """
    Sort + Greedy Match: Satisfy least greedy children first.

    Key Insight:
    - Sort children by greed (ascending)
    - Sort cookies by size (ascending)
    - Match smallest sufficient cookie to each child
    - Never "waste" a large cookie on a less greedy child

    Greedy Choice: Always try to satisfy the least greedy unsatisfied child
    with the smallest cookie that works.

    Time: O(n log n + m log m) | Space: O(1) excluding sort
    """
    def findContentChildren(self, greed: List[int], cookies: List[int]) -> int:
        greed.sort()
        cookies.sort()

        child_index = 0
        cookie_index = 0
        satisfied_count = 0

        while child_index < len(greed) and cookie_index < len(cookies):
            # Current cookie can satisfy current child
            if cookies[cookie_index] >= greed[child_index]:
                satisfied_count += 1
                child_index += 1      # Move to next child
                cookie_index += 1     # Use this cookie
            else:
                # Cookie too small, try next (larger) cookie
                cookie_index += 1

        return satisfied_count
```

### Why Greedy Works

**Greedy Choice Property**: If cookie `c` can satisfy child `g`, and `c` is the smallest such cookie, we should use it.

Proof by exchange: If we use a larger cookie `c'` for child `g`, we might not be able to satisfy a greedier child later who needs `c' > c`.

**Optimal Substructure**: After matching (child, cookie), the remaining problem is identical but smaller.

### Trace Example

```
greed:   [1, 2, 3]  (sorted)
cookies: [1, 1]     (sorted)

cookie=1 >= greed=1 → satisfy, child=1, cookie=1, count=1
cookie=1 < greed=2  → skip cookie, cookie=2
No more cookies

Result: 1 child satisfied
```

### Pattern: Sort + Match

This is a common greedy pattern:
1. Sort both sequences
2. Use two pointers to match
3. Greedy choice: match smallest that works

Similar problems:
- LC 1029 (Two City Scheduling)
- LC 870 (Advantage Shuffle)
- Meeting room assignments


