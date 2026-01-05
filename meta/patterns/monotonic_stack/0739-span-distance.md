## Variation: Span / Distance Aggregation

> **Problem**: Compute how many consecutive days the stock price was less than or equal to today's price (LeetCode 901).
> **Key Insight**: Span = distance to previous greater element.

### Daily Temperatures (LeetCode 739)

```python
def daily_temperatures(temperatures: list[int]) -> list[int]:
    """
    For each day, find how many days until a warmer temperature.
    This is the distance to the next greater element.

    Time: O(n), Space: O(n)
    """
    n = len(temperatures)
    result = [0] * n
    stack = []  # Stack of indices, temperatures are decreasing

    for i in range(n):
        while stack and temperatures[stack[-1]] < temperatures[i]:
            idx = stack.pop()
            result[idx] = i - idx  # Distance to next greater
        stack.append(i)

    return result
```

### Online Stock Span (LeetCode 901)

```python
class StockSpanner:
    """
    Online computation of stock span.
    Span = number of consecutive days with price <= today's price.

    Key insight: Span includes the current day plus all days
    that were "dominated" by previous greater prices.

    Stack stores (price, span) pairs.
    """
    def __init__(self):
        self.stack = []

    def next(self, price: int) -> int:
        span = 1  # Current day counts

        # Pop and accumulate spans of dominated days
        while self.stack and self.stack[-1][0] <= price:
            _, prev_span = self.stack.pop()
            span += prev_span

        self.stack.append((price, span))
        return span
```

### Span Interpretation

The span at position `i` represents:
- **Count interpretation**: Number of consecutive elements to the left that are dominated
- **Distance interpretation**: `i - index_of_previous_greater_element`

### Key Differences from Base Template

| Aspect | Base NGE | Span/Distance |
|--------|----------|---------------|
| Resolves | Value of boundary | Distance to boundary |
| Returns | Boundary element | Count or distance |
| Stack stores | Just indices | May store (value, span) pairs |


