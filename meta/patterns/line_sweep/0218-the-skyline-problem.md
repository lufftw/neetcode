## Problem: The Skyline Problem (LC 218)

> **Advanced Variant**: Height tracking with multiset/heap.

### Problem Statement

Given buildings `[[left, right, height], ...]`, return the skyline as a list of key points `[[x, height], ...]` where the silhouette changes.

### Pattern: Height Tracking

**Invariant**: Track maximum height among all active buildings at each position.

**Delta from Base**: Instead of counting, maintain a multiset of active heights.

### Algorithm

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

### Implementation with SortedList

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

### Implementation with Heap (Lazy Deletion)

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

### Event Sorting Strategy

For skyline, the sort order is critical:
1. **Same x**: Process starts before ends (so we see new max before removing old)
2. **Same x, same type**:
   - Starts: taller buildings first (higher height wins)
   - Ends: shorter buildings first (delays height drop)

### Why This is Harder Than Meeting Rooms

| Aspect | Meeting Rooms | Skyline |
|--------|---------------|---------|
| State | Simple counter | Max of active set |
| Operation | increment/decrement | insert/delete/find-max |
| Data Structure | Integer | Heap or Sorted Container |
| Output | Single value | List of critical points |

### Complexity

- **Time**: O(n log n) for sorting and heap/sorted container operations
- **Space**: O(n) for events and active buildings

### Edge Cases

1. Buildings with same left edge: taller one determines skyline
2. Buildings with same right edge: process in order
3. Adjacent buildings: merge if same height
4. Nested buildings: inner building doesn't affect outer skyline
