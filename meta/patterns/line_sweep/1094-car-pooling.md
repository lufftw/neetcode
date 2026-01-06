## Problem: Car Pooling (LC 1094)

> **Variant**: Capacity tracking with line sweep.

### Problem Statement

Given `trips = [[numPassengers, from, to], ...]` and `capacity`, determine if it's possible to pick up and drop off all passengers without exceeding capacity.

### Pattern: Capacity Tracking

**Invariant**: At any point, current passengers ≤ capacity.

**Delta from Base**: Events have variable weights (passenger count), not just ±1.

### Algorithm

```
trips: [[2,1,5], [3,3,7]], capacity = 4

Events (sorted):
  1: +2 (pickup)   → passengers = 2  ≤ 4 ✓
  3: +3 (pickup)   → passengers = 5  > 4 ✗
  5: -2 (dropoff)  → passengers = 3
  7: -3 (dropoff)  → passengers = 0

Answer: False (exceeded at position 3)
```

### Implementation

```python
def carPooling(trips: list[list[int]], capacity: int) -> bool:
    events = []
    for passengers, start, end in trips:
        events.append((start, passengers))   # Pickup
        events.append((end, -passengers))    # Dropoff

    # Sort: by position, then dropoffs before pickups at same position
    events.sort(key=lambda x: (x[0], x[1]))

    current_passengers = 0
    for _, delta in events:
        current_passengers += delta
        if current_passengers > capacity:
            return False

    return True
```

### Why Dropoff Before Pickup?

At the same position, passengers exit before new ones board:
- Process dropoff (negative delta) first
- Then process pickup (positive delta)

This is automatic with sort key `(position, delta)` since negative < positive.

### Difference Array Alternative

When positions are bounded and small:

```python
def carPooling_diff(trips: list[list[int]], capacity: int) -> bool:
    # Positions bounded by 0 to 1000
    diff = [0] * 1001

    for passengers, start, end in trips:
        diff[start] += passengers
        diff[end] -= passengers

    current = 0
    for delta in diff:
        current += delta
        if current > capacity:
            return False

    return True
```

**Trade-off**: O(max_position) space but O(n + max_position) time (no sorting).

### Complexity

- **Line Sweep**: O(n log n) time, O(n) space
- **Difference Array**: O(n + P) time, O(P) space where P = max position

### Key Differences from Meeting Rooms II

| Aspect | Meeting Rooms II | Car Pooling |
|--------|------------------|-------------|
| Delta | Always ±1 | Variable (passenger count) |
| Goal | Find maximum | Check threshold |
| Return | Count | Boolean |
