## Variation: Container / Valley Resolution

> **Problem**: Calculate trapped rainwater (LeetCode 42).
> **Key Insight**: Each "pop" completes a valley — water trapped between left wall, bottom, and right wall.

### Stack-Based Trapping Rain Water

```python
def trap(height: list[int]) -> int:
    """
    Calculate total trapped rainwater.

    Algorithm:
    - Maintain a monotonically decreasing stack
    - When we see a taller bar, we've found a valley
    - Pop the bottom of the valley, compute water trapped
    - Water width = current_index - left_wall_index - 1
    - Water height = min(left_wall, right_wall) - bottom_height

    Time: O(n), Space: O(n)
    """
    stack = []  # Stack of indices, heights are decreasing
    water = 0

    for i, h in enumerate(height):
        while stack and height[stack[-1]] < h:
            bottom = stack.pop()

            if not stack:
                break  # No left wall, water flows out

            left_wall_idx = stack[-1]
            left_wall_height = height[left_wall_idx]
            right_wall_height = h
            bottom_height = height[bottom]

            width = i - left_wall_idx - 1
            bounded_height = min(left_wall_height, right_wall_height) - bottom_height
            water += width * bounded_height

        stack.append(i)

    return water
```

### Valley Completion on Pop

Each pop operation finalizes a container segment:

```
Heights: [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]

When we reach height 2 at index 3:
  Stack before: [1, 2] (heights [1, 0])
  Pop index 2 (height 0): This is the valley bottom
    Left wall: index 1 (height 1)
    Right wall: index 3 (height 2)
    Width: 3 - 1 - 1 = 1
    Bounded height: min(1, 2) - 0 = 1
    Water: 1 × 1 = 1
```

### Roles in Valley Resolution

- **Bottom**: The popped element (lowest point of the valley)
- **Left wall**: The element below the bottom in the stack
- **Right wall**: The current element that triggered the pop

### Why Each Pop Finalizes a Bounded Container

The monotonically decreasing stack ensures:
1. When we pop, the current element is taller than the popped element
2. The element below the popped is also taller (or we'd have popped it earlier)
3. This creates a "valley" bounded on both sides

### Edge Cases

- **Empty input**: Return 0
- **Single element**: No container possible, return 0
- **Two elements**: No valley possible, return 0
- **No valleys (monotonic)**: Stack never pops with left wall, return 0


