## Variation: Circular Boundary Search

> **Problem**: Find next greater element in a circular array (LeetCode 503).
> **Key Insight**: Traverse the array twice (2n iterations), but only push indices during the first pass.

### Implementation

```python
def next_greater_circular(nums: list[int]) -> list[int]:
    """
    Find next greater element in circular array.

    Algorithm:
    - Traverse array twice (indices 0 to 2n-1)
    - Use modulo to wrap around: actual_index = i % n
    - Only push indices during first pass (i < n)
    - Second pass only resolves remaining elements

    Time: O(n), Space: O(n)
    """
    n = len(nums)
    result = [-1] * n
    stack = []

    for i in range(2 * n):
        actual_idx = i % n

        # Pop elements that found their circular NGE
        while stack and nums[stack[-1]] < nums[actual_idx]:
            idx = stack.pop()
            result[idx] = nums[actual_idx]

        # Only push during first pass to avoid duplicate processing
        if i < n:
            stack.append(actual_idx)

    return result
```

### Why Push Only in First Pass?

If we push in both passes, indices would be duplicated:
- First pass pushes index 0
- Second pass would push index 0 again (since 2n % n = 0)

By limiting pushes to the first pass, each index is pushed exactly once.

### Termination and "No Boundary" Cases

After 2n iterations:
- Elements remaining in stack have no next greater element in the circular array
- Their result stays -1 (the default)

### Edge Cases

- **Single element**: Result is [-1] (no other element to compare)
- **All equal elements**: All results are -1 (no strictly greater element)
- **Strictly increasing then wraps**: Each element finds its boundary in second pass


