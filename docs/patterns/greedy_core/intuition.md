# Greedy Core: Pattern Intuition Guide

> *"Greedy is not about being short-sighted — it's about having the confidence that local wisdom leads to global success."*

---

## The Situation That Calls for Greedy Core

Imagine you're hiking across stepping stones to cross a river. At each stone, you can see how far you can jump. You don't need to plan the entire route — you just need to know: **"Can I reach a stone that gets me closer to the goal?"**

This is the essence of **Greedy Core**: make the locally best choice, and trust that it leads to the globally best outcome.

---

## Three Mental Models

Greedy Core problems fall into three distinct patterns, each with its own mental model:

### 1. The Farthest Reach (Reachability)

**Mental Model**: You're a frog on lily pads. At each pad, you can see the farthest pad you could possibly reach. You don't need to plan each hop — you just need to track the farthest possible destination.

**Key Insight**: If you can reach position X, and from X you can reach Y, then you can reach Y. The exact path doesn't matter for reachability questions.

**When to Use**: Problems asking "can you reach the end?" or "what's the minimum number of steps?"

**Visual**:
```
Positions:  0   1   2   3   4   5
Jumps:     [2,  3,  1,  1,  4]
Reach:      ────►──────►────────►
            From 0, can reach 2
                From 1, can reach 4
                    From anywhere ≤4, can reach 5 ✓
```

### 2. The Balance Sheet (Prefix Min/Reset)

**Mental Model**: You're driving around a circular track with gas stations. You start with an empty tank. At each station, you gain some gas but spend some to reach the next station.

If your tank ever goes negative, you know: **"I can't have started from any station I've passed so far."** Reset and try the next station as your new candidate.

**Key Insight**: If you fail at station J starting from station I, you'll also fail starting from any station between I and J (they have even less accumulated gas).

**When to Use**: Circular route problems, resource tracking with feasibility checks.

**Visual**:
```
Stations:  0    1    2    3    4
Net gain:  -2   -2   -2   +3   +3
Running:   -2 → fail! reset to 1
           -2 → fail! reset to 2
           -2 → fail! reset to 3
           +3 → +6 (cumulative success)

Total = 0 ≥ 0, so starting at 3 works.
```

### 3. The Matchmaker (Sort + Match)

**Mental Model**: You're a matchmaker pairing children with cookies. Greedy children need bigger cookies. How do you maximize happiness?

Sort both lists. Match the least greedy child with the smallest sufficient cookie. Never waste a big cookie on an undemanding child.

**Key Insight**: Sorting transforms a complex assignment problem into a simple left-to-right scan.

**When to Use**: Problems with two sequences to match/assign, optimization of pairings.

**Visual**:
```
Children (greed): [1, 2, 3]  → sorted
Cookies (size):   [1, 2, 1]  → [1, 1, 2] sorted

Match: greed=1 ← cookie=1 ✓
       greed=2 ← cookie=2 ✓ (skip cookie=1, too small)
       greed=3 ← no cookie big enough

Result: 2 children satisfied
```

---

## Pattern Recognition Signals

When you see these phrases, think **Greedy Core**:

### Signal: "Can you reach..." or "Minimum jumps to..."
> *"Determine if you can reach the last index"*
> *"Find the minimum number of jumps"*

**Action**: Track farthest reachable position.

### Signal: "Complete a circuit" or "Circular route"
> *"Find starting point to complete the loop"*
> *"Track resource balance around a cycle"*

**Action**: Use prefix sum with reset; check total feasibility.

### Signal: "Distribute" or "Assign" or "Match"
> *"Assign cookies to maximize satisfaction"*
> *"Distribute people to minimize cost"*

**Action**: Sort by the key metric, then greedily match.

### Signal: "Neighbors must satisfy..." (bidirectional)
> *"Higher-rated neighbors must have more"*
> *"Constraints from both left and right"*

**Action**: Two-pass greedy (forward + backward).

---

## The Two-Pass Pattern

Some problems have constraints from **both directions**. A single pass can't see the future. The solution: **two passes**.

**Example**: Candy distribution (LC 135)
- Forward pass: "If I'm better than my left neighbor, I need more candy than them."
- Backward pass: "If I'm better than my right neighbor, I need more candy than them."
- Final answer: Take the **max** at each position.

**Mental Model**: Two waves of information sweeping through the array, meeting in the middle with complete knowledge.

---

## When Greedy Fails

Greedy Core does **NOT** work when:

1. **The future affects the present**
   - Knapsack: Taking a small item now might block a better combination later
   - Solution: Dynamic Programming

2. **Multiple interacting constraints**
   - Job scheduling with deadlines AND profits AND durations
   - Solution: Often DP or heap-based greedy

3. **Non-monotonic properties**
   - Choices that seem good now become bad later
   - Solution: Search (backtracking, BFS) or DP

### The Greedy Validity Test

Before using greedy, ask:
1. **Greedy Choice Property**: Does the locally optimal choice lead to a globally optimal solution?
2. **Optimal Substructure**: Does the optimal solution contain optimal solutions to subproblems?
3. **No Regret**: Once a choice is made, will we never need to undo it?

If all three are "yes," greedy works.

---

## Common Pitfalls

### Pitfall 1: Forgetting Early Exit
**Problem**: Continuing to iterate when the answer is already determined.
```python
# Bad: Always scans entire array
for i in range(len(nums)):
    farthest = max(farthest, i + nums[i])
return farthest >= len(nums) - 1

# Good: Exit early when goal is reached
for i in range(len(nums)):
    if i > farthest:
        return False
    farthest = max(farthest, i + nums[i])
    if farthest >= len(nums) - 1:
        return True  # Early exit!
```

### Pitfall 2: Off-by-One in Jump Counting
**Problem**: Counting a jump at the wrong position.
```python
# The boundary check happens AFTER processing the position
for i in range(len(nums) - 1):  # Stop before last
    farthest = max(farthest, i + nums[i])
    if i == current_end:  # At boundary, must jump
        jumps += 1
        current_end = farthest
```

### Pitfall 3: Forgetting Total Feasibility Check
**Problem**: Returning a candidate start without verifying total balance.
```python
# Wrong: Just return candidate
return candidate_start

# Right: Check if total is non-negative
return candidate_start if total_surplus >= 0 else -1
```

---

## Practice Progression

Master Greedy Core through this sequence:

1. **LC 55** (Jump Game) — Pure reachability tracking
2. **LC 45** (Jump Game II) — Add level counting
3. **LC 455** (Assign Cookies) — Simple sort + match
4. **LC 1029** (Two City Scheduling) — Sort by derived metric
5. **LC 134** (Gas Station) — Reset logic with feasibility
6. **LC 135** (Candy) — Two-pass bidirectional constraints

---

## The Unifying Principle

Greedy Core is about **confidence in local decisions**.

Unlike DP, which hedges by considering all possibilities, greedy commits fully to the current best choice. This works when the problem has structure that guarantees local optimality implies global optimality.

The three kernels — reachability, reset, and sort+match — are different manifestations of this principle:
- **Reachability**: "Extend as far as possible; the path will work itself out."
- **Reset**: "If this start fails, everything before it fails too; try fresh."
- **Sort+Match**: "Handle the easiest cases first; they won't interfere with harder ones."

*"Trust the greedy choice. If it's the right pattern, it won't let you down."*
