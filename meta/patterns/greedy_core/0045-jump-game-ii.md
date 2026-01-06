## Variant: Jump Game II (LeetCode 45)

> **Problem**: Find the minimum number of jumps to reach the last index.
> **Invariant**: Track current jump's boundary and next jump's farthest reach.
> **Delta from Base**: Count jumps using "level boundaries" (BFS-like greedy).

### Implementation

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

### Why BFS-Like Greedy Works

Each jump defines a "level" in implicit BFS:
- Level 0: positions reachable with 0 jumps (just index 0)
- Level 1: positions reachable with 1 jump
- Level k: positions reachable with k jumps

We don't need a queue because:
1. Positions are visited in order (index 0, 1, 2, ...)
2. `current_end` marks where current level ends
3. `next_farthest` finds where next level ends

### Trace Example

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

### Difference from Base Template

| Aspect | Jump Game (LC 55) | Jump Game II (LC 45) |
|--------|-------------------|----------------------|
| Goal | Reachability (yes/no) | Minimum jumps (count) |
| State | Single variable: `farthest` | Two variables: `current_end`, `next_farthest` |
| Logic | Check if `i > farthest` | Increment count at level boundary |
| Output | Boolean | Integer |


