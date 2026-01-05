## Base Template: Next Greater / Next Smaller Boundaries

> **Pattern**: Find, for each element, the nearest element satisfying a comparison condition.
> **Invariant**: Stack contains indices of elements awaiting their boundary, in monotonic order.
> **Role**: BASE TEMPLATE for `MonotonicStack` API Kernel.

### Four Boundary Directions

| Pattern | Direction | Stack Order | Comparison | Common Name |
|---------|-----------|-------------|------------|-------------|
| NGE-R | Next Greater to Right | Decreasing | `>` | Next Greater Element |
| NGE-L | Next Greater to Left | Decreasing (reverse) | `>` | Previous Greater Element |
| NSE-R | Next Smaller to Right | Increasing | `<` | Next Smaller Element |
| PSE-L | Previous Smaller to Left | Increasing (reverse) | `<` | Previous Smaller Element |

### Next Greater Element to the Right (NGE-R)

```python
def next_greater_element(nums: list[int]) -> list[int]:
    """
    For each element, find the next greater element to its right.
    Returns -1 if no such element exists.

    Algorithm:
    - Maintain a monotonically decreasing stack (by value)
    - When current element > stack top, stack top found its NGE
    - Each element is pushed once and popped at most once → O(n)

    Time: O(n), Space: O(n)
    """
    n = len(nums)
    result = [-1] * n  # Default: no next greater
    stack = []  # Stack of indices, values are decreasing

    for i in range(n):
        # Pop all elements smaller than current (they found their NGE)
        while stack and nums[stack[-1]] < nums[i]:
            idx = stack.pop()
            result[idx] = nums[i]  # or result[idx] = i for index
        stack.append(i)

    return result
```

### Previous Smaller Element to the Left (PSE-L)

```python
def previous_smaller_element(nums: list[int]) -> list[int]:
    """
    For each element, find the previous smaller element to its left.
    Returns -1 if no such element exists.

    Algorithm:
    - Maintain a monotonically increasing stack (by value)
    - For each element, pop until we find a smaller element
    - The stack top (if exists) is the previous smaller element

    Time: O(n), Space: O(n)
    """
    n = len(nums)
    result = [-1] * n
    stack = []  # Stack of indices, values are increasing

    for i in range(n):
        # Pop elements >= current (they can't be PSE for future elements)
        while stack and nums[stack[-1]] >= nums[i]:
            stack.pop()

        # Stack top (if exists) is the previous smaller element
        if stack:
            result[i] = nums[stack[-1]]  # or stack[-1] for index

        stack.append(i)

    return result
```

### Returning Value vs Index vs Distance

The same algorithm can return different information based on the problem:

```python
def next_greater_variants(nums: list[int]) -> tuple[list[int], list[int], list[int]]:
    """
    Compute NGE returning value, index, and distance.
    """
    n = len(nums)
    nge_value = [-1] * n     # The value of next greater element
    nge_index = [-1] * n     # The index of next greater element
    nge_distance = [0] * n   # Distance to next greater element
    stack = []

    for i in range(n):
        while stack and nums[stack[-1]] < nums[i]:
            idx = stack.pop()
            nge_value[idx] = nums[i]
            nge_index[idx] = i
            nge_distance[idx] = i - idx
        stack.append(i)

    return nge_value, nge_index, nge_distance
```

### Handling Duplicates: Strict vs Non-Strict Comparisons

**Strict comparison (`<` or `>`)**: Equal elements do NOT satisfy the boundary condition.

```python
# Strict: Find next STRICTLY greater (not equal)
while stack and nums[stack[-1]] < nums[i]:  # < means strictly less
    # ...
```

**Non-strict comparison (`<=` or `>=`)**: Equal elements DO satisfy the boundary condition.

```python
# Non-strict: Find next greater or equal
while stack and nums[stack[-1]] <= nums[i]:  # <= includes equal
    # ...
```

**When to use which:**
- **Strict**: Default for most problems (Next Greater Element)
- **Non-strict**: When duplicates should be treated as boundaries (e.g., contribution counting to avoid double-counting)


