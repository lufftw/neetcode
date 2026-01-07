# Interval DP - Intuition Guide

## The Mental Model: Building from Small to Large

Imagine you're solving a puzzle where:
- You have a sequence of elements
- You need to process them optimally
- The order of processing matters
- Once you split/merge at a point, two independent subproblems emerge

**Interval DP thinks backwards**: "What was the LAST operation?"

## Why "Last Operation" Thinking?

Consider bursting balloons: if we think "which balloon to burst FIRST", the problem becomes messy because neighbors change.

Instead: "Which balloon was burst LAST in interval (i, j)?"
- If k was last, we know nums[i] and nums[j] were still there
- The coins from k = nums[i] * nums[k] * nums[j]
- Subproblems (i, k) and (k, j) are independent!

## Core Insight

```
Interval [i, j]: What's the optimal answer?
    └── Try each split point k
        └── Combine: dp[i][k] + dp[k][j] + merge_cost(i, k, j)

Fill order: by interval length (small → large)
```

## Pattern 1: Burst Balloons (LC 312) - "Last to Burst"

**Key insight**: Think about the LAST balloon to burst in each interval.

```
nums = [3, 1, 5, 8]
With boundaries: [1, 3, 1, 5, 8, 1]

For interval (0, 5), if k=2 (value 1) is burst LAST:
  - Left boundary: nums[0] = 1
  - Right boundary: nums[5] = 1
  - Coins from k: 1 * 1 * 1 = 1
  - Plus: dp[0][2] + dp[2][5]
```

Why add boundaries? The virtual 1s at ends make edge cases clean.

## Pattern 2: Polygon Triangulation (LC 1039) - "Choose Third Vertex"

**Key insight**: Triangulation = choosing a third vertex for each edge.

```
Polygon: [1, 2, 3, 4, 5] (vertices in order)

Edge (0, 4): which vertex k forms the triangle?
  - If k=2: triangle (0, 2, 4), cost = v[0] * v[2] * v[4]
  - Plus: dp[0][2] (polygon with edge 0-2)
        + dp[2][4] (polygon with edge 2-4)
```

Same structure as balloons - just different cost interpretation!

## Pattern 3: Cut Stick (LC 1547) - "Last Cut Position"

**Key insight**: Transform cuts into intervals, think about last cut.

```
Stick length = 7, cuts = [1, 3, 4, 5]
Add boundaries: cuts = [0, 1, 3, 4, 5, 7]

To cut segment [0, 7], if we cut at position 3 LAST:
  - Cost = 7 - 0 = 7 (length of stick when we cut)
  - Plus: dp[0][3] + dp[3][7]
```

Preprocessing: Sort cuts and add boundaries.

## Pattern 4: Strange Printer (LC 664) - "Extend First Print"

**Key insight**: Different recurrence - matching characters optimization.

```
String: "aba"

To print s[0:3]:
  - Default: print 'a' first, then handle rest → 1 + dp[1][2]
  - Optimization: s[2] == s[0], so when printing 'a',
    extend to cover position 2 as well!
    → dp[1][1] + dp[2][2] (handle 'b' between them)
```

This is NOT a split-point pattern, but character-matching optimization.

## The Universal Template

```python
# Fill by interval length
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1

        # Try all split points
        for k in range(i + 1, j):
            cost = compute_merge_cost(i, k, j)
            dp[i][j] = optimize(dp[i][j], dp[i][k] + dp[k][j] + cost)
```

## Pattern Recognition Checklist

| Question | If Yes → Interval DP |
|----------|---------------------|
| Process a sequence optimally? | ✓ |
| Order of operations matters? | ✓ |
| Subproblems defined by [i, j]? | ✓ |
| Each operation creates two independent parts? | ✓ |

## Variant Recognition

| Clue | Variant |
|------|---------|
| "burst", "remove", neighbors matter | LC 312 style |
| "triangulate", geometric | LC 1039 style |
| "cut", "split", cost = length | LC 1547 style |
| "print", character matching | LC 664 style |

## Common Pitfalls

1. **Forgetting boundaries**: LC 312 needs [1]+nums+[1], LC 1547 needs [0]+cuts+[n]
2. **Wrong loop bounds**: Interval length starts at 2 (or 3 for polygons)
3. **Inclusive vs exclusive**: Know if dp[i][j] includes endpoints
4. **Not preprocessing**: LC 664 should remove consecutive duplicates

## Complexity

All standard interval DP problems:
- **Time**: O(n³) - three nested loops
- **Space**: O(n²) - the DP table
