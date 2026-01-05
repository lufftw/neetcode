## Corporate Flight Bookings (LeetCode 1109)

> **Problem**: Given flight bookings with range [first, last] and seat count, compute total seats for each flight.
> **Insight**: Classic difference array for range updates, prefix sum to get final counts.
> **Role**: CANONICAL DIFFERENCE ARRAY problem (range update → point query).

### Problem Structure

Each booking `[first, last, seats]` adds `seats` to flights `first` through `last` (inclusive).

```
Booking [1, 3, 10] means:
Flight 1: +10 seats
Flight 2: +10 seats
Flight 3: +10 seats

Using difference array:
diff[1-1] += 10   (start adding at flight 1, 0-indexed)
diff[3] -= 10     (stop adding after flight 3)
```

### Implementation

```python
class SolutionDifferenceArray:
    """
    Compute total seats reserved for each flight using difference array.

    Difference Array Mechanics:
    - diff[i] = change in seat count at flight i
    - To add 'seats' to range [first, last] (1-indexed):
      diff[first-1] += seats   (start adding, convert to 0-indexed)
      diff[last] -= seats      (stop adding after last)
    - Prefix sum reconstructs actual seat counts

    Why O(n + m)?
    - O(m) to process all bookings (each is O(1))
    - O(n) to compute prefix sum
    - Much better than O(n * m) naive approach

    Time: O(n + m) where n = flights, m = bookings | Space: O(n)
    """
    def corpFlightBookings(self, bookings: List[List[int]], n: int) -> List[int]:
        # Difference array: diff[i] = change in seat count at flight i
        # Use n+1 to handle the boundary case when last == n
        seat_change = [0] * (n + 1)

        # Apply range updates using difference array technique
        for first_flight, last_flight, seat_count in bookings:
            # Convert to 0-indexed: first_flight=1 -> index 0
            seat_change[first_flight - 1] += seat_count    # Start adding seats
            seat_change[last_flight] -= seat_count         # Stop after last flight

        # Prefix sum to reconstruct actual seat counts
        total_seats = []
        current_seats = 0
        for flight_index in range(n):
            current_seats += seat_change[flight_index]
            total_seats.append(current_seats)

        return total_seats
```

### Trace Example

```
bookings = [[1,2,10],[2,3,20],[2,5,25]], n = 5

Building difference array:
Booking [1,2,10]: diff[0]+=10, diff[2]-=10  -> [10,0,-10,0,0,0]
Booking [2,3,20]: diff[1]+=20, diff[3]-=20  -> [10,20,-10,-20,0,0]
Booking [2,5,25]: diff[1]+=25, diff[5]-=25  -> [10,45,-10,-20,0,-25]

Prefix sum:
Flight 1: 0 + 10 = 10
Flight 2: 10 + 45 = 55
Flight 3: 55 + (-10) = 45
Flight 4: 45 + (-20) = 25
Flight 5: 25 + 0 = 25

Answer: [10, 55, 45, 25, 25]
```

### Difference Array vs Naive Approach

| Approach | Time | When Better |
|----------|------|-------------|
| Naive (update each flight) | O(n * m) | Small inputs |
| Difference Array | O(n + m) | Many overlapping ranges |

For this problem with up to 20,000 bookings and 20,000 flights, difference array is essential.


