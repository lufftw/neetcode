## Variation: Binary Search on Answer Space (LeetCode 875, 1011)

> **Problem**: Find the minimum (or maximum) value that satisfies a feasibility predicate.
> **Key Insight**: The answer itself is what we binary search, not an index.
> **Invariant**: If `x` is feasible, all values greater (or less) are also feasible.

### When to Use Binary Search on Answer

This pattern applies when:

1. You need to find an **optimal value** (minimize/maximize)
2. There's a **monotonic feasibility** condition
3. You can **check feasibility** in O(n) or better

```
Search Space for "Minimize Maximum":
┌─────────────────────────────────────────────────────────────┐
│  Answer Space: [min_possible, max_possible]                 │
│                                                             │
│  [infeasible, infeasible, ..., feasible, feasible, ...]    │
│                                   ↑                         │
│                              first feasible = answer        │
└─────────────────────────────────────────────────────────────┘
```

### Template

```python
def binary_search_on_answer(lo: int, hi: int, is_feasible) -> int:
    """
    Find the minimum value in [lo, hi] where is_feasible(x) is True.

    Requirements:
    - is_feasible is monotonic: if is_feasible(x), then is_feasible(x+1)
    - At least one value in [lo, hi] must be feasible

    This is exactly predicate boundary search over the answer space.

    Time Complexity: O(log(hi - lo) × feasibility_check)
    Space Complexity: O(1)

    Args:
        lo: Minimum possible answer (inclusive)
        hi: Maximum possible answer (inclusive)
        is_feasible: Function returning True if answer x is feasible

    Returns:
        Minimum feasible answer
    """
    while lo < hi:
        mid = lo + (hi - lo) // 2

        if is_feasible(mid):
            # mid works, but maybe something smaller also works
            hi = mid
        else:
            # mid doesn't work, need larger value
            lo = mid + 1

    return lo
```

### Koko Eating Bananas (LeetCode 875)

```python
def min_eating_speed(piles: list[int], h: int) -> int:
    """
    Find minimum eating speed k to finish all bananas within h hours.

    Problem:
    - Each hour, Koko eats k bananas from one pile
    - If pile has less than k, she eats the whole pile and waits
    - Find minimum k such that total hours <= h

    Insight:
    - Answer space: [1, max(piles)]
    - If k=1 works, any larger k also works (monotonic)
    - Feasibility check: sum(ceil(pile/k) for pile in piles) <= h

    Predicate: can_finish(k) = total_hours(k) <= h

    Time Complexity: O(n × log(max(piles)))
    Space Complexity: O(1)

    Args:
        piles: Array of banana pile sizes
        h: Available hours

    Returns:
        Minimum eating speed
    """
    def hours_needed(speed: int) -> int:
        """Calculate total hours needed at given speed."""
        total = 0
        for pile in piles:
            # Ceiling division: (pile + speed - 1) // speed
            total += (pile + speed - 1) // speed
        return total

    def can_finish(speed: int) -> bool:
        """Check if Koko can finish within h hours at this speed."""
        return hours_needed(speed) <= h

    # Answer space: [1, max(piles)]
    # At speed = max(piles), each pile takes 1 hour
    lo, hi = 1, max(piles)

    while lo < hi:
        mid = lo + (hi - lo) // 2

        if can_finish(mid):
            # This speed works, try to find a smaller one
            hi = mid
        else:
            # Too slow, need faster eating
            lo = mid + 1

    return lo
```

### Capacity To Ship Packages (LeetCode 1011)

```python
def ship_within_days(weights: list[int], days: int) -> int:
    """
    Find minimum ship capacity to ship all packages within given days.

    Problem:
    - Packages must be shipped in order (no reordering)
    - Each day, ship consecutive packages up to capacity
    - Find minimum capacity to finish in exactly `days` days

    Insight:
    - Minimum capacity = max(weights) (must fit largest package)
    - Maximum capacity = sum(weights) (ship everything in one day)
    - If capacity C works, C+1 also works (monotonic)

    Feasibility Check:
    - Greedily fill each day up to capacity
    - Count days needed
    - Return days_needed <= days

    Time Complexity: O(n × log(sum(weights)))
    Space Complexity: O(1)

    Args:
        weights: Array of package weights (in order)
        days: Number of days to ship all packages

    Returns:
        Minimum ship capacity
    """
    def days_needed(capacity: int) -> int:
        """Calculate days needed to ship all packages at given capacity."""
        day_count = 1
        current_load = 0

        for weight in weights:
            if current_load + weight > capacity:
                # Start a new day
                day_count += 1
                current_load = weight
            else:
                current_load += weight

        return day_count

    def can_ship(capacity: int) -> bool:
        """Check if all packages can be shipped within `days` days."""
        return days_needed(capacity) <= days

    # Answer space: [max(weights), sum(weights)]
    lo = max(weights)  # Must fit largest package
    hi = sum(weights)  # Can ship everything in one day

    while lo < hi:
        mid = lo + (hi - lo) // 2

        if can_ship(mid):
            # This capacity works, try smaller
            hi = mid
        else:
            # Need more capacity
            lo = mid + 1

    return lo
```

### Common Answer Space Problems

| Problem | Answer Space | Feasibility Predicate | Monotonicity |
|---------|-------------|----------------------|--------------|
| Koko Eating Bananas | [1, max(piles)] | hours_needed <= h | Increasing k → decreasing hours |
| Ship Packages | [max(w), sum(w)] | days_needed <= d | Increasing cap → decreasing days |
| Split Array (410) | [max(nums), sum(nums)] | splits_needed <= m | Increasing max → decreasing splits |
| Magnetic Force (1552) | [1, max_dist] | can_place_balls | Increasing dist → harder to place |


