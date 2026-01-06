## Base Template: Jump Game (LeetCode 55)

> **Problem**: Determine if you can reach the last index, starting from index 0.
> **Invariant**: `farthest_reachable` = maximum index we can reach at each step.
> **Role**: BASE TEMPLATE for `GreedyReachability` kernel.

### Implementation

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

### Why Greedy Works

The greedy choice: always extend `farthest_reachable` as far as possible.

**Greedy Choice Property**: If we can reach position `i`, and from `i` we can reach `j`, then we can reach `j`. We don't need to track *how* we got to `i`.

**Optimal Substructure**: Reachability is transitive. If A → B and B → C, then A → C.

### Trace Example

```
nums:      [2, 3, 1, 1, 4]
index:      0  1  2  3  4
farthest:   0  2  4  4  4

i=0: farthest = max(0, 0+2) = 2
i=1: farthest = max(2, 1+3) = 4 >= 4 ✓ (early exit)

Result: True
```

### Edge Cases

| Case | Input | Output | Handling |
|------|-------|--------|----------|
| Single element | `[0]` | `True` | Already at end |
| Stuck at start | `[0, 1]` | `False` | `farthest=0`, can't reach i=1 |
| Zero in middle | `[2, 0, 0]` | `True` | Jump over zeros from i=0 |


