## Problem: Meeting Rooms II (LC 253)

> **Base Template** for event counting line sweep.

### Problem Statement

Given an array of meeting time intervals `[[start, end], ...]`, find the minimum number of conference rooms required.

### Pattern: Event Counting

**Invariant**: At any point, track the number of ongoing meetings.

**Key Insight**: Maximum concurrent meetings = minimum rooms needed.

### Algorithm

```
Meetings: [[0,30], [5,10], [15,20]]

Events (sorted):
  0: +1 (start)  → count = 1
  5: +1 (start)  → count = 2  ← max
 10: -1 (end)    → count = 1
 15: +1 (start)  → count = 2  ← max
 20: -1 (end)    → count = 1
 30: -1 (end)    → count = 0

Answer: 2 rooms
```

### Implementation

```python
def minMeetingRooms(intervals: list[list[int]]) -> int:
    events = []
    for start, end in intervals:
        events.append((start, 1))   # Meeting starts
        events.append((end, -1))    # Meeting ends

    # Sort: by time, then ends before starts at same time
    events.sort(key=lambda x: (x[0], x[1]))

    max_rooms = 0
    current_rooms = 0

    for _, delta in events:
        current_rooms += delta
        max_rooms = max(max_rooms, current_rooms)

    return max_rooms
```

### Why End Before Start?

When a meeting ends and another starts at the same time, we can reuse the room:
- Process end (-1) first to free the room
- Then process start (+1) to occupy it

Sort key `(time, delta)` achieves this since -1 < +1.

### Complexity

- **Time**: O(n log n) for sorting
- **Space**: O(n) for events array

### Alternative: Heap Approach

```python
import heapq

def minMeetingRooms_heap(intervals: list[list[int]]) -> int:
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[0])  # Sort by start time
    heap = []  # Min-heap of end times

    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heappop(heap)  # Reuse room
        heapq.heappush(heap, end)

    return len(heap)
```

Both approaches are O(n log n), but line sweep generalizes better.
