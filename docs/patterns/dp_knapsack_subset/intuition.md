# DP Knapsack / Subset: Pattern Intuition Guide

> *"The knapsack question is simple: take it or leave it. The art is in how you remember what you've already considered."*

---

## The Situation That Calls for Knapsack DP

Imagine you're a burglar with a backpack of limited capacity. You see valuable items of different weights. For each item, you ask: **"Should I take this or leave it?"**

This is the essence of Knapsack/Subset DP: making binary decisions (take/skip) across a collection of items to optimize some goal.

---

## The Two Fundamental Variants

### 0/1 Knapsack (Each Item Once)

**Mental Model**: Shopping with a gift card. Each store item can only be bought once.

```
Items:      [Apple, Banana, Cherry]
Weights:    [2, 3, 5]
Values:     [3, 4, 5]
Capacity:   5

For each item: Take it (use capacity) or skip it?
```

**Key Constraint**: Once you take an item, it's gone from consideration.

### Unbounded Knapsack (Items Reusable)

**Mental Model**: Buying at a vending machine. Each button dispenses unlimited copies.

```
Coins:      [1, 2, 5]
Target:     11

For each coin: Use it (as many times as needed) or move to next?
```

**Key Constraint**: You can use the same item multiple times.

---

## The Critical Iteration Direction

This is the most important concept to internalize:

### 0/1: Iterate Backwards

```python
for num in nums:
    for s in range(target, num - 1, -1):  # Backwards!
        dp[s] = dp[s] or dp[s - num]
```

**Why?** Each number should contribute at most once per iteration.

If you go forward, `dp[s - num]` might already include `num` from this iteration, causing double-counting.

### Unbounded: Iterate Forward

```python
for coin in coins:
    for a in range(coin, amount + 1):  # Forward!
        dp[a] = min(dp[a], dp[a - coin] + 1)
```

**Why?** You *want* to reuse the current coin.

If you go backward, `dp[a - coin]` hasn't been updated yet, missing the reuse opportunity.

---

## The Three Goals

Knapsack problems ask three types of questions:

### 1. Can You Reach? (Boolean)
> *"Can the array be partitioned into two equal subsets?"*

```python
dp[s] = dp[s] or dp[s - num]  # True if either way works
```

### 2. How Many Ways? (Count)
> *"How many different ways to make the amount?"*

```python
dp[s] += dp[s - num]  # Add up all the ways
```

### 3. What's the Minimum/Maximum? (Optimize)
> *"What's the minimum number of coins?"*

```python
dp[s] = min(dp[s], dp[s - num] + 1)  # Pick the better option
```

---

## Pattern Recognition Signals

### Signal: "Partition" or "Divide into two groups"
> *"Can you split the array into two subsets with equal sum?"*

**Action**: Target = total_sum / 2, use 0/1 boolean.

### Signal: "Number of ways with +/-"
> *"Assign + or - to each number to reach target"*

**Action**: Transform to subset sum: P = (total + target) / 2.

### Signal: "Minimum coins" or "Fewest items"
> *"Fewest coins to make the amount"*

**Action**: Unbounded knapsack with min().

### Signal: "Count combinations" (not permutations)
> *"Number of ways using items, order doesn't matter"*

**Action**: Items outer loop, amount inner loop.

---

## The Transformation Trick

Some problems don't look like knapsack but can be transformed:

### Target Sum Transformation

**Problem**: Assign +/- to reach target.
**Insight**: Let P = numbers with +, N = numbers with -.
- P - N = target
- P + N = total

Solving: **P = (target + total) / 2**

Now it's: "Count subsets summing to P" — a standard 0/1 knapsack!

### Partition Transformation

**Problem**: Can array be split into two equal halves?
**Insight**: Each half must sum to total/2.

Now it's: "Can we select items summing to total/2?" — 0/1 knapsack!

---

## When to Use DP vs Backtracking

| Question | Answer |
|----------|--------|
| Need the count/min/max? | Use DP |
| Need to list all combinations? | Use Backtracking |
| Target fits in memory as array index? | DP is feasible |
| Same subproblems reached many ways? | DP benefits from memoization |

**Rule of Thumb**: If the answer is a number (count, min, max), use DP. If you need to output the actual selections, use backtracking.

---

## Common Pitfalls

### Pitfall 1: Wrong Iteration Direction

```python
# WRONG for 0/1 (double-counts items)
for num in nums:
    for s in range(num, target + 1):  # Forward - BAD!
        dp[s] = dp[s] or dp[s - num]

# RIGHT for 0/1
for num in nums:
    for s in range(target, num - 1, -1):  # Backward - GOOD!
        dp[s] = dp[s] or dp[s - num]
```

### Pitfall 2: Combinations vs Permutations

```python
# Combinations (order doesn't matter): coins outer
for coin in coins:
    for a in range(coin, amount + 1):
        dp[a] += dp[a - coin]

# Permutations (order matters): amount outer
for a in range(1, amount + 1):
    for coin in coins:
        if coin <= a:
            dp[a] += dp[a - coin]
```

### Pitfall 3: Forgetting Edge Cases

- Total sum is odd → can't partition evenly
- (target + total) is odd → no valid +/- assignment
- Target is negative → transform might not work

---

## Practice Progression

Master Knapsack/Subset DP through this sequence:

1. **LC 416** (Partition Equal Subset Sum) — Basic 0/1 boolean
2. **LC 494** (Target Sum) — 0/1 count with transformation
3. **LC 322** (Coin Change) — Unbounded minimize
4. **LC 518** (Coin Change 2) — Unbounded count combinations

---

## The Unifying Principle

Knapsack/Subset DP is about **making binary decisions across items while tracking capacity/sum**.

The key insight: **the number of ways to reach sum S with items 1..i only depends on how many ways to reach sums S and S-item[i] with items 1..i-1.**

This recursive structure allows us to build solutions bottom-up, one item at a time.

*"Take or skip. That's the only question. The answer builds from the answers to smaller questions."*
