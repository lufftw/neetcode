## Variant: Candy (LeetCode 135)

> **Problem**: Distribute candies to children in a line so higher-rated children get more than neighbors.
> **Invariant**: Two-pass greedy ensures both left and right neighbor constraints.
> **Delta from Base**: Two-pass scanning (forward + backward).

### Implementation

```python
class Solution:
    """
    Two-Pass Greedy: Satisfy left constraint, then right constraint.

    Key Insight:
    - Single pass can't handle both directions simultaneously
    - Forward pass: ensure higher rating than LEFT neighbor → more candy
    - Backward pass: ensure higher rating than RIGHT neighbor → more candy
    - Take max of both constraints at each position

    Greedy Choice: Give minimum candy that satisfies constraints.

    Time: O(n) | Space: O(n)
    """
    def candy(self, ratings: List[int]) -> int:
        n = len(ratings)
        candies = [1] * n  # Everyone gets at least 1

        # Forward pass: satisfy left neighbor constraint
        for i in range(1, n):
            if ratings[i] > ratings[i - 1]:
                candies[i] = candies[i - 1] + 1

        # Backward pass: satisfy right neighbor constraint
        for i in range(n - 2, -1, -1):
            if ratings[i] > ratings[i + 1]:
                # Take max to preserve forward pass constraint
                candies[i] = max(candies[i], candies[i + 1] + 1)

        return sum(candies)
```

### Why Two Passes Are Necessary

Single pass fails because we don't know future ratings:

```
ratings: [1, 3, 2, 1]

Forward only: [1, 2, 1, 1]
             Problem: index 2 (rating=2) has same candy as index 3 (rating=1)

Backward only: [1, 3, 2, 1]
              Problem: index 0 (rating=1) has same candy as index 1 (rating=3)

Both passes: [1, 3, 2, 1] ✓
             Forward:  [1, 2, 1, 1]
             Backward: [1, 3, 2, 1] (max of both)
```

### Trace Example

```
ratings:  [1, 0, 2]

Forward pass (left constraint):
  i=1: ratings[1]=0 <= ratings[0]=1 → candies[1]=1
  i=2: ratings[2]=2 > ratings[1]=0  → candies[2]=2
  candies: [1, 1, 2]

Backward pass (right constraint):
  i=1: ratings[1]=0 <= ratings[2]=2 → candies[1]=1
  i=0: ratings[0]=1 > ratings[1]=0  → candies[0]=max(1, 1+1)=2
  candies: [2, 1, 2]

Result: 2 + 1 + 2 = 5
```

### Optimization: O(1) Space

Can use slope counting (peaks and valleys) for O(1) space, but the two-pass approach is clearer and sufficient for interviews.


