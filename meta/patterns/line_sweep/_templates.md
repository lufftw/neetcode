## Quick Reference Templates

### Template 1: Event Counting (Meeting Rooms II)

```python
def max_overlap(intervals: list[list[int]]) -> int:
    """Find maximum number of overlapping intervals."""
    events = []
    for start, end in intervals:
        events.append((start, 1))   # Start event
        events.append((end, -1))    # End event

    # Sort: by position, then ends before starts (for half-open intervals)
    events.sort(key=lambda x: (x[0], x[1]))

    max_count = current = 0
    for _, delta in events:
        current += delta
        max_count = max(max_count, current)

    return max_count
```

### Template 2: Capacity Tracking (Car Pooling)

```python
def can_fit_capacity(trips: list[tuple[int, int, int]], capacity: int) -> bool:
    """Check if all trips fit within capacity."""
    events = []
    for load, start, end in trips:
        events.append((start, load))    # Add load
        events.append((end, -load))     # Remove load

    events.sort(key=lambda x: (x[0], x[1]))

    current = 0
    for _, delta in events:
        current += delta
        if current > capacity:
            return False

    return True
```

### Template 3: Height Tracking with SortedList (Skyline)

```python
from sortedcontainers import SortedList

def skyline(buildings: list[list[int]]) -> list[list[int]]:
    """Get skyline critical points."""
    events = []
    for left, right, height in buildings:
        events.append((left, 0, height))   # Start
        events.append((right, 1, height))  # End

    # Sort: by x, starts before ends, taller starts first
    events.sort(key=lambda e: (e[0], e[1], -e[2] if e[1] == 0 else e[2]))

    result = []
    heights = SortedList([0])

    for x, event_type, h in events:
        if event_type == 0:
            heights.add(h)
        else:
            heights.remove(h)

        current_max = heights[-1]
        if not result or result[-1][1] != current_max:
            result.append([x, current_max])

    return result
```

### Template 4: Height Tracking with Heap (Lazy Deletion)

```python
import heapq

def skyline_heap(buildings: list[list[int]]) -> list[list[int]]:
    """Get skyline using heap with lazy deletion."""
    events = []
    for left, right, height in buildings:
        events.append((left, -height, right))  # Start: negative for max-heap
        events.append((right, 0, 0))           # End marker

    events.sort()
    result = []
    heap = [(0, float('inf'))]  # (neg_height, end_x)

    for x, neg_h, end_x in events:
        # Lazy cleanup
        while heap[0][1] <= x:
            heapq.heappop(heap)

        if neg_h:  # Start event
            heapq.heappush(heap, (neg_h, end_x))

        curr_max = -heap[0][0]
        if not result or result[-1][1] != curr_max:
            result.append([x, curr_max])

    return result
```

### Template 5: Difference Array (Bounded Range)

```python
def range_add_query(n: int, updates: list[tuple[int, int, int]]) -> list[int]:
    """Apply range updates, return final array."""
    diff = [0] * (n + 1)

    for start, end, val in updates:
        diff[start] += val
        diff[end + 1] -= val

    # Convert difference array to actual values
    result = []
    current = 0
    for i in range(n):
        current += diff[i]
        result.append(current)

    return result
```

## Event Encoding Cheat Sheet

| Problem Type | Start | End | Sort Key |
|--------------|-------|-----|----------|
| Count overlap | `(pos, +1)` | `(pos, -1)` | `(pos, delta)` |
| Capacity | `(pos, +load)` | `(pos, -load)` | `(pos, delta)` |
| Skyline | `(pos, 0, h)` | `(pos, 1, h)` | `(pos, type, ±h)` |
| Heap skyline | `(pos, -h, end)` | `(pos, 0, 0)` | natural |
