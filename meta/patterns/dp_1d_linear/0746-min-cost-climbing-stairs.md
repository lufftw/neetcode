## Variant: Min Cost Climbing Stairs (LeetCode 746)

> **Problem**: Find minimum cost to reach the top of stairs, where each step has a cost.
> **State**: `dp[i]` = minimum cost to reach step i.
> **Delta from Base**: Add cost to transition, minimize instead of sum.

### Implementation

```python
class Solution:
    """
    1D DP: Minimize cost to reach each step.

    State: dp[i] = minimum cost to reach step i
    Transition: dp[i] = min(dp[i-1], dp[i-2]) + cost[i]
        - Pay cost[i] to step on this stair
        - Choose cheaper path from (i-1) or (i-2)
    Base: dp[0] = cost[0], dp[1] = cost[1]
        - Must pay cost to start from step 0 or 1

    Note: "Top" is beyond the last stair (index n).

    Time: O(n) | Space: O(1)
    """
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        n = len(cost)

        # Space-optimized
        prev2 = cost[0]  # Cost to reach step 0
        prev1 = cost[1]  # Cost to reach step 1

        for i in range(2, n):
            current = min(prev1, prev2) + cost[i]
            prev2 = prev1
            prev1 = current

        # Can reach top from either last or second-to-last step
        return min(prev1, prev2)
```

### Key Difference from Base

| Aspect | Climbing Stairs (LC 70) | Min Cost Climbing (LC 746) |
|--------|-------------------------|----------------------------|
| Goal | Count ways | Minimize cost |
| Operation | Addition (sum paths) | Minimum (best path) + cost |
| Final answer | `dp[n]` | `min(dp[n-1], dp[n-2])` |

### Why Return `min(prev1, prev2)`?

The "top" is beyond the last stair. You can reach it by:
- Taking 1 step from stair `n-1`
- Taking 2 steps from stair `n-2`

No additional cost to "step off" the stairs.

### Trace Example

```
cost: [10, 15, 20]

dp[0] = 10 (pay 10 to step on first stair)
dp[1] = 15 (pay 15 to step on second stair)
dp[2] = min(15, 10) + 20 = 30

Top = min(dp[2], dp[1]) = min(30, 15) = 15

Path: Start at step 1 (pay 15), take 2 steps to top.
```


