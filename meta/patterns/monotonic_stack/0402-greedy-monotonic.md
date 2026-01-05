## Variation: Greedy Monotonic Stack

> **Problem**: Remove K digits to get the smallest number (LeetCode 402).
> **Key Insight**: Maintain a monotonically increasing stack as the "greedy best prefix".

### Remove K Digits

```python
def remove_k_digits(num: str, k: int) -> str:
    """
    Remove k digits to create the smallest possible number.

    Algorithm:
    - Maintain monotonically increasing stack (greedy best prefix)
    - Pop larger digits when a smaller digit is seen (local optimality)
    - Handle leading zeros and remaining k

    Time: O(n), Space: O(n)
    """
    stack = []

    for digit in num:
        # Pop larger digits if we can still remove (k > 0)
        while k > 0 and stack and stack[-1] > digit:
            stack.pop()
            k -= 1
        stack.append(digit)

    # If k > 0, remove from the end (stack is increasing, end is largest)
    if k > 0:
        stack = stack[:-k]

    # Remove leading zeros and handle empty result
    result = ''.join(stack).lstrip('0')
    return result if result else '0'
```

### Greedy Optimality

The pop decision is locally optimal:
- If we see digit `d` and stack top is `s > d`, removing `s` gives a smaller number
- The monotonic increasing property ensures the "best so far" prefix

### Remove Duplicate Letters (LeetCode 316)

```python
def remove_duplicate_letters(s: str) -> str:
    """
    Remove duplicate letters to get lexicographically smallest result.
    Each character must appear exactly once.

    Additional constraints:
    - Track last occurrence of each character
    - Only pop if the character appears later

    Time: O(n), Space: O(26) = O(1)
    """
    last_occurrence = {c: i for i, c in enumerate(s)}
    stack = []
    in_stack = set()

    for i, c in enumerate(s):
        if c in in_stack:
            continue

        # Pop if current is smaller and popped char appears later
        while stack and stack[-1] > c and last_occurrence[stack[-1]] > i:
            in_stack.remove(stack.pop())

        stack.append(c)
        in_stack.add(c)

    return ''.join(stack)
```

### Similar Problems

| Problem | Key Constraint | Stack Order |
|---------|----------------|-------------|
| 402 Remove K Digits | Remove exactly k | Increasing |
| 316 Remove Duplicate Letters | Each char once | Increasing with occurrence check |
| 321 Create Maximum Number | Combine two arrays | Decreasing (for max) |


