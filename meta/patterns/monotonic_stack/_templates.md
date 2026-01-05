## Template Quick Reference

### Next Greater Element (Right)

```python
def next_greater(arr):
    n, result, stack = len(arr), [-1] * len(arr), []
    for i in range(n):
        while stack and arr[stack[-1]] < arr[i]:
            result[stack.pop()] = arr[i]
        stack.append(i)
    return result
```

### Previous Smaller Element (Left)

```python
def prev_smaller(arr):
    n, result, stack = len(arr), [-1] * len(arr), []
    for i in range(n):
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        result[i] = arr[stack[-1]] if stack else -1
        stack.append(i)
    return result
```

### Largest Rectangle in Histogram

```python
def largest_rectangle(heights):
    heights, stack, max_area = heights + [0], [-1], 0
    for i, h in enumerate(heights):
        while stack[-1] != -1 and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            max_area = max(max_area, height * (i - stack[-1] - 1))
        stack.append(i)
    return max_area
```

### Trapping Rain Water

```python
def trap(height):
    stack, water = [], 0
    for i, h in enumerate(height):
        while stack and height[stack[-1]] < h:
            bottom = stack.pop()
            if stack:
                w = i - stack[-1] - 1
                bounded = min(height[stack[-1]], h) - height[bottom]
                water += w * bounded
        stack.append(i)
    return water
```

### Sum of Subarray Minimums

```python
def sum_subarray_mins(arr):
    n, MOD = len(arr), 10**9 + 7
    left, right, stack = [0]*n, [0]*n, []
    for i in range(n):
        while stack and arr[stack[-1]] >= arr[i]: stack.pop()
        left[i] = i - stack[-1] if stack else i + 1
        stack.append(i)
    stack = []
    for i in range(n-1, -1, -1):
        while stack and arr[stack[-1]] > arr[i]: stack.pop()
        right[i] = stack[-1] - i if stack else n - i
        stack.append(i)
    return sum(arr[i] * left[i] * right[i] for i in range(n)) % MOD
```


