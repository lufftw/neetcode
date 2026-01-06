## Base Template: Climbing Stairs (LeetCode 70)

> **Problem**: Count the number of distinct ways to climb n stairs, taking 1 or 2 steps at a time.
> **State**: `dp[i]` = number of ways to reach step i.
> **Role**: BASE TEMPLATE for additive 1D DP.

### Implementation

```python
class Solution:
    """
    1D DP: Count ways to reach each step.

    State: dp[i] = number of distinct ways to reach step i
    Transition: dp[i] = dp[i-1] + dp[i-2]
        - Can reach step i from step (i-1) with 1 step
        - Can reach step i from step (i-2) with 2 steps
    Base: dp[0] = 1 (one way to stay at ground)
          dp[1] = 1 (one way to reach step 1)

    This is exactly the Fibonacci sequence!

    Time: O(n) | Space: O(1) with optimization
    """
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n

        # Space-optimized: only need last two values
        prev2 = 1  # dp[i-2]
        prev1 = 2  # dp[i-1]

        for step in range(3, n + 1):
            current = prev1 + prev2
            prev2 = prev1
            prev1 = current

        return prev1
```

### Why This Works

The key insight: to reach step `i`, you must have been at step `i-1` or `i-2`.
- From `i-1`: take 1 step → contributes `dp[i-1]` ways
- From `i-2`: take 2 steps → contributes `dp[i-2]` ways

Total ways = sum of both options.

### Trace Example

```
n = 5

Step 0: 1 way (stay at ground)
Step 1: 1 way (one 1-step)
Step 2: 2 ways (1+1 or 2)
Step 3: 3 ways (1+1+1, 1+2, 2+1)
Step 4: 5 ways
Step 5: 8 ways

Result: 8
```

### Edge Cases

| Case | Input | Output | Handling |
|------|-------|--------|----------|
| Single step | n=1 | 1 | Base case |
| Two steps | n=2 | 2 | Base case |
| Zero steps | n=0 | 1 | One way to stay |


