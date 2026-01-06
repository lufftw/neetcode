# DP 1D Linear Pattern

## Table of Contents

1. [API Kernel: `DP1DLinear`](#1-api-kernel-dp1dlinear)
2. [The 1D DP Backbone](#2-the-1d-dp-backbone)
3. [Two Fundamental Patterns](#3-two-fundamental-patterns)
4. [Space Optimization](#4-space-optimization)
5. [Key Insight: The "Include or Exclude" Decision](#5-key-insight-the-include-or-exclude-decision)
6. [Base Template: Climbing Stairs (LeetCode 70)](#6-base-template-climbing-stairs-leetcode-70)
7. [Variant: Min Cost Climbing Stairs (LeetCode 746)](#7-variant-min-cost-climbing-stairs-leetcode-746)
8. [Variant: House Robber (LeetCode 198)](#8-variant-house-robber-leetcode-198)
9. [Variant: House Robber II (LeetCode 213)](#9-variant-house-robber-ii-leetcode-213)
10. [Variant: Best Time to Buy and Sell Stock (LeetCode 121)](#10-variant-best-time-to-buy-and-sell-stock-leetcode-121)
11. [Pattern Comparison](#11-pattern-comparison)
12. [Decision Flowchart](#12-decision-flowchart)
13. [Template Quick Reference](#13-template-quick-reference)

---

## 1. API Kernel: `DP1DLinear`

> **Core Mechanism**: Build optimal solutions by combining optimal solutions to smaller subproblems along a single dimension.

**DP 1D Linear** covers dynamic programming problems where the state depends on a single dimension (typically array index or step count). The pattern follows a consistent backbone: define state, establish transitions, handle base cases, and optionally optimize space.

---

## 2. The 1D DP Backbone

Every 1D linear DP problem follows this structure:

| Component | Question to Answer | Example (Climbing Stairs) |
|-----------|-------------------|---------------------------|
| **State** | What does `dp[i]` represent? | Number of ways to reach step i |
| **Transition** | How does `dp[i]` relate to previous states? | `dp[i] = dp[i-1] + dp[i-2]` |
| **Base Case** | What are the initial values? | `dp[0] = 1, dp[1] = 1` |
| **Answer** | Where is the final answer? | `dp[n]` |
| **Space Optimization** | Can we reduce O(n) to O(1)? | Yes, only need last 2 values |

---

## 3. Two Fundamental Patterns

| Pattern | State Definition | Transition Logic | Problems |
|---------|------------------|------------------|----------|
| **Additive (Count)** | `dp[i]` = ways to reach i | Add from all valid previous states | LC 70, 746 |
| **Selective (Max/Min)** | `dp[i]` = optimal value at i | Choose best among options | LC 198, 213, 121 |

---

## 4. Space Optimization

Most 1D DP problems can be optimized from O(n) to O(1) space:

```python
# O(n) space
dp = [0] * (n + 1)
for i in range(2, n + 1):
    dp[i] = dp[i-1] + dp[i-2]
return dp[n]

# O(1) space
prev2, prev1 = 1, 1
for i in range(2, n + 1):
    prev2, prev1 = prev1, prev2 + prev1
return prev1
```

---

## 5. Key Insight: The "Include or Exclude" Decision

Many 1D DP problems boil down to one question at each step:
- **Include** current element (and skip some previous elements)
- **Exclude** current element (and take the result from previous)

This creates the classic transition: `dp[i] = max(dp[i-1], dp[i-2] + value[i])`

---

---

## 6. Base Template: Climbing Stairs (LeetCode 70)

> **Problem**: Count the number of distinct ways to climb n stairs, taking 1 or 2 steps at a time.
> **State**: `dp[i]` = number of ways to reach step i.
> **Role**: BASE TEMPLATE for additive 1D DP.

### 6.1 Implementation

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

### 6.2 Why This Works

The key insight: to reach step `i`, you must have been at step `i-1` or `i-2`.
- From `i-1`: take 1 step → contributes `dp[i-1]` ways
- From `i-2`: take 2 steps → contributes `dp[i-2]` ways

Total ways = sum of both options.

### 6.3 Trace Example

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

### 6.4 Edge Cases

| Case | Input | Output | Handling |
|------|-------|--------|----------|
| Single step | n=1 | 1 | Base case |
| Two steps | n=2 | 2 | Base case |
| Zero steps | n=0 | 1 | One way to stay |

---

## 7. Variant: Min Cost Climbing Stairs (LeetCode 746)

> **Problem**: Find minimum cost to reach the top of stairs, where each step has a cost.
> **State**: `dp[i]` = minimum cost to reach step i.
> **Delta from Base**: Add cost to transition, minimize instead of sum.

### 7.1 Implementation

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

### 7.2 Key Difference from Base

| Aspect | Climbing Stairs (LC 70) | Min Cost Climbing (LC 746) |
|--------|-------------------------|----------------------------|
| Goal | Count ways | Minimize cost |
| Operation | Addition (sum paths) | Minimum (best path) + cost |
| Final answer | `dp[n]` | `min(dp[n-1], dp[n-2])` |

### 7.3 Why Return `min(prev1, prev2)`?

The "top" is beyond the last stair. You can reach it by:
- Taking 1 step from stair `n-1`
- Taking 2 steps from stair `n-2`

No additional cost to "step off" the stairs.

### 7.4 Trace Example

```
cost: [10, 15, 20]

dp[0] = 10 (pay 10 to step on first stair)
dp[1] = 15 (pay 15 to step on second stair)
dp[2] = min(15, 10) + 20 = 30

Top = min(dp[2], dp[1]) = min(30, 15) = 15

Path: Start at step 1 (pay 15), take 2 steps to top.
```

---

## 8. Variant: House Robber (LeetCode 198)

> **Problem**: Maximize loot from non-adjacent houses (can't rob two consecutive houses).
> **State**: `dp[i]` = maximum loot considering houses 0 to i.
> **Delta from Base**: Include/exclude decision at each house.

### 8.1 Implementation

```python
class Solution:
    """
    1D DP: Include/Exclude decision at each step.

    State: dp[i] = maximum loot from houses[0..i]
    Transition: dp[i] = max(
        dp[i-1],           # Skip current house, keep previous best
        dp[i-2] + nums[i]  # Rob current house, add to best before adjacent
    )
    Base: dp[0] = nums[0], dp[1] = max(nums[0], nums[1])

    The classic "take or skip" pattern.

    Time: O(n) | Space: O(1)
    """
    def rob(self, nums: List[int]) -> int:
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]

        # Space-optimized
        prev2 = nums[0]                    # Best up to house i-2
        prev1 = max(nums[0], nums[1])      # Best up to house i-1

        for i in range(2, len(nums)):
            current = max(prev1, prev2 + nums[i])
            prev2 = prev1
            prev1 = current

        return prev1
```

### 8.2 The Include/Exclude Framework

At each house, you have two choices:
1. **Skip** (exclude): Take whatever you had before → `dp[i-1]`
2. **Rob** (include): Take this house + best non-adjacent → `dp[i-2] + nums[i]`

This framework applies to many DP problems!

### 8.3 Trace Example

```
nums: [2, 7, 9, 3, 1]

i=0: prev2 = 2
i=1: prev1 = max(2, 7) = 7
i=2: current = max(7, 2+9) = 11, prev2=7, prev1=11
i=3: current = max(11, 7+3) = 11, prev2=11, prev1=11
i=4: current = max(11, 11+1) = 12

Result: 12 (rob houses 0, 2, 4 → 2+9+1=12)
```

### 8.4 Edge Cases

| Case | Input | Output | Handling |
|------|-------|--------|----------|
| Single house | [5] | 5 | Base case |
| Two houses | [2, 3] | 3 | max of both |
| All same value | [1, 1, 1, 1] | 2 | Rob alternate |

---

## 9. Variant: House Robber II (LeetCode 213)

> **Problem**: Houses are arranged in a circle; first and last house are adjacent.
> **State**: Same as House Robber, but handle circular constraint.
> **Delta from Base**: Split into two subproblems to avoid circular conflict.

### 9.1 Implementation

```python
class Solution:
    """
    Circular DP: Split into two linear subproblems.

    Key Insight: First and last houses are adjacent, so we can't rob both.
    Solution: Take the maximum of two scenarios:
        1. Rob houses[0..n-2] (exclude last house)
        2. Rob houses[1..n-1] (exclude first house)

    This transforms circular DP into two linear DP problems.

    Time: O(n) | Space: O(1)
    """
    def rob(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return nums[0]

        # Helper: linear house robber on subarray
        def rob_linear(houses: List[int]) -> int:
            if not houses:
                return 0
            if len(houses) == 1:
                return houses[0]

            prev2 = houses[0]
            prev1 = max(houses[0], houses[1])

            for i in range(2, len(houses)):
                current = max(prev1, prev2 + houses[i])
                prev2 = prev1
                prev1 = current

            return prev1

        # Two scenarios: exclude last OR exclude first
        return max(
            rob_linear(nums[:-1]),  # Houses 0 to n-2
            rob_linear(nums[1:])   # Houses 1 to n-1
        )
```

### 9.2 Why Split Works

The circular constraint means: "Don't rob both first and last."

By splitting into two ranges:
- `[0, n-2]`: First house is eligible, last is excluded → no conflict
- `[1, n-1]`: Last house is eligible, first is excluded → no conflict

One of these must contain the optimal solution.

### 9.3 Trace Example

```
nums: [2, 3, 2]

Scenario 1: nums[0..1] = [2, 3] → max = 3
Scenario 2: nums[1..2] = [3, 2] → max = 3

Result: max(3, 3) = 3
(Can't rob all three because first and last are adjacent)
```

### 9.4 Pattern: Circular → Linear Decomposition

This technique generalizes:
- Circular array problems often decompose into linear subproblems
- Break the circle by fixing one element's state (include/exclude)

---

## 10. Variant: Best Time to Buy and Sell Stock (LeetCode 121)

> **Problem**: Find maximum profit from one buy-sell transaction.
> **State**: Track minimum price seen so far.
> **Delta from Base**: Implicit DP with running minimum.

### 10.1 Implementation

```python
class Solution:
    """
    Implicit 1D DP: Track best buy price for each potential sell day.

    Key Insight: For each day as potential sell day, the best buy day
    is the minimum price seen before it.

    State (implicit): min_price = lowest price up to current day
    Transition: max_profit = max(max_profit, price - min_price)

    Time: O(n) | Space: O(1)
    """
    def maxProfit(self, prices: List[int]) -> int:
        min_price = float('inf')
        max_profit = 0

        for price in prices:
            # Update best buy price seen so far
            min_price = min(min_price, price)

            # Calculate profit if we sell today
            profit_if_sell_today = price - min_price

            # Update best profit
            max_profit = max(max_profit, profit_if_sell_today)

        return max_profit
```

### 10.2 Why This is 1D DP

The explicit DP formulation:
- `dp[i]` = maximum profit achievable selling on or before day i
- `min_so_far[i]` = minimum price in days 0 to i

Transition: `dp[i] = max(dp[i-1], prices[i] - min_so_far[i])`

We optimize away the array since we only need the previous values.

### 10.3 Connection to House Robber Pattern

| Problem | Track | Decision |
|---------|-------|----------|
| House Robber | Best loot so far | Include or exclude current |
| Stock Buy/Sell | Min price so far | Sell today or wait |

Both follow the "optimal prefix" pattern.

### 10.4 Trace Example

```
prices: [7, 1, 5, 3, 6, 4]

Day 0: min=7, profit=0
Day 1: min=1, profit=0 (would be negative)
Day 2: min=1, profit=4 (buy at 1, sell at 5)
Day 3: min=1, profit=4
Day 4: min=1, profit=5 (buy at 1, sell at 6)
Day 5: min=1, profit=5

Result: 5
```

### 10.5 Edge Cases

| Case | Input | Output | Handling |
|------|-------|--------|----------|
| Decreasing prices | [7, 6, 4, 3, 1] | 0 | Never sell (profit would be negative) |
| Single day | [5] | 0 | Can't complete transaction |
| Two days, profit | [1, 5] | 4 | Buy day 0, sell day 1 |

---

---

## 11. Pattern Comparison

### 11.1 1D DP vs Greedy

| Aspect | 1D Linear DP | Greedy |
|--------|--------------|--------|
| **Decision** | Considers all subproblems | Local optimal only |
| **Structure** | Overlapping subproblems | Greedy choice property |
| **Example** | House Robber (need dp) | Jump Game (greedy works) |
| **When to use** | Can't prove greedy correctness | Clear greedy choice |

### 11.2 1D DP vs 2D DP

| Aspect | 1D Linear DP | 2D DP |
|--------|--------------|-------|
| **State** | Single dimension | Two dimensions |
| **Space** | O(n) → O(1) | O(n*m) → O(n) |
| **Examples** | Climbing Stairs, House Robber | Longest Common Subsequence |
| **Complexity** | Linear transitions | Matrix transitions |

### 11.3 Additive vs Selective 1D DP

| Pattern | Goal | Operator | Example |
|---------|------|----------|---------|
| **Additive** | Count ways | Sum | LC 70 (Climbing Stairs) |
| **Selective** | Optimize value | Max/Min | LC 198 (House Robber) |

### 11.4 Space Optimization Summary

| Pattern | Original | Optimized | Key Observation |
|---------|----------|-----------|-----------------|
| Fibonacci-like | O(n) | O(1) | Only need last 2 values |
| Kadane-style | O(n) | O(1) | Only need running best |
| Include/Exclude | O(n) | O(1) | Only need last 2 values |

---

---

## 12. Decision Flowchart

```
Start: "Optimization over a sequence?"
       │
       ▼
  ┌─────────────────────┐
  │ Count ways to       │
  │ reach end/target?   │───Yes──▶ Additive DP (LC 70, 746)
  └─────────────────────┘          dp[i] = sum of valid previous states
       │ No
       ▼
  ┌─────────────────────┐
  │ Maximize/Minimize   │
  │ with adjacency      │───Yes──▶ Include/Exclude DP (LC 198, 213)
  │ constraint?         │          dp[i] = max(dp[i-1], dp[i-2] + val)
  └─────────────────────┘
       │ No
       ▼
  ┌─────────────────────┐
  │ Track running       │
  │ min/max prefix?     │───Yes──▶ Implicit DP / Kadane-style (LC 121)
  └─────────────────────┘
       │ No
       ▼
  ┌─────────────────────┐
  │ Circular array      │
  │ constraint?         │───Yes──▶ Split into linear subproblems (LC 213)
  └─────────────────────┘
       │ No
       ▼
  Consider 2D DP or other patterns
```

### 12.1 Pattern Selection Guide

| Problem Signal | Pattern | Example |
|----------------|---------|---------|
| "Number of ways" | Additive DP | LC 70 |
| "Minimum cost to reach" | Min DP | LC 746 |
| "Can't take adjacent" | Include/Exclude | LC 198 |
| "Circular arrangement" | Split + Linear DP | LC 213 |
| "One transaction" | Running min/max | LC 121 |

### 12.2 State Definition Checklist

When defining `dp[i]`, ask:
1. What does the index `i` represent? (step, house, day)
2. What value does `dp[i]` hold? (count, max, min)
3. What are valid transitions to `dp[i]`?
4. What are the base cases?
5. Where is the final answer? (`dp[n]`, `dp[n-1]`, `max(dp)`)

### 12.3 Space Optimization Decision

| Question | If Yes | If No |
|----------|--------|-------|
| Transition uses only last k states? | Optimize to O(k) | Keep O(n) array |
| Need to reconstruct path? | Keep full array | Can optimize |
| Multiple queries on same array? | Keep prefix array | Can optimize |

---

---

## 13. Template Quick Reference

### 13.1 1. Fibonacci-Style (Count Ways)

```python
def count_ways(n: int) -> int:
    """Count ways to reach step n (1 or 2 steps at a time)."""
    if n <= 2:
        return n

    prev2, prev1 = 1, 2
    for i in range(3, n + 1):
        prev2, prev1 = prev1, prev2 + prev1

    return prev1
```

### 13.2 2. Min Cost Path

```python
def min_cost(costs: List[int]) -> int:
    """Minimum cost to reach beyond last step."""
    n = len(costs)
    if n == 1:
        return costs[0]

    prev2 = costs[0]
    prev1 = costs[1]

    for i in range(2, n):
        current = min(prev1, prev2) + costs[i]
        prev2, prev1 = prev1, current

    return min(prev1, prev2)
```

### 13.3 3. Include/Exclude (House Robber)

```python
def max_non_adjacent(nums: List[int]) -> int:
    """Maximum sum of non-adjacent elements."""
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]

    prev2 = nums[0]
    prev1 = max(nums[0], nums[1])

    for i in range(2, len(nums)):
        current = max(prev1, prev2 + nums[i])
        prev2, prev1 = prev1, current

    return prev1
```

### 13.4 4. Circular Array Decomposition

```python
def max_circular(nums: List[int]) -> int:
    """Maximum non-adjacent sum in circular array."""
    if len(nums) == 1:
        return nums[0]

    def max_linear(arr: List[int]) -> int:
        if len(arr) == 1:
            return arr[0]
        prev2 = arr[0]
        prev1 = max(arr[0], arr[1])
        for i in range(2, len(arr)):
            prev2, prev1 = prev1, max(prev1, prev2 + arr[i])
        return prev1

    return max(
        max_linear(nums[:-1]),  # Exclude last
        max_linear(nums[1:])    # Exclude first
    )
```

### 13.5 5. Running Min/Max (Kadane-Style)

```python
def max_profit_single_transaction(prices: List[int]) -> int:
    """Maximum profit from single buy-sell."""
    min_price = float('inf')
    max_profit = 0

    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)

    return max_profit
```

### 13.6 6. Generic 1D DP Template

```python
def solve_1d_dp(arr: List[int], combine, initial_values: List) -> int:
    """
    Generic 1D DP template.

    Args:
        arr: Input array
        combine: Function (prev2, prev1, current_val) -> new_value
        initial_values: Base case values [dp[0], dp[1], ...]
    """
    n = len(arr)
    if n <= len(initial_values):
        return initial_values[n - 1] if n > 0 else 0

    # Initialize from base cases
    prev_values = initial_values[:]

    for i in range(len(initial_values), n):
        new_value = combine(prev_values, arr[i])
        prev_values.pop(0)
        prev_values.append(new_value)

    return prev_values[-1]
```

### 13.7 Variable Naming Convention

| Variable | Purpose | Example |
|----------|---------|---------|
| `prev2` / `prev1` | Space-optimized DP values | `prev2, prev1 = prev1, current` |
| `current` | Current DP value being computed | `current = max(prev1, prev2 + val)` |
| `min_price` / `max_val` | Running minimum/maximum | `min_price = min(min_price, price)` |
| `dp[i]` | DP array (when not optimized) | `dp[i] = dp[i-1] + dp[i-2]` |



---



*Document generated for NeetCode Practice Framework — API Kernel: dp_1d_linear*
