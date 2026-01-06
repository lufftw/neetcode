# DP 1D Linear: Pattern Intuition Guide

> *"Dynamic programming is just careful brute force — you solve every subproblem, but you remember what you've already solved."*

---

## The Situation That Calls for 1D DP

Imagine you're climbing a staircase and want to count how many ways you can reach the top. At each step, you can take 1 or 2 stairs. How do you think about this?

The brute force approach: try every possible combination. But this explodes exponentially.

The DP insight: **The number of ways to reach step 5 depends only on how many ways you can reach steps 3 and 4.** If you know those, you just add them up.

This is the essence of 1D Linear DP: **build solutions from smaller subproblems along a single dimension.**

---

## The 1D DP Backbone

Every 1D DP problem follows the same skeleton:

```
1. DEFINE STATE: What does dp[i] represent?
2. WRITE TRANSITION: How does dp[i] relate to previous values?
3. SET BASE CASES: What are the starting values?
4. FIND ANSWER: Where is the final result?
5. OPTIMIZE SPACE: Can we reduce memory?
```

**Mental Model**: Think of `dp[i]` as "the answer to the problem if the input only went up to index i."

---

## Two Fundamental Patterns

### Pattern 1: Additive (Count Ways)

**Mental Model**: A branching path where you sum all possible routes.

```
          Step 5
         /      \
      Step 4   Step 3
       /  \     /  \
    ...   ...  ...  ...
```

To reach step 5, you add:
- Ways to reach step 4 (then take 1 step)
- Ways to reach step 3 (then take 2 steps)

**Formula**: `dp[i] = dp[i-1] + dp[i-2]`

**Problems**: LC 70 (Climbing Stairs), LC 746 (Min Cost Climbing)

### Pattern 2: Selective (Max/Min)

**Mental Model**: At each point, you make an optimal choice.

```
House:  [2, 7, 9, 3, 1]
         ↓
        Rob or skip?
```

At each house, you choose:
- **Skip**: Keep the best you had before → `dp[i-1]`
- **Rob**: Take this house + best from non-adjacent → `dp[i-2] + nums[i]`

**Formula**: `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`

**Problems**: LC 198 (House Robber), LC 121 (Best Time Buy/Sell Stock)

---

## The "Include or Exclude" Framework

Many DP problems reduce to one question at each step:

> *"Should I include the current element or exclude it?"*

| Decision | Effect | When to Choose |
|----------|--------|----------------|
| **Include** | Add value, skip some previous | Current element is valuable |
| **Exclude** | Keep previous best, skip current | Previous result is better |

The transition becomes: `dp[i] = best(include_option, exclude_option)`

---

## Space Optimization: The Two-Variable Trick

Most 1D DP only needs the last 1-2 values. Why store an entire array?

**Before (O(n) space)**:
```python
dp = [0] * (n + 1)
dp[0], dp[1] = 1, 1
for i in range(2, n + 1):
    dp[i] = dp[i-1] + dp[i-2]
return dp[n]
```

**After (O(1) space)**:
```python
prev2, prev1 = 1, 1
for i in range(2, n + 1):
    prev2, prev1 = prev1, prev2 + prev1
return prev1
```

**When to optimize**:
- Transition only uses last k values → O(k) space
- Don't need to reconstruct the path → safe to optimize
- Not doing multiple queries → no need to keep full array

---

## Pattern Recognition Signals

### Signal: "Number of ways to..."
> *"How many distinct ways to climb n stairs?"*
> *"Count paths from start to end"*

**Action**: Additive DP, sum transitions.

### Signal: "Maximize profit without taking adjacent"
> *"Rob houses but can't rob neighbors"*
> *"Maximum sum of non-consecutive elements"*

**Action**: Include/exclude DP.

### Signal: "Track best so far"
> *"Best time to buy and sell"*
> *"Maximum subarray sum"*

**Action**: Running min/max (implicit DP).

### Signal: "Circular array"
> *"First and last elements are adjacent"*

**Action**: Split into two linear subproblems.

---

## Common Pitfalls

### Pitfall 1: Wrong Base Cases
**Problem**: Off-by-one errors in initialization.

```python
# Wrong: dp[1] should be 1, not 2 for climbing stairs
dp[0], dp[1] = 1, 2  # ERROR

# Right: One way to reach step 0 (stay), one way to reach step 1
dp[0], dp[1] = 1, 1
```

**Solution**: Trace through small examples manually.

### Pitfall 2: Confusing "Up To" vs "At"

Two different state definitions:
- `dp[i]` = best solution **using elements 0..i** (can include i)
- `dp[i]` = best solution **ending at i** (must include i)

These require different transitions!

### Pitfall 3: Forgetting Edge Cases

```python
# Always handle small inputs before the loop
if n <= 2:
    return n  # Or appropriate base case
```

### Pitfall 4: Wrong Final Answer Location

| Problem | Answer Location |
|---------|-----------------|
| Reach step n | `dp[n]` |
| Best among all | `max(dp)` or `dp[n-1]` |
| Min cost to go beyond | `min(dp[n-1], dp[n-2])` |

---

## The Circular Array Trick

When first and last elements conflict (can't both be selected):

**Solution**: Solve two separate linear problems:
1. Exclude the last element: solve for `arr[0:n-1]`
2. Exclude the first element: solve for `arr[1:n]`

Take the better of the two results.

**Why it works**: By excluding one endpoint, you break the circle into a line.

---

## Practice Progression

Master 1D Linear DP through this sequence:

1. **LC 70** (Climbing Stairs) — Pure Fibonacci, additive DP
2. **LC 746** (Min Cost Climbing) — Add cost, switch to min
3. **LC 198** (House Robber) — Include/exclude framework
4. **LC 213** (House Robber II) — Circular decomposition
5. **LC 121** (Best Time Buy/Sell) — Implicit DP with running min

---

## The Unifying Principle

1D Linear DP is about **building optimal solutions from optimal sub-solutions**.

The key insight: **if you know the best answer for smaller problems, you can combine them to get the best answer for the current problem.**

This works because of two properties:
1. **Optimal Substructure**: Optimal solution contains optimal solutions to subproblems
2. **Overlapping Subproblems**: Same subproblems are solved multiple times

DP avoids redundant computation by remembering what you've already solved.

*"Don't recalculate. Remember."*
