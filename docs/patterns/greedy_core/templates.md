# Greedy Core Pattern

## Table of Contents

1. [API Kernel: `GreedyCore`](#1-api-kernel-greedycore)
2. [Three Core Kernels](#2-three-core-kernels)
3. [Why NOT Interval / Heap Greedy?](#3-why-not-interval--heap-greedy)
4. [Core Principle: Greedy Choice Property](#4-core-principle-greedy-choice-property)
5. [Base Template: Jump Game (LeetCode 55)](#5-base-template-jump-game-leetcode-55)
6. [Variant: Jump Game II (LeetCode 45)](#6-variant-jump-game-ii-leetcode-45)
7. [Variant: Gas Station (LeetCode 134)](#7-variant-gas-station-leetcode-134)
8. [Variant: Candy (LeetCode 135)](#8-variant-candy-leetcode-135)
9. [Variant: Assign Cookies (LeetCode 455)](#9-variant-assign-cookies-leetcode-455)
10. [Variant: Two City Scheduling (LeetCode 1029)](#10-variant-two-city-scheduling-leetcode-1029)
11. [Pattern Comparison](#11-pattern-comparison)
12. [Decision Flowchart](#12-decision-flowchart)
13. [Problem Mapping](#13-problem-mapping)
14. [Template Quick Reference](#14-template-quick-reference)

---

## 1. API Kernel: `GreedyCore`

> **Core Mechanism**: Make locally optimal choices that lead to a globally optimal solution through invariant preservation.

**Greedy Core** encompasses non-interval, non-heap greedy algorithms that maintain a simple invariant during a single pass. Unlike interval scheduling (which requires sorting by end times) or heap-based greedy (which requires priority queue), these problems rely on direct state tracking and local decision-making.

---

## 2. Three Core Kernels

| Kernel | Key Invariant | Representative Problems |
|--------|---------------|------------------------|
| **Reachability** | Track farthest reachable position | Jump Game, Jump Game II |
| **Prefix Min/Reset** | Track running minimum with conditional reset | Gas Station |
| **Sort + Match** | Sort by one dimension, greedily match | Candy, Assign Cookies, Two City Scheduling |

---

## 3. Why NOT Interval / Heap Greedy?

| Category | Characteristics | Examples |
|----------|-----------------|----------|
| **Greedy Core** (this pattern) | Single-pass, state tracking, no complex data structures | LC 55, 45, 134, 135, 455, 1029 |
| **Interval Greedy** | Sort by interval endpoints, conflict resolution | LC 56, 435, 452 |
| **Heap Greedy** | Priority queue for dynamic selection | LC 253, 621, 1046 |

---

## 4. Core Principle: Greedy Choice Property

A greedy algorithm works when:
1. **Greedy Choice Property**: A locally optimal choice leads to a globally optimal solution
2. **Optimal Substructure**: The optimal solution contains optimal solutions to subproblems

For Greedy Core problems, the choice is typically:
- "Extend as far as possible" (reachability)
- "Reset when deficit" (prefix minimum)
- "Match smallest available" (sorting)

---

## 5. Base Template: Jump Game (LeetCode 55)

> **Problem**: Determine if you can reach the last index, starting from index 0.
> **Invariant**: `farthest_reachable` = maximum index we can reach at each step.
> **Role**: BASE TEMPLATE for `GreedyReachability` kernel.

### 5.1 Implementation

```python
class Solution:
    """
    Greedy Reachability: Track farthest reachable position.

    Key Insight:
    - At each position i, we can jump anywhere in [i+1, i+nums[i]]
    - If i > farthest_reachable, position i is unreachable, so we fail
    - If farthest_reachable >= last_index at any point, we succeed

    Invariant: farthest_reachable always holds the maximum index
    reachable from any position we've seen so far.

    Time: O(n) | Space: O(1)
    """
    def canJump(self, nums: List[int]) -> bool:
        farthest_reachable = 0
        last_index = len(nums) - 1

        for current_index in range(len(nums)):
            # If current position is unreachable, fail
            if current_index > farthest_reachable:
                return False

            # Update farthest reachable from this position
            farthest_reachable = max(
                farthest_reachable,
                current_index + nums[current_index]
            )

            # Early exit: can already reach the end
            if farthest_reachable >= last_index:
                return True

        return True
```

### 5.2 Why Greedy Works

The greedy choice: always extend `farthest_reachable` as far as possible.

**Greedy Choice Property**: If we can reach position `i`, and from `i` we can reach `j`, then we can reach `j`. We don't need to track *how* we got to `i`.

**Optimal Substructure**: Reachability is transitive. If A → B and B → C, then A → C.

### 5.3 Trace Example

```
nums:      [2, 3, 1, 1, 4]
index:      0  1  2  3  4
farthest:   0  2  4  4  4

i=0: farthest = max(0, 0+2) = 2
i=1: farthest = max(2, 1+3) = 4 >= 4 ✓ (early exit)

Result: True
```

### 5.4 Edge Cases

| Case | Input | Output | Handling |
|------|-------|--------|----------|
| Single element | `[0]` | `True` | Already at end |
| Stuck at start | `[0, 1]` | `False` | `farthest=0`, can't reach i=1 |
| Zero in middle | `[2, 0, 0]` | `True` | Jump over zeros from i=0 |

---

## 6. Variant: Jump Game II (LeetCode 45)

> **Problem**: Find the minimum number of jumps to reach the last index.
> **Invariant**: Track current jump's boundary and next jump's farthest reach.
> **Delta from Base**: Count jumps using "level boundaries" (BFS-like greedy).

### 6.1 Implementation

```python
class Solution:
    """
    Greedy Jump Counting: Implicit BFS with level boundaries.

    Key Insight:
    - Each "jump" explores all positions reachable from current level
    - current_end marks the boundary of current jump's reach
    - next_farthest tracks the farthest we can reach in next jump
    - When we hit current_end, we must make a jump to continue

    This is BFS without a queue: levels are defined by jump boundaries.

    Time: O(n) | Space: O(1)
    """
    def jump(self, nums: List[int]) -> int:
        if len(nums) <= 1:
            return 0

        jump_count = 0
        current_end = 0      # Boundary of current jump's reach
        next_farthest = 0    # Farthest position reachable in next jump

        for current_index in range(len(nums) - 1):  # Don't need to jump from last
            # Extend next jump's reach
            next_farthest = max(
                next_farthest,
                current_index + nums[current_index]
            )

            # Reached current jump's boundary - must make a jump
            if current_index == current_end:
                jump_count += 1
                current_end = next_farthest

                # Early exit: can reach the end
                if current_end >= len(nums) - 1:
                    break

        return jump_count
```

### 6.2 Why BFS-Like Greedy Works

Each jump defines a "level" in implicit BFS:
- Level 0: positions reachable with 0 jumps (just index 0)
- Level 1: positions reachable with 1 jump
- Level k: positions reachable with k jumps

We don't need a queue because:
1. Positions are visited in order (index 0, 1, 2, ...)
2. `current_end` marks where current level ends
3. `next_farthest` finds where next level ends

### 6.3 Trace Example

```
nums:        [2, 3, 1, 1, 4]
index:        0  1  2  3  4

i=0: next_farthest = max(0, 0+2) = 2
     i == current_end(0) → jump_count=1, current_end=2

i=1: next_farthest = max(2, 1+3) = 4 >= last_index

i=2: i == current_end(2) → jump_count=2, current_end=4
     current_end >= last_index → break

Result: 2 jumps
```

### 6.4 Difference from Base Template

| Aspect | Jump Game (LC 55) | Jump Game II (LC 45) |
|--------|-------------------|----------------------|
| Goal | Reachability (yes/no) | Minimum jumps (count) |
| State | Single variable: `farthest` | Two variables: `current_end`, `next_farthest` |
| Logic | Check if `i > farthest` | Increment count at level boundary |
| Output | Boolean | Integer |

---

## 7. Variant: Gas Station (LeetCode 134)

> **Problem**: Find the starting gas station index to complete a circular route, or -1 if impossible.
> **Invariant**: Track running surplus; reset start when deficit occurs.
> **Delta from Base**: Prefix sum with reset + total feasibility check.

### 7.1 Implementation

```python
class Solution:
    """
    Greedy Reset: Track local surplus, reset start on deficit.

    Key Insights:
    1. If total_gas >= total_cost, a valid start exists (pigeonhole principle)
    2. If we can't reach station j from station i, we also can't reach j
       from any station between i and j (they have less accumulated gas)
    3. When surplus goes negative, the next station is a candidate start

    Invariant: current_surplus tracks gas balance since last reset point.

    Time: O(n) | Space: O(1)
    """
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        total_surplus = 0      # Total gas - total cost (feasibility check)
        current_surplus = 0    # Surplus since candidate start
        candidate_start = 0    # Current best starting station

        for station in range(len(gas)):
            net_gain = gas[station] - cost[station]
            total_surplus += net_gain
            current_surplus += net_gain

            # Can't reach next station from candidate_start
            # Reset: next station becomes new candidate
            if current_surplus < 0:
                candidate_start = station + 1
                current_surplus = 0

        # If total is non-negative, candidate_start is valid
        return candidate_start if total_surplus >= 0 else -1
```

### 7.2 Why Reset Works

**Key Lemma**: If we can't complete [i, j] (surplus goes negative at j), then no station in [i, j] can be a valid start.

Proof: Any station k in [i, j] would have even less accumulated gas when reaching j, since it misses the non-negative contributions from [i, k-1].

**Greedy Choice**: When we fail, skip all stations in the failing segment and try the next one.

### 7.3 Trace Example

```
gas:  [1, 2, 3, 4, 5]
cost: [3, 4, 5, 1, 2]
net:  [-2,-2,-2, 3, 3]   (gas - cost at each station)

station=0: current=-2 < 0 → reset, candidate=1
station=1: current=-2 < 0 → reset, candidate=2
station=2: current=-2 < 0 → reset, candidate=3
station=3: current=3
station=4: current=6

total_surplus = -2-2-2+3+3 = 0 >= 0
Result: candidate_start = 3
```

### 7.4 Why Total Check is Sufficient

If `total_surplus >= 0`, there must exist a valid start:
- Total gas >= total cost
- The "lowest point" in the prefix sum defines the optimal start
- Starting after the lowest point ensures we never dip below zero

---

## 8. Variant: Candy (LeetCode 135)

> **Problem**: Distribute candies to children in a line so higher-rated children get more than neighbors.
> **Invariant**: Two-pass greedy ensures both left and right neighbor constraints.
> **Delta from Base**: Two-pass scanning (forward + backward).

### 8.1 Implementation

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

### 8.2 Why Two Passes Are Necessary

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

### 8.3 Trace Example

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

### 8.4 Optimization: O(1) Space

Can use slope counting (peaks and valleys) for O(1) space, but the two-pass approach is clearer and sufficient for interviews.

---

## 9. Variant: Assign Cookies (LeetCode 455)

> **Problem**: Maximize children satisfied with cookies. Child i needs greed[i], cookie j has size[j].
> **Invariant**: Sort both arrays; match smallest satisfiable child with smallest sufficient cookie.
> **Delta from Base**: Sorting + two-pointer greedy matching.

### 9.1 Implementation

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

### 9.2 Why Greedy Works

**Greedy Choice Property**: If cookie `c` can satisfy child `g`, and `c` is the smallest such cookie, we should use it.

Proof by exchange: If we use a larger cookie `c'` for child `g`, we might not be able to satisfy a greedier child later who needs `c' > c`.

**Optimal Substructure**: After matching (child, cookie), the remaining problem is identical but smaller.

### 9.3 Trace Example

```
greed:   [1, 2, 3]  (sorted)
cookies: [1, 1]     (sorted)

cookie=1 >= greed=1 → satisfy, child=1, cookie=1, count=1
cookie=1 < greed=2  → skip cookie, cookie=2
No more cookies

Result: 1 child satisfied
```

### 9.4 Pattern: Sort + Match

This is a common greedy pattern:
1. Sort both sequences
2. Use two pointers to match
3. Greedy choice: match smallest that works

Similar problems:
- LC 1029 (Two City Scheduling)
- LC 870 (Advantage Shuffle)
- Meeting room assignments

---

## 10. Variant: Two City Scheduling (LeetCode 1029)

> **Problem**: Send n people to city A and n to city B, minimizing total cost.
> **Invariant**: Sort by cost difference (A cost - B cost); send first half to A.
> **Delta from Base**: Sort by "relative advantage" metric.

### 10.1 Implementation

```python
class Solution:
    """
    Greedy by Cost Difference: Sort by savings from choosing A over B.

    Key Insight:
    - cost[i] = [cost_A, cost_B]
    - diff = cost_A - cost_B measures "how much cheaper A is"
    - Negative diff: A is cheaper, send to A
    - Positive diff: B is cheaper, send to B
    - Sort by diff, send first n (lowest diff) to A, rest to B

    Greedy Choice: Maximize total savings by prioritizing largest
    cost differences.

    Time: O(n log n) | Space: O(1) excluding sort
    """
    def twoCitySchedCost(self, costs: List[List[int]]) -> int:
        # Sort by (cost_A - cost_B)
        # People with most "savings from A" come first
        costs.sort(key=lambda x: x[0] - x[1])

        total_cost = 0
        n = len(costs) // 2

        # First n people go to city A (they benefit most from A)
        for i in range(n):
            total_cost += costs[i][0]

        # Remaining n people go to city B
        for i in range(n, 2 * n):
            total_cost += costs[i][1]

        return total_cost
```

### 10.2 Why Sorting by Difference Works

Consider swapping assignments for two people:
- Person X at A, Person Y at B → cost = X_A + Y_B
- Swap: X at B, Y at A → cost = X_B + Y_A
- Difference: (X_A + Y_B) - (X_B + Y_A) = (X_A - X_B) - (Y_A - Y_B)

If X's diff < Y's diff, keeping X at A is optimal.

### 10.3 Trace Example

```
costs: [[10,20], [30,200], [400,50], [30,20]]

Calculate diffs:
  [10,20]  → diff = -10 (A much cheaper)
  [30,200] → diff = -170 (A much cheaper)
  [400,50] → diff = 350 (B much cheaper)
  [30,20]  → diff = 10 (B slightly cheaper)

Sort by diff: [[30,200], [10,20], [30,20], [400,50]]
              diff: -170,   -10,    10,     350

First n=2 to A: 30 + 10 = 40
Last n=2 to B: 20 + 50 = 70
Total: 110
```

### 10.4 Generalization: Relative Advantage Sorting

This pattern applies when:
1. Each item has multiple options with different costs
2. Must distribute items across options
3. Sort by "relative advantage" of one option over another

The "advantage" metric captures opportunity cost.

---

## 11. Pattern Comparison

### 11.1 Greedy Core vs Interval Greedy

| Aspect | Greedy Core | Interval Greedy |
|--------|-------------|-----------------|
| **Input Structure** | Arrays, sequences | Intervals with start/end |
| **Sorting** | Optional (by value/metric) | Required (by endpoint) |
| **Key Operation** | State tracking, reachability | Conflict detection, selection |
| **Examples** | LC 55, 134, 135 | LC 56, 435, 452 |

### 11.2 Greedy Core vs Heap Greedy

| Aspect | Greedy Core | Heap Greedy |
|--------|-------------|-------------|
| **Data Structure** | Simple variables | Priority queue |
| **Selection** | Direct comparison | Dynamic min/max |
| **Use Case** | Single pass, fixed order | Dynamic selection |
| **Examples** | LC 55, 455, 1029 | LC 253, 621, 1046 |

### 11.3 Greedy Core vs Dynamic Programming

| Aspect | Greedy Core | Dynamic Programming |
|--------|-------------|---------------------|
| **Decision** | Local optimal = Global optimal | Must consider all subproblems |
| **Backtracking** | Never reconsider | May reconsider via memoization |
| **Proof Required** | Greedy choice + optimal substructure | Recurrence relation |
| **Time Complexity** | Usually O(n) or O(n log n) | Often O(n^2) or O(n * state) |

### 11.4 Three Kernels Comparison

| Kernel | Invariant | Key Technique | Problems |
|--------|-----------|---------------|----------|
| **Reachability** | Farthest reachable position | Single scan, max update | LC 55, 45 |
| **Prefix Min/Reset** | Running balance with reset | Deficit triggers reset | LC 134 |
| **Sort + Match** | Sorted order enables optimal | Two pointers / sorting | LC 135, 455, 1029 |

---

## 12. Decision Flowchart

```
Start: "Optimization problem with local choices?"
       │
       ▼
  ┌─────────────────────┐
  │ Can reach / traverse│
  │ positions in array? │───Yes──▶ Reachability Greedy (LC 55, 45)
  └─────────────────────┘
       │ No
       ▼
  ┌─────────────────────┐
  │ Circular route with │
  │ resource tracking?  │───Yes──▶ Prefix Min/Reset Greedy (LC 134)
  └─────────────────────┘
       │ No
       ▼
  ┌─────────────────────┐
  │ Match/assign items  │
  │ from two sequences? │───Yes──▶ Sort + Match Greedy (LC 455, 1029)
  └─────────────────────┘
       │ No
       ▼
  ┌─────────────────────┐
  │ Satisfy constraints │
  │ from both sides?    │───Yes──▶ Two-Pass Greedy (LC 135)
  └─────────────────────┘
       │ No
       ▼
  Consider Interval Greedy / Heap Greedy / DP
```

### 12.1 Kernel Selection Guide

| Problem Signal | Kernel | Example |
|----------------|--------|---------|
| "Can reach", "maximum jump" | Reachability | LC 55, 45 |
| "Complete circuit", "balance tracking" | Prefix Min/Reset | LC 134 |
| "Distribute", "assign", "match" | Sort + Match | LC 455, 1029 |
| "Satisfy neighbors", "bidirectional constraint" | Two-Pass | LC 135 |

### 12.2 When Greedy Fails

Greedy Core does NOT apply when:

1. **Overlapping subproblems**: Same state reached multiple ways
   - Example: Coin change (LC 322) needs DP

2. **Non-local dependencies**: Future choices affect current
   - Example: 0/1 Knapsack needs DP

3. **Multiple constraint dimensions**: Can't sort by single metric
   - Example: Meeting scheduling with rooms needs heap

### 12.3 Proving Greedy Correctness

For Greedy Core problems, verify:

1. **Greedy Choice Property**: Local optimal leads to global optimal
2. **Optimal Substructure**: Solution contains optimal solutions to subproblems
3. **No need to reconsider**: Once a choice is made, it's final

---

## 13. Problem Mapping

### 13.1 By Kernel Type

| Kernel | Problems | Key Technique |
|--------|----------|---------------|
| **Reachability** | LC 55, 45, 1024 | Track farthest reachable, level boundaries |
| **Prefix Min/Reset** | LC 134 | Running balance, reset on deficit |
| **Sort + Match** | LC 455, 1029, 870, 2285 | Sort, two-pointer matching |
| **Two-Pass** | LC 135, 42 (variant) | Forward + backward scan |

### 13.2 By Difficulty Progression

| Level | Problem | Why Here |
|-------|---------|----------|
| **Beginner** | LC 455 (Assign Cookies) | Pure sort + match |
| **Beginner** | LC 55 (Jump Game) | Single invariant tracking |
| **Intermediate** | LC 45 (Jump Game II) | Two variables, level counting |
| **Intermediate** | LC 1029 (Two City) | Sort by derived metric |
| **Intermediate** | LC 134 (Gas Station) | Reset logic, total check |
| **Advanced** | LC 135 (Candy) | Two-pass with max merge |

### 13.3 Related Non-Core Greedy

These problems use greedy but belong to other categories:

| Problem | Category | Why Not Core |
|---------|----------|--------------|
| LC 56 (Merge Intervals) | Interval Greedy | Sort by start, merge logic |
| LC 435 (Non-overlapping Intervals) | Interval Greedy | Sort by end, conflict counting |
| LC 253 (Meeting Rooms II) | Heap Greedy | Dynamic room assignment |
| LC 621 (Task Scheduler) | Heap Greedy | Priority-based selection |

---

## 14. Template Quick Reference

### 14.1 1. Reachability (Can Reach End)

```python
def canReach(nums: List[int]) -> bool:
    farthest = 0
    for i in range(len(nums)):
        if i > farthest:
            return False
        farthest = max(farthest, i + nums[i])
    return True
```

### 14.2 2. Minimum Jumps (BFS-like Level Counting)

```python
def minJumps(nums: List[int]) -> int:
    if len(nums) <= 1:
        return 0

    jumps = 0
    current_end = 0
    next_farthest = 0

    for i in range(len(nums) - 1):
        next_farthest = max(next_farthest, i + nums[i])
        if i == current_end:
            jumps += 1
            current_end = next_farthest
    return jumps
```

### 14.3 3. Circular Route with Reset

```python
def findStart(gain: List[int], cost: List[int]) -> int:
    total = 0
    current = 0
    start = 0

    for i in range(len(gain)):
        net = gain[i] - cost[i]
        total += net
        current += net
        if current < 0:
            start = i + 1
            current = 0

    return start if total >= 0 else -1
```

### 14.4 4. Sort + Two-Pointer Match

```python
def greedyMatch(needs: List[int], supplies: List[int]) -> int:
    needs.sort()
    supplies.sort()

    matched = 0
    supply_idx = 0

    for need in needs:
        while supply_idx < len(supplies) and supplies[supply_idx] < need:
            supply_idx += 1
        if supply_idx < len(supplies):
            matched += 1
            supply_idx += 1

    return matched
```

### 14.5 5. Two-Pass (Bidirectional Constraints)

```python
def twoPassGreedy(values: List[int]) -> List[int]:
    n = len(values)
    result = [1] * n

    # Forward pass: left constraint
    for i in range(1, n):
        if values[i] > values[i - 1]:
            result[i] = result[i - 1] + 1

    # Backward pass: right constraint
    for i in range(n - 2, -1, -1):
        if values[i] > values[i + 1]:
            result[i] = max(result[i], result[i + 1] + 1)

    return result
```

### 14.6 6. Sort by Relative Advantage

```python
def optimalAssignment(costs: List[List[int]]) -> int:
    # costs[i] = [option_A_cost, option_B_cost]
    # Sort by advantage of A over B
    costs.sort(key=lambda x: x[0] - x[1])

    n = len(costs) // 2
    total = 0

    # First half to option A
    for i in range(n):
        total += costs[i][0]

    # Second half to option B
    for i in range(n, 2 * n):
        total += costs[i][1]

    return total
```

### 14.7 Variable Naming Convention

| Variable | Purpose | Example |
|----------|---------|---------|
| `farthest` / `farthest_reachable` | Maximum reachable position | `farthest = max(farthest, i + nums[i])` |
| `current_end` | Boundary of current level/jump | `if i == current_end: jumps += 1` |
| `current_surplus` / `current` | Running balance since reset | `current += gain[i] - cost[i]` |
| `candidate_start` | Reset point candidate | `candidate_start = i + 1` |
| `satisfied_count` / `matched` | Count of successful matches | `matched += 1` |



---



*Document generated for NeetCode Practice Framework — API Kernel: greedy_core*
