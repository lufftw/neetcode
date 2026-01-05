## Meeting Rooms II (LeetCode 253)

> **Problem**: Given an array of meeting time intervals, find the minimum number of conference rooms required.
> **Pattern**: Greedy assignment with min-heap of end times
> **Variant**: Interval scheduling with heap

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "minimum rooms/resources" | → Greedy with heap |
| "overlapping intervals" | → Sort + track end times |
| "schedule tasks" | → Min-heap for earliest available |

### The Greedy Insight

```
Meetings: [[0,30], [5,10], [15,20]]

Timeline:
0   5   10  15  20  25  30
|-------- Meeting 0 --------|
    |- M1 -|
            |-M2-|

At t=5: Meeting 1 starts, Meeting 0 still running → need 2 rooms
At t=15: Meeting 2 starts, Meeting 0 still running → need 2 rooms

Minimum rooms = 2 (max concurrent meetings)
```

### Implementation

```python
# Pattern: heap_interval_scheduling
# See: docs/patterns/heap/templates.md Section 5

import heapq

class SolutionHeap:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        """
        Find minimum meeting rooms using min-heap of end times.

        Key Insight:
        - Sort meetings by start time (process chronologically)
        - Min-heap tracks when each room becomes free (end times)
        - For each meeting: if starts after earliest end, reuse room
        - Otherwise, allocate new room

        Why min-heap of end times?
        - We need the room that frees up earliest
        - If new meeting starts >= earliest end, room can be reused
        - Pop the old end time, push new end time
        """
        if not intervals:
            return 0

        # Sort by start time
        intervals.sort(key=lambda x: x[0])

        # Min-heap of end times (when rooms become free)
        end_times: list[int] = []

        for start, end in intervals:
            # Check if earliest-ending room is now free
            if end_times and end_times[0] <= start:
                # Room is free, reuse it (pop old end, push new end)
                heapq.heapreplace(end_times, end)
            else:
                # All rooms busy, allocate new room
                heapq.heappush(end_times, end)

        # Number of rooms = size of heap
        return len(end_times)
```

### Trace Example

```
Input: intervals = [[0,30], [5,10], [15,20]]

After sorting (already sorted by start): [[0,30], [5,10], [15,20]]

Process [0, 30]:
  end_times = [30]
  Rooms needed: 1

Process [5, 10]:
  Earliest end = 30, but meeting starts at 5 (5 < 30)
  Cannot reuse, allocate new room
  end_times = [10, 30]
  Rooms needed: 2

Process [15, 20]:
  Earliest end = 10, meeting starts at 15 (15 >= 10)
  Reuse room! Replace 10 with 20
  end_times = [20, 30]
  Rooms needed: 2

Result: 2 rooms
```

### Alternative: Sweep Line

```python
class SolutionSweepLine:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        """
        Sweep line: track events at each time point.

        Events:
        - +1 at start time (meeting begins)
        - -1 at end time (meeting ends)

        Max concurrent events = max rooms needed.
        """
        events = []
        for start, end in intervals:
            events.append((start, 1))   # Meeting starts
            events.append((end, -1))    # Meeting ends

        # Sort by time; if same time, process ends before starts
        # (room frees up before new meeting uses it)
        events.sort(key=lambda x: (x[0], x[1]))

        max_rooms = 0
        current_rooms = 0

        for time, delta in events:
            current_rooms += delta
            max_rooms = max(max_rooms, current_rooms)

        return max_rooms
```

### Complexity Comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Min-heap | O(n log n) | O(n) | Sort + heap ops |
| Sweep line | O(n log n) | O(n) | Sort events |
| Brute force | O(n²) | O(1) | Check all pairs |

### Related Problems

| Problem | Variation |
|---------|-----------|
| LC 252: Meeting Rooms | Just check if any overlap |
| LC 56: Merge Intervals | Merge overlapping intervals |
| LC 435: Non-overlapping Intervals | Min removals for no overlap |
| LC 1094: Car Pooling | Range update + capacity check |


