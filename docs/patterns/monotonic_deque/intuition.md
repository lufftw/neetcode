# Monotonic Deque - Intuition Guide

## The Mental Model: The VIP Queue

Imagine a VIP queue where only the "best" candidates stay:
- New candidates join from the back
- When someone better arrives, weaker candidates leave
- The front always shows the current best
- Old candidates eventually time out and leave

This is exactly how a monotonic deque works for sliding window problems.

## Why Monotonic Deque?

A heap gives O(log k) per operation. But with a deque, we achieve O(1) amortized:
- Each element enters once, exits once
- The front is always the answer
- No need to search through the structure

## Core Insight

When looking for the **maximum** in a window:
- If element `B` comes after `A` and `B >= A`, then `A` will never be the maximum for any future window
- `A` is "dominated" by `B` and can be removed

```
Window: [3, 1, 4, 2]
              ^
              4 dominates 1 and 3

Deque: [4, 2] - only potential maximums kept
```

## Pattern 1: Fixed Window Maximum (LC 239)

**The insight**: Maintain a decreasing deque. Front = current window max.

```
nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3

Step 1: [1]       dq=[0]         window incomplete
Step 2: [1,3]     dq=[1]         3 dominates 1, pop it
Step 3: [1,3,-1]  dq=[1,2]       window complete, max=3
Step 4: [3,-1,-3] dq=[1,2,3]     max=3 (index 1 still valid)
Step 5: [-1,-3,5] dq=[4]         5 dominates all, max=5
...
```

The code:
```python
# Remove dominated elements from back
while dq and nums[dq[-1]] < num:
    dq.pop()
```

## Pattern 2: Two Deques (LC 1438)

**The insight**: For max-min constraint, maintain both max and min deques.

```
nums = [8, 2, 4, 7], limit = 4

                max_dq    min_dq    max-min  valid?
i=0: [8]        [0]       [0]       0        ✓
i=1: [8,2]      [0,1]     [1,0]     6        ✗ shrink!
     [2]        [1]       [1]       0        ✓
i=2: [2,4]      [1,2]     [1,2]     2        ✓
i=3: [2,4,7]    [3,2]     [1,2,3]   5        ✗ shrink!
     [4,7]      [3,2]     [2,3]     3        ✓

Longest: 2
```

## Pattern 3: Prefix Sum + Deque (LC 862)

**The insight**: With negative numbers, use prefix sums and find minimum prefix.

```
nums = [2, -1, 2], k = 3
prefix = [0, 2, 1, 3]

For j=3 (prefix=3):
  Find smallest i where prefix[3] - prefix[i] >= 3
  prefix[3] - prefix[2] = 3 - 1 = 2 < 3
  prefix[3] - prefix[0] = 3 - 0 = 3 >= 3 ✓
  Length = 3 - 0 = 3
```

Why increasing deque?
```
If prefix[i1] >= prefix[i2] where i1 < i2:
  - i2 gives larger difference (prefix[j] - prefix[i2] >= prefix[j] - prefix[i1])
  - i2 gives shorter length (j - i2 < j - i1)
  - i1 is dominated, remove it
```

## Pattern 4: Algebraic Transformation (LC 1499)

**The insight**: Rewrite the equation to separate the indices.

```
Maximize: yi + yj + |xi - xj|

Since sorted and i < j:
  = yi + yj + (xj - xi)
  = (yj + xj) + (yi - xi)
      ^^^^^^^^   ^^^^^^^^^
      current j  maximize for i in window
```

Now it's a standard sliding window maximum on `yi - xi`!

## Common Mistakes

### Mistake 1: Wrong comparison operator

```python
# ❌ Wrong for max deque: using <=
while dq and nums[dq[-1]] <= num:  # Removes equal elements

# ✅ Right: use < for max (keep equal elements)
while dq and nums[dq[-1]] < num:
```

### Mistake 2: Not removing stale elements

```python
# ❌ Wrong: forgetting to remove out-of-window elements
dq.append(i)
result.append(nums[dq[0]])

# ✅ Right: remove stale elements first
while dq and dq[0] < i - k + 1:
    dq.popleft()
dq.append(i)
```

### Mistake 3: Wrong window condition

```python
# ❌ Wrong: off-by-one in window check
if i >= k:

# ✅ Right: window complete when i >= k-1
if i >= k - 1:
```

## Quick Pattern Recognition

| Clue | Pattern |
|------|---------|
| "maximum/minimum in sliding window" | Single deque |
| "longest subarray with max-min <= limit" | Two deques |
| "shortest subarray with sum >= k" (negatives) | Prefix + deque |
| "maximize yi + yj + distance" | Transform + deque |

## Monotonic Deque vs Monotonic Stack

| Structure | Use Case | Direction |
|-----------|----------|-----------|
| **Stack** | Next greater/smaller element | Push/pop from one end |
| **Deque** | Window maximum/minimum | Push one end, pop both ends |

## Visual Summary

```
Monotonic Deque (Decreasing for Max):

New element arrives:
                    ┌─────────────────────────────┐
    Remove stale    │  Remove dominated elements  │  Add new
    from front      │  from back                  │  to back
         ↓          │           ↓                 │     ↓
    ┌───────────────┴───────────────────────────────────┐
    │  MAX  │  ...  │  ...  │  dominated  │  NEW      │
    └───────────────────────────────────────────────────┘
       ↑                          ↑
    Answer is                   These get
    always here                 removed
```
