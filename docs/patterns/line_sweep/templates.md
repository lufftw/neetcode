# Line Sweep Pattern

## Table of Contents

1. [API Kernel: `LineSweep`](#1-api-kernel-linesweep)
2. [Why Line Sweep?](#2-why-line-sweep)
3. [Core Insight](#3-core-insight)
4. [Universal Template Structure](#4-universal-template-structure)
5. [Event Encoding Strategies](#5-event-encoding-strategies)
6. [State Management Data Structures](#6-state-management-data-structures)
7. [Pattern Variants](#7-pattern-variants)
8. [Problem: Meeting Rooms II (LC 253)](#8-problem-meeting-rooms-ii-lc-253)
9. [Problem: Car Pooling (LC 1094)](#9-problem-car-pooling-lc-1094)
10. [Problem: The Skyline Problem (LC 218)](#10-problem-the-skyline-problem-lc-218)
11. [Pattern Comparison](#11-pattern-comparison)
12. [When to Use Each Pattern](#12-when-to-use-each-pattern)
13. [Data Structure Selection](#13-data-structure-selection)
14. [Complexity Comparison](#14-complexity-comparison)
15. [When to Use Line Sweep](#15-when-to-use-line-sweep)
16. [Quick Reference Templates](#16-quick-reference-templates)
17. [Event Encoding Cheat Sheet](#17-event-encoding-cheat-sheet)

---

## 1. API Kernel: `LineSweep`

> **Core Mechanism**: Transform intervals/rectangles into discrete events (start/end points), sort by position, and sweep through maintaining state with a data structure.

## 2. Why Line Sweep?

Line sweep solves problems where:
- You have multiple overlapping intervals, rectangles, or ranges
- You need to track aggregate state (count, max height, capacity) at any point
- Processing all pairs would be O(n²) but events can be processed in O(n log n)

## 3. Core Insight

**Every interval creates two events**: a start event and an end event. By processing events in sorted order, we convert a 2D overlap problem into a 1D scan.

```
Intervals:  [1,4] [2,5] [3,6]

Events:     1:+1  2:+1  3:+1  4:-1  5:-1  6:-1
            ↓     ↓     ↓     ↓     ↓     ↓
Count:      1     2     3     2     1     0
Max = 3 (at position 3)
```

## 4. Universal Template Structure

```python
def line_sweep(intervals):
    # Step 1: Create events
    events = []
    for start, end in intervals:
        events.append((start, +1))  # Start event
        events.append((end, -1))    # End event

    # Step 2: Sort events
    # Tie-breaking rule depends on problem:
    # - For counting overlap: end before start at same position
    # - For skyline: start before end at same position
    events.sort()

    # Step 3: Sweep and maintain state
    current_state = 0
    result = initial_value

    for position, delta in events:
        current_state += delta
        result = update(result, current_state)

    return result
```

## 5. Event Encoding Strategies

| Problem Type | Start Event | End Event | Sort Key | Tie-breaking |
|-------------|-------------|-----------|----------|--------------|
| **Count Overlap** | (pos, +1) | (pos, -1) | position | end before start |
| **Skyline** | (pos, -height) | (pos, height) | position | start before end |
| **Capacity Check** | (pos, +load) | (pos, -load) | position | depends on semantics |

## 6. State Management Data Structures

| Complexity | Data Structure | Use Case |
|------------|----------------|----------|
| Simple counting | Integer counter | Meeting rooms, car pooling |
| Max tracking | Heap or Sorted Container | Skyline problem |
| Complex queries | Segment Tree | Range-based queries |

## 7. Pattern Variants

1. **Event Counting** (Base): Count active intervals at each point
2. **Capacity Tracking**: Track cumulative load/capacity
3. **Height Tracking**: Maintain max height with multiset/heap
4. **Difference Array**: Offline version using prefix sums

---

## 8. Problem: Meeting Rooms II (LC 253)

> **Base Template** for event counting line sweep.

### 8.1 Problem Statement

Given an array of meeting time intervals `[[start, end], ...]`, find the minimum number of conference rooms required.

### 8.2 Pattern: Event Counting

**Invariant**: At any point, track the number of ongoing meetings.

**Key Insight**: Maximum concurrent meetings = minimum rooms needed.

### 8.3 Algorithm

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

### 8.4 Implementation

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

### 8.5 Why End Before Start?

When a meeting ends and another starts at the same time, we can reuse the room:
- Process end (-1) first to free the room
- Then process start (+1) to occupy it

Sort key `(time, delta)` achieves this since -1 < +1.

### 8.6 Complexity

- **Time**: O(n log n) for sorting
- **Space**: O(n) for events array

### 8.7 Alternative: Heap Approach

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

---

## 9. Problem: Car Pooling (LC 1094)

> **Variant**: Capacity tracking with line sweep.

### 9.1 Problem Statement

Given `trips = [[numPassengers, from, to], ...]` and `capacity`, determine if it's possible to pick up and drop off all passengers without exceeding capacity.

### 9.2 Pattern: Capacity Tracking

**Invariant**: At any point, current passengers ≤ capacity.

**Delta from Base**: Events have variable weights (passenger count), not just ±1.

### 9.3 Algorithm

```
trips: [[2,1,5], [3,3,7]], capacity = 4

Events (sorted):
  1: +2 (pickup)   → passengers = 2  ≤ 4 ✓
  3: +3 (pickup)   → passengers = 5  > 4 ✗
  5: -2 (dropoff)  → passengers = 3
  7: -3 (dropoff)  → passengers = 0

Answer: False (exceeded at position 3)
```

### 9.4 Implementation

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

### 9.5 Why Dropoff Before Pickup?

At the same position, passengers exit before new ones board:
- Process dropoff (negative delta) first
- Then process pickup (positive delta)

This is automatic with sort key `(position, delta)` since negative < positive.

### 9.6 Difference Array Alternative

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

### 9.7 Complexity

- **Line Sweep**: O(n log n) time, O(n) space
- **Difference Array**: O(n + P) time, O(P) space where P = max position

### 9.8 Key Differences from Meeting Rooms II

| Aspect | Meeting Rooms II | Car Pooling |
|--------|------------------|-------------|
| Delta | Always ±1 | Variable (passenger count) |
| Goal | Find maximum | Check threshold |
| Return | Count | Boolean |

---

## 10. Problem: The Skyline Problem (LC 218)

> **Advanced Variant**: Height tracking with multiset/heap.

### 10.1 Problem Statement

Given buildings `[[left, right, height], ...]`, return the skyline as a list of key points `[[x, height], ...]` where the silhouette changes.

### 10.2 Pattern: Height Tracking

**Invariant**: Track maximum height among all active buildings at each position.

**Delta from Base**: Instead of counting, maintain a multiset of active heights.

### 10.3 Algorithm

```
Buildings: [[2,9,10], [3,7,15], [5,12,12]]

Events:
  x=2: add height 10     → max = 10  → output [2, 10]
  x=3: add height 15     → max = 15  → output [3, 15]
  x=5: add height 12     → max = 15  (no change)
  x=7: remove height 15  → max = 12  → output [7, 12]
  x=9: remove height 10  → max = 12  (no change)
  x=12: remove height 12 → max = 0   → output [12, 0]

Skyline: [[2,10], [3,15], [7,12], [12,0]]
```

### 10.4 Implementation with SortedList

```python
from sortedcontainers import SortedList

def getSkyline(buildings: list[list[int]]) -> list[list[int]]:
    # Create events: (x, type, height)
    # type: 0 = start (add), 1 = end (remove)
    events = []
    for left, right, height in buildings:
        events.append((left, 0, height))   # Building starts
        events.append((right, 1, height))  # Building ends

    # Sort: by x, then starts before ends, then by height (desc for starts)
    events.sort(key=lambda e: (e[0], e[1], -e[2] if e[1] == 0 else e[2]))

    result = []
    active_heights = SortedList([0])  # Always include ground level

    for x, event_type, height in events:
        if event_type == 0:  # Start
            active_heights.add(height)
        else:  # End
            active_heights.remove(height)

        current_max = active_heights[-1]

        # Only add point if max height changed
        if not result or result[-1][1] != current_max:
            result.append([x, current_max])

    return result
```

### 10.5 Implementation with Heap (Lazy Deletion)

```python
import heapq

def getSkyline_heap(buildings: list[list[int]]) -> list[list[int]]:
    events = []
    for left, right, height in buildings:
        events.append((left, -height, right))  # Start: negative height for max-heap
        events.append((right, 0, 0))           # End: height 0 as marker

    events.sort()
    result = []
    # Max-heap: (-height, end_x)
    heap = [(0, float('inf'))]  # Ground level

    for x, neg_height, end_x in events:
        # Lazy deletion: remove buildings that have ended
        while heap[0][1] <= x:
            heapq.heappop(heap)

        if neg_height:  # Start event
            heapq.heappush(heap, (neg_height, end_x))

        current_max = -heap[0][0]

        if not result or result[-1][1] != current_max:
            result.append([x, current_max])

    return result
```

### 10.6 Event Sorting Strategy

For skyline, the sort order is critical:
1. **Same x**: Process starts before ends (so we see new max before removing old)
2. **Same x, same type**:
   - Starts: taller buildings first (higher height wins)
   - Ends: shorter buildings first (delays height drop)

### 10.7 Why This is Harder Than Meeting Rooms

| Aspect | Meeting Rooms | Skyline |
|--------|---------------|---------|
| State | Simple counter | Max of active set |
| Operation | increment/decrement | insert/delete/find-max |
| Data Structure | Integer | Heap or Sorted Container |
| Output | Single value | List of critical points |

### 10.8 Complexity

- **Time**: O(n log n) for sorting and heap/sorted container operations
- **Space**: O(n) for events and active buildings

### 10.9 Edge Cases

1. Buildings with same left edge: taller one determines skyline
2. Buildings with same right edge: process in order
3. Adjacent buildings: merge if same height
4. Nested buildings: inner building doesn't affect outer skyline

---

## 11. Pattern Comparison

| Problem | Event Type | State Structure | Output | Sort Tie-break |
|---------|------------|-----------------|--------|----------------|
| **Meeting Rooms II** | ±1 (start/end) | Integer counter | Max count | End before start |
| **Car Pooling** | ±passengers | Integer counter | Boolean | Dropoff before pickup |
| **Skyline** | add/remove height | Sorted container | Critical points | Starts before ends |

## 12. When to Use Each Pattern

```
Need to track overlap count?
├── Yes → Event Counting (Meeting Rooms II)
│   └── Need capacity check instead of max?
│       └── Yes → Capacity Tracking (Car Pooling)
└── No → Need to track max height?
    └── Yes → Height Tracking (Skyline)
```

## 13. Data Structure Selection

| Requirement | Data Structure | Example |
|-------------|----------------|---------|
| Count only | Integer | Meeting Rooms II |
| Count with threshold | Integer | Car Pooling |
| Max of active set | Heap or SortedList | Skyline |
| Range queries | Segment Tree | Complex variants |

## 14. Complexity Comparison

| Problem | Time | Space | Key Operation |
|---------|------|-------|---------------|
| Meeting Rooms II | O(n log n) | O(n) | Counter update |
| Car Pooling | O(n log n) | O(n) | Counter check |
| Skyline | O(n log n) | O(n) | Max query + deletion |

---

## 15. When to Use Line Sweep

### 15.1 Pattern Recognition Signals

Use line sweep when you see:

1. **Multiple intervals** that can overlap
2. **Questions about overlap** (count, max, capacity)
3. **Aggregate state** at positions (how many active? max height?)
4. **Temporal or spatial ordering** (sort by time/position makes sense)

### 15.2 Decision Flowchart

```
Problem has intervals/ranges?
├── No → Not line sweep
└── Yes → What do you need to track?
    ├── Count of overlaps → Event Counting
    │   └── Examples: Meeting Rooms II, Course Schedule III
    ├── Sum/capacity → Capacity Tracking
    │   └── Examples: Car Pooling, Range Addition
    └── Max/min of active set → Height Tracking
        └── Examples: Skyline, Falling Squares
```

### 15.3 Line Sweep vs Other Patterns

| Alternative | When to Prefer Alternative |
|-------------|---------------------------|
| **Merge Intervals** | Need to collapse overlapping intervals, not count them |
| **Interval Scheduling** | Greedy selection (maximize non-overlap) |
| **Difference Array** | Bounded positions, avoid sorting |
| **Segment Tree** | Complex range queries with updates |

### 15.4 Problem Transformation Hints

If problem says... | Think about...
---|---
"minimum rooms" | Event counting, find max
"can all fit" | Capacity tracking, check threshold
"silhouette/outline" | Height tracking with sorted container
"at any point in time" | Track state during sweep

### 15.5 Common Pitfalls

1. **Wrong tie-breaking**: End before start vs start before end depends on semantics
2. **Off-by-one**: Half-open intervals `[start, end)` vs closed `[start, end]`
3. **Missing ground level**: Skyline needs height 0 as baseline
4. **Lazy deletion bugs**: Heap approach requires careful cleanup

---

## 16. Quick Reference Templates

### 16.1 Template 1: Event Counting (Meeting Rooms II)

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

### 16.2 Template 2: Capacity Tracking (Car Pooling)

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

### 16.3 Template 3: Height Tracking with SortedList (Skyline)

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

### 16.4 Template 4: Height Tracking with Heap (Lazy Deletion)

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

### 16.5 Template 5: Difference Array (Bounded Range)

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

## 17. Event Encoding Cheat Sheet

| Problem Type | Start | End | Sort Key |
|--------------|-------|-----|----------|
| Count overlap | `(pos, +1)` | `(pos, -1)` | `(pos, delta)` |
| Capacity | `(pos, +load)` | `(pos, -load)` | `(pos, delta)` |
| Skyline | `(pos, 0, h)` | `(pos, 1, h)` | `(pos, type, ±h)` |
| Heap skyline | `(pos, -h, end)` | `(pos, 0, 0)` | natural |



---



*Document generated for NeetCode Practice Framework — API Kernel: line_sweep*
