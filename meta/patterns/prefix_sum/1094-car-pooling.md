## Car Pooling (LeetCode 1094)

> **Problem**: Check if a car can pick up and drop off all passengers without exceeding capacity.
> **Insight**: Model as range updates; use difference array to track passenger count changes.
> **Role**: DIFFERENCE ARRAY VARIANT (inverse of prefix sum).

### Difference Array Principle

Difference array is the **inverse** of prefix sum:
- **Prefix Sum**: Given point values, compute range sums in O(1)
- **Difference Array**: Given range updates, compute point values in O(n)

```
To add 'value' to range [start, end]:
  diff[start] += value   (start adding)
  diff[end+1] -= value   (stop adding after end)

Prefix sum of diff = actual values at each point
```

### Implementation

```python
class SolutionDifferenceArray:
    """
    Check if car pooling is feasible using difference array.

    Difference Array Technique:
    1. Record passenger changes at pickup/dropoff locations
    2. Prefix sum gives actual passenger count at each location
    3. Verify no location exceeds capacity

    Key Insight:
    - Passengers board at 'from' location
    - Passengers exit at 'to' location (NOT inclusive - they're gone before 'to')
    - This creates range [from, to) updates

    Time: O(n + m) where n = trips, m = max location | Space: O(m)
    """
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        # Find max location to determine array size
        max_location = max(trip[2] for trip in trips)

        # Difference array: diff[i] = change in passenger count at location i
        passenger_change = [0] * (max_location + 1)

        # Build difference array
        for passengers, pickup_location, dropoff_location in trips:
            passenger_change[pickup_location] += passengers    # Passengers board
            passenger_change[dropoff_location] -= passengers   # Passengers exit

        # Prefix sum to compute actual passenger count at each location
        current_passengers = 0
        for delta in passenger_change:
            current_passengers += delta
            if current_passengers > capacity:
                return False

        return True
```

### Trace Example

```
trips = [[2,1,5],[3,3,7]], capacity = 4

Location:  0   1   2   3   4   5   6   7
           ↓   ↓   ↓   ↓   ↓   ↓   ↓   ↓
diff:     [0, +2,  0, +3,  0, -2,  0, -3]

Prefix sum (passengers at each location):
loc 0: 0
loc 1: 0 + 2 = 2  ✓
loc 2: 2 + 0 = 2  ✓
loc 3: 2 + 3 = 5  > 4  ✗

Answer: False (exceeds capacity at location 3)
```

### Why Dropoff is Exclusive

Passengers exit BEFORE the dropoff location:
```
Trip: [2, 1, 3] means 2 passengers from location 1 to 3
At location 3, they're already gone!

diff[1] += 2  (board at 1)
diff[3] -= 2  (exit at 3, so location 3 has no extra passengers)
```


