# DP Knapsack / Subset Pattern

## Table of Contents

1. [API Kernel: `DPKnapsackSubset`](#1-api-kernel-dpknapsacksubset)
2. [The "Take or Skip" Decision](#2-the-take-or-skip-decision)
3. [Two Major Variants](#3-two-major-variants)
4. [State Definition Patterns](#4-state-definition-patterns)
5. [When DP vs Backtracking?](#5-when-dp-vs-backtracking)
6. [Space Optimization](#6-space-optimization)
7. [Base Template: Partition Equal Subset Sum (LeetCode 416)](#7-base-template-partition-equal-subset-sum-leetcode-416)
8. [Variant: Target Sum (LeetCode 494)](#8-variant-target-sum-leetcode-494)
9. [Variant: Coin Change (LeetCode 322)](#9-variant-coin-change-leetcode-322)
10. [Variant: Coin Change 2 (LeetCode 518)](#10-variant-coin-change-2-leetcode-518)
11. [Pattern Comparison](#11-pattern-comparison)
12. [Decision Flowchart](#12-decision-flowchart)
13. [Template Quick Reference](#13-template-quick-reference)

---

## 1. API Kernel: `DPKnapsackSubset`

> **Core Mechanism**: Make "take or skip" decisions on items to reach a target capacity or sum.

**DP Knapsack/Subset** covers dynamic programming problems where you select items from a collection to achieve a goal. The fundamental question at each item: **"Should I include this item or not?"**

---

## 2. The "Take or Skip" Decision

Every knapsack/subset problem reduces to this choice at each item:

| Decision | Effect | Transition |
|----------|--------|------------|
| **Take** | Add item to selection, reduce remaining capacity | `dp[i][c] = ... dp[i-1][c - weight[i]] + value[i]` |
| **Skip** | Don't use item, keep capacity | `dp[i][c] = dp[i-1][c]` |

---

## 3. Two Major Variants

| Variant | Item Reuse | Iteration Order | Examples |
|---------|------------|-----------------|----------|
| **0/1 Knapsack** | Each item used at most once | Items outer, capacity inner (reverse for 1D) | LC 416, 494 |
| **Unbounded Knapsack** | Items can be reused | Items outer, capacity inner (forward for 1D) | LC 322, 518 |

---

## 4. State Definition Patterns

| Goal | State | Transition |
|------|-------|------------|
| **Can reach target?** | `dp[c]` = True/False for capacity c | `dp[c] = dp[c] or dp[c - item]` |
| **Count ways to reach** | `dp[c]` = number of ways | `dp[c] += dp[c - item]` |
| **Minimize items to reach** | `dp[c]` = min items needed | `dp[c] = min(dp[c], dp[c - item] + 1)` |

---

## 5. When DP vs Backtracking?

| Use DP | Use Backtracking |
|--------|------------------|
| Need count/min/max of ALL valid selections | Need to enumerate actual selections |
| Target sum is bounded (fits in DP table) | Target is too large for DP table |
| Overlapping subproblems (same target reached multiple ways) | Few/no overlapping subproblems |

**Rule of Thumb**: If "number of ways" or "minimum count," use DP. If "list all combinations," use backtracking.

---

## 6. Space Optimization

Most 2D knapsack DP can be reduced to 1D:

```python
# 2D version
dp = [[0] * (target + 1) for _ in range(n + 1)]
for i in range(1, n + 1):
    for c in range(target + 1):
        dp[i][c] = dp[i-1][c]  # skip
        if c >= nums[i-1]:
            dp[i][c] = max(dp[i][c], dp[i-1][c - nums[i-1]] + nums[i-1])  # take

# 1D version (iterate capacity backwards for 0/1 knapsack)
dp = [0] * (target + 1)
for num in nums:
    for c in range(target, num - 1, -1):  # backwards!
        dp[c] = max(dp[c], dp[c - num] + num)
```

**Why backwards for 0/1?** To ensure each item is used at most once per iteration.

---

## 7. Base Template: Partition Equal Subset Sum (LeetCode 416)

> **Problem**: Can array be partitioned into two subsets with equal sum?
> **State**: `dp[s]` = True if sum s is achievable.
> **Role**: BASE TEMPLATE for 0/1 subset sum.

### 7.1 Implementation

```python
class Solution:
    """
    0/1 Knapsack: Can we select items to reach target sum?

    Key Insight: If total sum is S, we need to find a subset summing to S/2.
    If such a subset exists, the remaining elements also sum to S/2.

    State: dp[s] = True if sum s is achievable using some subset
    Transition: dp[s] = dp[s] or dp[s - num] (take or skip)
    Base: dp[0] = True (empty subset has sum 0)

    Why iterate backwards? Each number can only be used once.
    Forward iteration would use the same number multiple times.

    Time: O(n * sum) | Space: O(sum)
    """
    def canPartition(self, nums: List[int]) -> bool:
        total = sum(nums)

        # Odd sum can't be split evenly
        if total % 2 != 0:
            return False

        target = total // 2
        dp = [False] * (target + 1)
        dp[0] = True  # Empty subset

        for num in nums:
            # Iterate backwards to ensure each num used at most once
            for s in range(target, num - 1, -1):
                dp[s] = dp[s] or dp[s - num]

        return dp[target]
```

### 7.2 Why Backwards Iteration?

Consider `nums = [1, 5, 5]`, target = 5:

**Forward (wrong for 0/1):**
```
dp = [T, F, F, F, F, F]
num = 1: dp[1] = dp[0] = T → [T, T, F, F, F, F]
         dp[2] = dp[1] = T → [T, T, T, F, F, F]  # Used 1 twice!
```

**Backwards (correct):**
```
dp = [T, F, F, F, F, F]
num = 1: dp[1] = dp[0] = T → [T, T, F, F, F, F]
num = 5: dp[5] = dp[0] = T → [T, T, F, F, F, T]
```

### 7.3 Trace Example

```
nums: [1, 5, 11, 5], total = 22, target = 11

dp = [T, F, F, F, F, F, F, F, F, F, F, F]

num=1:  dp[1] = T
num=5:  dp[6] = dp[1] = T, dp[5] = dp[0] = T
num=11: dp[11] = dp[0] = T ✓

Result: True (subsets: {11} and {1,5,5})
```

---

## 8. Variant: Target Sum (LeetCode 494)

> **Problem**: Count ways to assign +/- to each number to reach target sum.
> **State**: `dp[s]` = number of ways to reach sum s.
> **Delta from Base**: Count instead of boolean, transform to subset sum.

### 8.1 Implementation

```python
class Solution:
    """
    0/1 Knapsack: Count ways to reach target.

    Key Insight: Transform +/- assignment to subset selection.
    - Let P = sum of numbers with + sign
    - Let N = sum of numbers with - sign
    - P - N = target, P + N = total
    - Therefore: P = (target + total) / 2

    We need to count subsets summing to P (positive group).

    State: dp[s] = number of ways to form sum s
    Transition: dp[s] += dp[s - num]
    Base: dp[0] = 1 (one way: empty subset)

    Time: O(n * sum) | Space: O(sum)
    """
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        total = sum(nums)

        # Check feasibility
        if (total + target) % 2 != 0 or total + target < 0:
            return 0

        subset_sum = (total + target) // 2
        dp = [0] * (subset_sum + 1)
        dp[0] = 1  # One way to form sum 0

        for num in nums:
            # Backwards for 0/1 (each number used once)
            for s in range(subset_sum, num - 1, -1):
                dp[s] += dp[s - num]

        return dp[subset_sum]
```

### 8.2 The Transformation Trick

The problem says: assign + or - to each number.
- Numbers with + form set P
- Numbers with - form set N

Equations:
- P - N = target (given)
- P + N = total (sum of all)

Solving: P = (target + total) / 2

**This transforms the problem into: count subsets summing to P.**

### 8.3 Trace Example

```
nums: [1, 1, 1, 1, 1], target = 3
total = 5, P = (3 + 5) / 2 = 4

Count subsets summing to 4:
- {1,1,1,1} from indices 0,1,2,3
- {1,1,1,1} from indices 0,1,2,4
- {1,1,1,1} from indices 0,1,3,4
- {1,1,1,1} from indices 0,2,3,4
- {1,1,1,1} from indices 1,2,3,4

Result: 5 ways
```

---

## 9. Variant: Coin Change (LeetCode 322)

> **Problem**: Minimum coins needed to make amount (coins can be reused).
> **State**: `dp[a]` = minimum coins to make amount a.
> **Delta from Base**: Unbounded (reuse allowed), minimize instead of count.

### 9.1 Implementation

```python
class Solution:
    """
    Unbounded Knapsack: Minimum items to reach target.

    Key Differences from 0/1:
    - Coins can be reused → iterate forwards
    - Goal is minimize → use min() instead of sum/or
    - Initialize with infinity (impossible until proven otherwise)

    State: dp[a] = minimum coins to make amount a
    Transition: dp[a] = min(dp[a], dp[a - coin] + 1)
    Base: dp[0] = 0 (zero coins for amount 0)

    Why iterate forwards? To allow reusing coins.
    dp[a - coin] might already include the current coin.

    Time: O(n * amount) | Space: O(amount)
    """
    def coinChange(self, coins: List[int], amount: int) -> int:
        # Initialize with "impossible" value
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0  # Zero coins for amount 0

        for coin in coins:
            # Forward iteration: coins can be reused
            for a in range(coin, amount + 1):
                dp[a] = min(dp[a], dp[a - coin] + 1)

        return dp[amount] if dp[amount] != float('inf') else -1
```

### 9.2 Why Forward Iteration for Unbounded?

Consider `coins = [2]`, amount = 4:

**Forward (correct for unbounded):**
```
dp = [0, inf, inf, inf, inf]
coin = 2:
  a=2: dp[2] = min(inf, dp[0]+1) = 1
  a=4: dp[4] = min(inf, dp[2]+1) = 2  # Reused coin 2!
```

**Backwards (wrong for unbounded):**
```
dp = [0, inf, inf, inf, inf]
coin = 2:
  a=4: dp[4] = min(inf, dp[2]+1) = inf  # dp[2] not yet computed
  a=2: dp[2] = min(inf, dp[0]+1) = 1
```

### 9.3 Trace Example

```
coins: [1, 2, 5], amount = 11

dp = [0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]

coin=1: dp[1]=1, dp[2]=2, ..., dp[11]=11
coin=2: dp[2]=1, dp[3]=2, dp[4]=2, ..., dp[11]=6
coin=5: dp[5]=1, dp[6]=2, dp[7]=2, ..., dp[10]=2, dp[11]=3

Result: 3 coins (5 + 5 + 1)
```

---

## 10. Variant: Coin Change 2 (LeetCode 518)

> **Problem**: Count number of ways to make amount (coins can be reused).
> **State**: `dp[a]` = number of ways to make amount a.
> **Delta from Coin Change: Count ways instead of minimize.

### 10.1 Implementation

```python
class Solution:
    """
    Unbounded Knapsack: Count ways to reach target.

    Key Insight: Same as Coin Change but counting instead of minimizing.
    - Coins can be reused → forward iteration
    - Count ways → use += instead of min()
    - Combinations (not permutations) → coins outer, amount inner

    State: dp[a] = number of ways to make amount a
    Transition: dp[a] += dp[a - coin]
    Base: dp[0] = 1 (one way to make amount 0: use no coins)

    Why coins outer loop? To count combinations, not permutations.
    Amount outer would count [1,2] and [2,1] as different.

    Time: O(n * amount) | Space: O(amount)
    """
    def change(self, amount: int, coins: List[int]) -> int:
        dp = [0] * (amount + 1)
        dp[0] = 1  # One way to make amount 0

        for coin in coins:
            # Forward for unbounded
            for a in range(coin, amount + 1):
                dp[a] += dp[a - coin]

        return dp[amount]
```

### 10.2 Combinations vs Permutations

The loop order matters:

**Coins outer (combinations):**
```python
for coin in coins:
    for a in range(coin, amount + 1):
        dp[a] += dp[a - coin]
```
→ Each coin is considered in sequence, so [1,2] and [2,1] are the same.

**Amount outer (permutations):**
```python
for a in range(1, amount + 1):
    for coin in coins:
        if coin <= a:
            dp[a] += dp[a - coin]
```
→ At each amount, all coins are considered, so [1,2] and [2,1] are different.

### 10.3 Trace Example

```
coins: [1, 2, 5], amount = 5

dp = [1, 0, 0, 0, 0, 0]

coin=1: dp = [1, 1, 1, 1, 1, 1]
        (1), (1,1), (1,1,1), (1,1,1,1), (1,1,1,1,1)

coin=2: dp = [1, 1, 2, 2, 3, 3]
        +1 way each for (2), (1,2), (2,2), (1,1,2), (1,2,2) etc.

coin=5: dp = [1, 1, 2, 2, 3, 4]
        +1 way for (5)

Result: 4 ways: (5), (2,2,1), (2,1,1,1), (1,1,1,1,1)
```

---

## 11. Pattern Comparison

### 11.1 0/1 Knapsack vs Unbounded Knapsack

| Aspect | 0/1 Knapsack | Unbounded Knapsack |
|--------|--------------|-------------------|
| **Item Usage** | Each item at most once | Items can be reused |
| **1D Iteration** | Backwards (`range(target, num-1, -1)`) | Forwards (`range(coin, amount+1)`) |
| **Examples** | LC 416, 494 | LC 322, 518 |
| **Mental Model** | Selecting from a set | Dispensing from unlimited supply |

### 11.2 DP Knapsack vs Backtracking

| Aspect | DP Knapsack | Backtracking |
|--------|-------------|--------------|
| **Returns** | Count, min, max, boolean | Actual combinations/selections |
| **Time** | O(n * target) | Exponential (but can prune) |
| **When to Use** | Need aggregate answer | Need to enumerate solutions |
| **Overlapping?** | Yes (same target from many paths) | Depends on problem |

### 11.3 Boolean vs Count vs Min/Max

| Goal | Operator | Initial Value | Transition |
|------|----------|---------------|------------|
| **Reachable?** | `or` | False, dp[0]=True | `dp[s] = dp[s] or dp[s-item]` |
| **Count ways** | `+=` | 0, dp[0]=1 | `dp[s] += dp[s-item]` |
| **Min items** | `min` | inf, dp[0]=0 | `dp[s] = min(dp[s], dp[s-item]+1)` |

---

## 12. Decision Flowchart

```
Start: "Select items to reach target/capacity?"
       │
       ▼
  ┌─────────────────────┐
  │ Can items be        │
  │ reused?             │
  └─────────────────────┘
       │
   ┌───┴───┐
   │       │
  No      Yes
   │       │
   ▼       ▼
  0/1    Unbounded
   │       │
   ▼       ▼
  ┌─────────────────────┐
  │ What's the goal?    │
  └─────────────────────┘
       │
   ┌───┼───┬───┐
   │   │   │   │
   ▼   ▼   ▼   ▼
Reach? Count Min Enumerate
   │   │   │   │
   ▼   ▼   ▼   ▼
  or  +=  min  Backtrack
```

### 12.1 Pattern Selection Guide

| Problem Signal | Pattern | Iteration |
|----------------|---------|-----------|
| "Partition into two equal subsets" | 0/1 Boolean | Backwards |
| "Number of ways with +/-" | 0/1 Count | Backwards |
| "Minimum coins" (unlimited supply) | Unbounded Min | Forwards |
| "Number of combinations" (reusable) | Unbounded Count | Forwards |
| "List all subsets" | Backtracking | N/A |

### 12.2 Iteration Direction Decision

| Question | If Yes |
|----------|--------|
| Can items be reused? | Forward iteration |
| Each item used at most once? | Backward iteration |
| Counting combinations (not permutations)? | Items outer loop |
| Counting permutations? | Amount/target outer loop |

### 12.3 Transformation Patterns

Some problems need transformation before applying knapsack:

| Original Problem | Transformation |
|------------------|----------------|
| Target Sum (+/-) | subset_sum = (total + target) / 2 |
| Partition | target = total / 2 |
| Last Stone Weight | Same as partition |

---

## 13. Template Quick Reference

### 13.1 1. 0/1 Knapsack - Boolean (Can Reach?)

```python
def can_partition(nums: List[int], target: int) -> bool:
    dp = [False] * (target + 1)
    dp[0] = True

    for num in nums:
        for s in range(target, num - 1, -1):  # Backwards!
            dp[s] = dp[s] or dp[s - num]

    return dp[target]
```

### 13.2 2. 0/1 Knapsack - Count Ways

```python
def count_subsets(nums: List[int], target: int) -> int:
    dp = [0] * (target + 1)
    dp[0] = 1

    for num in nums:
        for s in range(target, num - 1, -1):  # Backwards!
            dp[s] += dp[s - num]

    return dp[target]
```

### 13.3 3. Unbounded Knapsack - Minimum Items

```python
def min_coins(coins: List[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for coin in coins:
        for a in range(coin, amount + 1):  # Forwards!
            dp[a] = min(dp[a], dp[a - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1
```

### 13.4 4. Unbounded Knapsack - Count Combinations

```python
def count_combinations(coins: List[int], amount: int) -> int:
    dp = [0] * (amount + 1)
    dp[0] = 1

    for coin in coins:  # Coins outer for combinations
        for a in range(coin, amount + 1):  # Forwards!
            dp[a] += dp[a - coin]

    return dp[amount]
```

### 13.5 5. Target Sum Transformation

```python
def target_sum_ways(nums: List[int], target: int) -> int:
    total = sum(nums)

    # Transform: P - N = target, P + N = total → P = (target + total) / 2
    if (total + target) % 2 != 0 or total + target < 0:
        return 0

    subset_target = (total + target) // 2
    return count_subsets(nums, subset_target)  # Use 0/1 count template
```

### 13.6 6. Generic 2D Knapsack (When 1D Won't Work)

```python
def knapsack_2d(items: List[Tuple[int, int]], capacity: int) -> int:
    """
    items: list of (weight, value)
    Returns: maximum value achievable within capacity
    """
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        weight, value = items[i - 1]
        for c in range(capacity + 1):
            dp[i][c] = dp[i-1][c]  # Skip item
            if c >= weight:
                dp[i][c] = max(dp[i][c], dp[i-1][c - weight] + value)  # Take item

    return dp[n][capacity]
```

### 13.7 Variable Naming Convention

| Variable | Purpose | Example |
|----------|---------|---------|
| `dp[s]` / `dp[a]` | DP array for sum/amount | `dp[target]` |
| `target` / `amount` | Goal value | `target = total // 2` |
| `num` / `coin` / `item` | Current item being processed | `for num in nums:` |
| `s` / `a` / `c` | Loop variable for sum/amount/capacity | `for s in range(target, ...)` |



---



*Document generated for NeetCode Practice Framework — API Kernel: dp_knapsack_subset*
